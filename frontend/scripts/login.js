import { dataSubmit } from './dataFetch.js';
import { showMessage } from './uiMessage.js';

const btn = document.querySelector('.js-submit-button');  // Changed from '.js-submit'
const email = document.getElementById('email');
const password = document.getElementById('password');
const msgBox = document.getElementById('message');

btn.addEventListener('click', async () => {
  if (!email.value || !password.value) {
    showMessage(msgBox, 'Fill all fields', 'error');
    return;
  }

  btn.disabled = true;
  btn.textContent = 'Logging in...';

  try {
    const res = await dataSubmit(
      { email: email.value, password: password.value },
      'http://127.0.0.1:3000/login'
    );

    if (!res.success) {
      showMessage(msgBox, res.data?.msg || 'Login failed', 'error');
      return;
    }

    if (!res.data.access_token || !res.data.refresh_token) {
      showMessage(msgBox, 'Invalid server response', 'error');
      return;
    }

    localStorage.setItem('access_token', res.data.access_token);
    localStorage.setItem('refresh_token', res.data.refresh_token);

    window.location.href = 'dashboard.html';
  } catch (err) {
    showMessage(msgBox, 'An unexpected error occurred', 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Login';
  }
});