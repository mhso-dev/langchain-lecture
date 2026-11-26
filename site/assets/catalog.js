const search = document.querySelector('#search');
const projects = document.querySelector('#projects');
function filterChapters() {
  const query = search.value.trim().toLowerCase();
  const day = /^(\d+)(?:일차|일|장)?$/.exec(query);
  let count = 0;
  for (const unit of document.querySelectorAll('.unit')) {
    const include = !unit.hasAttribute('data-project') || projects?.checked;
    for (const card of unit.querySelectorAll('.card')) {
      const terms = card.dataset.search.toLowerCase();
      const matches = day ? terms.startsWith(Number(day[1]) + '일차 ') : query.split(/\s+/).every(word => terms.includes(word));
      card.hidden = !include || !matches;
      if (!card.hidden) count++;
    }
    unit.hidden = !unit.querySelector('.card:not([hidden])');
  }
  document.querySelector('#count').textContent = count + '개 장 표시';
}
search.addEventListener('input', filterChapters);
projects?.addEventListener('change', filterChapters);
filterChapters();

// Preserve bookmarks created by the portable textbook reader.
const route = /^#(chapter\d{2,3})(-figures)?(?:\/([\w-]+))?$/.exec(location.hash);
if (route && document.querySelector('a[href="' + route[1] + '/index.html"]')) {
  const page = 'index.html';
  location.replace(route[1] + '/' + page + (route[3] ? '#' + route[3] : ''));
}
