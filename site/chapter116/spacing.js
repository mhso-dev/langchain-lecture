// These are recorded outcomes of the chapter 98 local fixture.
const lab = document.querySelector('#spacing-lab');
const records = {
  A: {id: 'Q98-N01', rule: 'RULE-A', answer: '점검 전 전원 표시등을 확인합니다.'},
  B: {id: 'Q98-N02', rule: 'RULE-B', answer: '점검 전 고정 장치를 확인합니다.'},
  AB: {id: 'Q98-G01'}
};
function drawProof() {
  const label = lab.querySelector('input[name="equipment-case"]:checked').value;
  const enabled = lab.querySelector('#spacing-patch').checked;
  const known = label !== 'AB';
  const matched = enabled && known;
  const record = records[label];
  lab.classList.toggle('has-space', matched);
  lab.querySelector('#equipment-letter').textContent = label[0];
  lab.querySelector('#equipment-tail').hidden = known;
  lab.querySelector('#case-id').textContent = record.id;
  let note = '‘비’와 ‘' + label + '’가 붙어 있습니다. 검색기가 찾는 ‘장비 ' + label + '’와 공백 한 칸이 다릅니다.';
  if (!known) {
    note = enabled ? 'A 바로 뒤에 B가 있습니다. 두 글자를 한 이름으로 남겨 두므로 공백이 생기지 않습니다.' : 'AB는 두 글자로 된 이름입니다. 이 이름으로 고를 수 있는 규정은 없습니다.';
  } else if (enabled) {
    note = '‘비’와 ‘' + label + '’ 사이에 공백을 넣자 검색기에 ‘장비 ' + label + '’가 들어갑니다.';
  }
  lab.querySelector('#proof-note').textContent = note;
  lab.querySelector('#proof-answer').textContent = matched ? record.answer : '장비 A 또는 장비 B 중 하나를 지정하세요.';
  lab.querySelector('#proof-rule').textContent = matched ? record.rule : '근거 규정 없음';
}
lab.addEventListener('change', drawProof);
drawProof();
lab.querySelector('.spacing-controls').hidden = false;
