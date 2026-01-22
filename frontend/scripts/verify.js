import { API_URL } from './config.js';

// Get all state elements
const loading = document.getElementById('loading');
const success = document.getElementById('success');
const expired = document.getElementById('expired');
const invalid = document.getElementById('invalid');
const error = document.getElementById('error');
const errorMessage = document.getElementById('error-message');

// Function to show state
function showState(state) {
  // Hide all states
  loading.style.display = 'none';
  success.style.display = 'none';
  expired.style.display = 'none';
  invalid.style.display = 'none';
  error.style.display = 'none';

  // Show the requested state
  const element = document.getElementById(state);
  if (element) {
    element.style.display = 'block';
  }

  // Update body class for background color
  document.body.className = state;
}

// Get URL parameters
const params = new URLSearchParams(window.location.search);
const token_id = params.get("token_id");
const token = params.get("token");

// Check if parameters exist
if (!token || !token_id) {
  showState('error');
  if (errorMessage) errorMessage.textContent = 'Missing verification parameters.';
}

// Prepare data
const details = {
  token_id: token_id,
  token: token
};

console.log(details)

// Set initial state
showState('loading');

// Start verification
verifyEmail(details);

async function verifyEmail(details) {
  try {
    // Define headers
    const headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };
    
    console.log('Sending verification request:', details);
    
    const res = await fetch(`${API_URL}/verify-email`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(details)
    });
    
    console.log('Response status:', res.status);
    
    // Check if response is JSON
    const contentType = res.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      const text = await res.text();
      console.error('Non-JSON response:', text.substring(0, 200));
      throw new Error('Server returned non-JSON response');
    }
    
    const data = await res.json();
    console.log('Response data:', data);

    if (data.success) {
      showState('success');
    } else {
      if (data.error === 'expired') {
        showState('expired');
      } else if (data.error === 'invalid') {
        showState('invalid');
      } else {
        showState('error');
        if (errorMessage) errorMessage.textContent = data.msg || 'Verification failed.';
      }
    }
  } catch (err) {
    console.error('Verification error:', err);
    showState('error');
    if (errorMessage) {
      if (err.name === 'TypeError' && err.message.includes('Failed to fetch')) {
        errorMessage.textContent = 'Cannot connect to server. Check your connection.';
      } else {
        errorMessage.textContent = 'Network error. Please try again later.';
      }
    }
  }
}