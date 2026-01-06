export const showMessage = (el, msg, type = 'success', timeout = 4000) => {
  if (!el) {
    console.warn('Message element not found');
    return;
  }
  
  el.textContent = msg;
  el.className = `message ${type}`;
  el.classList.remove('hidden');

  if (timeout) {
    setTimeout(() => el.classList.add('hidden'), timeout);
  }
};

export const hideMessage = (el) => {
  if (!el) return;
  el.classList.add('hidden');
  el.textContent = '';
};