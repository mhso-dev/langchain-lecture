const input = document.querySelector('#topic-search');
const cards = [...document.querySelectorAll('.topic')];
function searchTopics(){
  const words = input.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
  const number = /^(\d+)(?:일차|장|일)?$/.exec(input.value.trim());
  for (const card of cards) {
    const terms = card.dataset.key.toLowerCase();
    card.hidden = number ? !card.dataset.lessons.split(' ').includes(String(Number(number[1]))) : !words.every(word => terms.includes(word));
  }
  for (const group of document.querySelectorAll('.collection')) {
    group.hidden = !group.querySelector('.topic:not([hidden])');
  }
  const count = cards.filter(card => !card.hidden).length;
  document.querySelector('#matches').textContent = count ? count+'개 단원' : '일치하는 단원이 없습니다.';
}
input.addEventListener('input',searchTopics);
searchTopics();
const old = /^#(chapter\d{2,3})(-figures)?(?:\/([\w-]+))?$/.exec(location.hash);
if (old && +old[1].slice(7) >= 1 && +old[1].slice(7) <= 120) {
  location.replace(old[1]+'/index.html'+(old[3] ? '#'+old[3] : ''));
}
