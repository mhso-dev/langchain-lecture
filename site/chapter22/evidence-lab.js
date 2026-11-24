(() => {
  const panel = document.getElementById('evidence-lab');
  if (!panel) return;
  const data = JSON.parse(panel.querySelector('script[type="application/json"]').textContent);
  const picker = panel.querySelector('select');
  const status = panel.querySelector('[data-status]');
  const source = panel.querySelector('[data-source]');
  const origin = panel.querySelector('[data-origin]');
  const metric = panel.querySelector('[data-metric]');
  const buttons = [...panel.querySelectorAll('[data-result]')];
  const words = data.vocabulary;
  const characters = Array.from(data.page);
  const vector = text => words.map(word => Number(text.includes(word)));
  const squaredDistance = (left, right) => left.reduce((sum, value, i) => sum + (value - right[i]) ** 2, 0);
  let rows, queryVector, tied;

  function showSource(index) {
    buttons.forEach((button, i) => button.setAttribute('aria-pressed', String(i === index)));
    if (index === null) {
      metric.textContent = '두 후보까지의 거리가 같습니다. 각 후보의 원문을 열어 주차 요금이 적혀 있는지 확인해 보세요.';
      origin.textContent = '선택한 청크 없음';
      source.textContent = data.page;
      return;
    }
    const row = rows[index], chunk = row.chunk;
    const highlight = document.createElement('mark');
    highlight.textContent = characters.slice(chunk.start, chunk.end).join('');
    source.replaceChildren(characters.slice(0, chunk.start).join(''), highlight, characters.slice(chunk.end).join(''));
    origin.textContent = `${chunk.source} · ${chunk.page}쪽 · ${chunk.id} · [${chunk.start}:${chunk.end}]`;
    const terms = queryVector.map((q, i) => `(${q} − ${row.vector[i]})²`).join(' + ');
    metric.textContent = `${terms} = ${row.distance} · FAISS 입력 위치 ${row.position}`;
    status.textContent = `${chunk.id} 원문 선택. ${tied ? '두 후보가 같은 거리입니다.' : ''}`;
  }

  function search() {
    queryVector = vector(picker.value);
    rows = data.chunks.map((chunk, position) => {
      const coordinates = vector(chunk.text);
      return {chunk, position, vector: coordinates, distance: squaredDistance(queryVector, coordinates)};
    }).sort((a, b) => a.distance - b.distance || a.position - b.position);
    tied = rows[0].distance === rows[1].distance;
    panel.querySelector('[data-vector]').textContent = `[${queryVector.join(', ')}]`;
    buttons.forEach((button, i) => {
      const row = rows[i];
      button.querySelector('[data-rank]').textContent = tied ? '공동 1위' : `${i + 1}위`;
      button.querySelector('[data-id]').textContent = row.chunk.id;
      button.querySelector('[data-coordinates]').textContent = `[${row.vector.join(', ')}]`;
      button.querySelector('[data-distance]').textContent = `거리 ${row.distance}`;
    });
    showSource(tied ? null : 0);
    status.textContent = tied ? '두 후보의 거리가 같아 자동 선택을 보류했습니다.' : `검색 1위 ${rows[0].chunk.id}의 원문을 표시했습니다.`;
  }
  picker.addEventListener('change', search);
  buttons.forEach((button, i) => button.addEventListener('click', () => showSource(i)));
  search();
})();
