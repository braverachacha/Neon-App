import { dataSubmit } from './dataFetch.js';
import { showMessage } from './uiMessage.js';
import { API_URL } from './config.js';
import { passwordCheck } from './passwordCheck.js';

const btn = document.querySelector('.js-submit-button');
const username = document.getElementById('username');
const email = document.getElementById('email');
const password = document.getElementById('password');
const msgBox = document.getElementById('message');

btn.addEventListener('click', async () => {
  // Username validation
  if (username.value.length < 3) {
    showMessage(msgBox, 'Username should be at least 3 characters', 'error');
    return;
  }

  // Email validation
  if (email.value.length < 3 || !email.value.includes('@') || !email.value.includes('.')) {
    showMessage(msgBox, 'Enter a valid email', 'error');
    return;
  }

  // Password validation using passwordCheck
  const isPasswordValid = passwordCheck(password.value, msgBox);
  if (!isPasswordValid) return;

  // Disable button while submitting
  btn.disabled = true;
  btn.textContent = 'Creating account...';

  try {
    const res = await dataSubmit(
      { username: username.value, email: email.value, password: password.value },
      `${API_URL}/register`
    );

    console.log(res); // debug response

    if (!res.success) {
      showMessage(msgBox, res.data?.msg || 'Registration failed', 'error');
      return;
    }

    showMessage(msgBox, res.data?.msg || 'Account created successfully!');
    setTimeout(() => window.location.href = 'login.html', 1500);
  } catch (err) {
    showMessage(msgBox, 'An unexpected error occurred', 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Submit';
  }
});