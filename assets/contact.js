// This local prototype validates the form but never sends or stores inquiries.
const inquiryForm = document.querySelector('#contact-form');
if (inquiryForm) {
  const inquiryStatus = document.querySelector('#contact-status');
  inquiryForm.addEventListener('submit', (event) => {
    event.preventDefault();
    inquiryStatus.textContent = 'This is a preview. Your inquiry has not been sent.';
    inquiryStatus.hidden = false;
    inquiryStatus.focus();
  });
  inquiryForm.addEventListener('input', () => {
    inquiryStatus.hidden = true;
  });
  inquiryForm.querySelector('[type="submit"]').disabled = false;
}
