(async () => {
  const token = localStorage.getItem('access_token');

  if (!token) {
    window.location.replace('login.html');
    return;
  }

  document.body.style.visibility = 'hidden';

  try {
    const res = await fetch('http://127.0.0.1:3000/protected-route', {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!res.ok) {
      localStorage.clear();
      window.location.replace('login.html');
    } else {
      document.body.style.visibility = 'visible';
    }
  } catch (err) {
    localStorage.clear();
    window.location.replace('login.html');
  }
})();