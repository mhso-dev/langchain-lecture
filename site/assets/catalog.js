const search = document.querySelector('#search');
const available = document.querySelector('#available');
function filterChapters() {
  const query = search.value.trim().toLowerCase().replace(/^(\d+)장/, '$1');
  let count = 0;
  for (const card of document.querySelectorAll('.card')) {
    card.hidden = !card.dataset.search.toLowerCase().includes(query)
      || (available.checked && card.dataset.available !== 'true');
    if (!card.hidden) count++;
  }
  for (const unit of document.querySelectorAll('.unit')) {
    unit.hidden = !unit.querySelector('.card:not([hidden])');
  }
  document.querySelector('#count').textContent = count + '개 장 표시';
}
search.addEventListener('input', filterChapters);
available.addEventListener('change', filterChapters);
filterChapters();

// Preserve bookmarks created by the portable textbook reader.
const route = /^#(chapter\d{2,3})(-figures)?(?:\/([\w-]+))?$/.exec(location.hash);
if (route && document.querySelector('a[href="' + route[1] + '/index.html"]')) {
  const page = route[2] && route[1] === 'chapter12' ? 'figures.html' : 'index.html';
  location.replace(route[1] + '/' + page + (route[3] ? '#' + route[3] : ''));
}
