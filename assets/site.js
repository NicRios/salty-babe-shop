const button = document.querySelector('.menu-toggle');
const menu = document.querySelector('#mobile-menu');
function setMenu(open) {
  button.setAttribute('aria-expanded', String(open));
  menu.hidden = !open;
  document.body.classList.toggle('menu-open', open);
  if (open) menu.querySelector('a').focus();
  else button.focus();
}
button.addEventListener('click', () => setMenu(button.getAttribute('aria-expanded') !== 'true'));
document.addEventListener('keydown', event => {
  if (menu.hidden) return;
  if (event.key === 'Escape') { setMenu(false); return; }
  if (event.key === 'Tab') {
    const links = [...menu.querySelectorAll('a')];
    if (!event.shiftKey && document.activeElement === links.at(-1)) { event.preventDefault(); button.focus(); }
    else if (event.shiftKey && document.activeElement === button) { event.preventDefault(); links.at(-1).focus(); }
  }
});
matchMedia('(min-width:768px)').addEventListener('change', event => {
  if (event.matches) { menu.hidden = true; button.setAttribute('aria-expanded','false'); document.body.classList.remove('menu-open'); }
});
