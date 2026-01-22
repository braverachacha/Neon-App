import { dataSubmit } from './dataFetch.js';
import { showMessage } from './uiMessage.js';
import { API_URL } from './config.js';
import { passwordCheck } from './passwordCheck.js'

const sendBtn = document.getElementById('send-reset-link');
const emailInput = document.getElementById('reset-email');
const msg = document.getElementById('reset-msg');
const newPassSection = document.getElementById('new-pass-section');
const resetSubmit = document.getElementById('reset-submit');
const newPassInput = document.getElementById('new-pass');
const resetResult = document.getElementById('reset-result');

const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get('token');
const msgBox = document.getElementById('reset-result');
console.log(msgBox);

// If token exists in URL, show password reset section
if (token) {
  newPassSection.style.display = 'block';
  emailInput.parentElement.style.display = 'none';
  sendBtn.style.display = 'none';
}

// Send reset link
sendBtn.addEventListener('click', async () => {
  const email = emailInput.value;

  if (!email) {
    showMessage(msg, 'Please enter your email address', 'error');
    return;
  }

  sendBtn.disabled = true;
  sendBtn.textContent = 'Sending...';

  try {
    const res = await dataSubmit(
      { email },
      `${API_URL}/forgot-password`
    );

    if (!res.success) {
      showMessage(msg, res.data?.msg || 'Failed to send reset link', 'error');
      return;
    }

    showMessage(msg, res.data.msg);
    emailInput.value = '';
  } catch (err) {
    showMessage(msg, 'Network error - please try again', 'error');
  } finally {
    sendBtn.disabled = false;
    sendBtn.textContent = 'Send Reset Link';
  }
});

// Reset password with token
resetSubmit.addEventListener('click', async () => {
  const password = newPassInput.value;
  
  // check password strength
  const isPasswordVerified = passwordCheck(password, msgBox);
  if (!isPasswordVerified) {
    return
  }


  resetSubmit.disabled = true;
  resetSubmit.textContent = 'Resetting...';

  try {
    const res = await dataSubmit(
      { token, password },
      `${API_URL}/reset-password`
    );

    if (!res.success) {
      showMessage(resetResult, res.data?.msg || 'Failed to reset password', 'error');
      return;
    }

    showMessage(resetResult, res.data.msg);
    newPassInput.value = '';

    setTimeout(() => window.location.replace('login.html'), 2000);
  } catch (err) {
    showMessage(resetResult, 'Network error - please try again', 'error');
  } finally {
    resetSubmit.disabled = false;
    resetSubmit.textContent = 'Reset Password';
  }
});
