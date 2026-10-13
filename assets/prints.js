(() => {
  const form = document.querySelector('#print-form');
  if (!form) return;

  const size = form.querySelector('#print-size');
  const border = form.querySelector('#print-border');
  const units = form.querySelectorAll('input[name="units"]');
  const unitLabel = document.querySelector('#print-unit-label');
  const price = document.querySelector('#print-price');
  const preview = document.querySelector('#print-preview');
  const status = document.querySelector('#print-status');
  const addButton = form.querySelector('button[type="submit"]');
  const title = document.querySelector('#print-title').textContent;

  function updatePreview() {
    const unit = form.querySelector('input[name="units"]:checked').value;
    for (const option of size.options) {
      option.textContent = option.dataset[unit];
    }
    unitLabel.textContent = unit;
    price.textContent = `USD $${size.selectedOptions[0].dataset.price}`;
    preview.classList.toggle('has-border', border.value === 'white');
    status.hidden = true;
  }

  size.addEventListener('change', updatePreview);
  border.addEventListener('change', updatePreview);
  units.forEach(input => input.addEventListener('change', updatePreview));
  window.addEventListener('pageshow', updatePreview);

  form.addEventListener('submit', event => {
    event.preventDefault();
    const unit = form.querySelector('input[name="units"]:checked').value === 'inches' ? 'in' : 'cm';
    const selection = `${title}, ${size.selectedOptions[0].textContent} ${unit}, ${border.selectedOptions[0].textContent}`;
    status.textContent = `Added to your preview: ${selection}. This is a prototype; no order has been placed.`;
    status.hidden = false;
    status.focus({ preventScroll: true });
  });

  updatePreview();
  addButton.disabled = false;
})();
