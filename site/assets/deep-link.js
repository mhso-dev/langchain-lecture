function revealTopic() {
  if (!location.hash) return;
  let name;
  try { name = decodeURIComponent(location.hash.slice(1)); } catch { return; }
  const target = document.getElementById(name);
  if (!target) return;
  let parent = target.closest('details');
  while (parent) {
    parent.open = true;
    parent = parent.parentElement?.closest('details');
  }
  target.scrollIntoView();
}
window.addEventListener('hashchange', revealTopic);
window.addEventListener('DOMContentLoaded', revealTopic);
