export const dataSubmit = async (details, url, token = null) => {
  try {
    const headers = { 'Content-Type': 'application/json' };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const res = await fetch(url, {
      method: 'POST',
      headers,
      body: JSON.stringify(details)
    });

    const data = await res.json();

    if (!res.ok) {
      return { success: false, data };
    }

    return { success: true, data };
  } catch (err) {
    return { 
      success: false, 
      data: { msg: 'Network error - please check your connection' } 
    };
  }
};