import { dataSubmit } from './dataFetch.js';
import { showMessage } from './uiMessage.js';
import { API_URL } from './config.js';

const btn = document.querySelector('.js-submit-button');
const username = document.getElementById('username');
const email = document.getElementById('email');
const password = document.getElementById('password');
const msgBox = document.getElementById('message');

btn.addEventListener('click', async () => {
  if (username.value.length < 3) {
    showMessage(msgBox, 'Username should be at least 3 characters', 'error');
    return;
  }
  
  if (email.value.length < 3 || !email.value.includes('@') || !email.value.includes('.')) {
    showMessage(msgBox, 'Enter a valid email', 'error');
    return;
  }

  if (password.value.length < 8) {
    showMessage(msgBox, 'Password should be at least 8 characters', 'error');
    return;
  }

  btn.disabled = true;
  btn.textContent = 'Creating account...';

  try {
    const res = await dataSubmit(
      { username: username.value, email: email.value, password: password.value },
      `${API_URL}/register`
    );

    if (!res.success) {
      showMessage(msgBox, res.data?.msg || 'Registration failed', 'error');
      return;
    }

    showMessage(msgBox, res.data.msg);
    setTimeout(() => window.location.href = 'login.html', 1500);
  } catch (err) {
    showMessage(msgBox, 'An unexpected error occurred', 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Submit';
  }
});
