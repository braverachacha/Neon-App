// API Configuration
export const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://127.0.0.1:3000'  // Development
  : 'https://your-backend.onrender.com';  // Production (update this after deploying to Render)
