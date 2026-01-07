// Get all state elements
const loading = document.getElementById('loading');
const success = document.getElementById('success');
const expired = document.getElementById('expired');
const invalid = document.getElementById('invalid');
const error = document.getElementById('error');
const errorMessage = document.getElementById('error-message');

// Get token from URL
const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get('token');

// Set initial state
document.body.className = 'loading';

if (!token) {
  showState('error');
  errorMessage.textContent = 'No verification token found in URL.';
} else {
  verifyEmail(token);
}

async function verifyEmail(token) {
  try {
    const res = await fetch(`http://127.0.0.1:3000/verify-email/${token}`);
    const data = await res.json();

    if (data.success) {
      showState('success');
      removeTokenFromURL(); // remove token from URL
      setTimeout(() => window.location.replace('login.html'), 2000);
    } else {
      if (data.error === 'expired') {
        showState('expired');
      } else if (data.error === 'invalid') {
        showState('invalid');
      } else {
        showState('error');
        errorMessage.textContent = data.msg || 'Verification failed.';
        error.style.display = 'block';
      }
    }
  } catch (err) {
    showState('error');
    errorMessage.textContent = 'Network error. Please try again later.';
    error.style.display = 'block';
  }
}

function showState(state) {
  // Hide all states
  loading.style.display = 'none';
  success.style.display = 'none';
  expired.style.display = 'none';
  invalid.style.display = 'none';
  error.style.display = 'none';

  // Show the requested state
  document.getElementById(state).style.display = 'block';
  
  // Update body class for background color
  document.body.className = state;
}