import { API_URL } from './config.js';

// Minimal with verification
(() => {
    const ping = async () => {
        try {
            const response = await fetch(`${API_URL}/ping`, {
                method: 'GET',
                signal: AbortSignal.timeout(5000)
            });

            if (response.ok) {
                const data = await response.json();
                console.log('✓ Backend alive:', data.msg || data.status);
                return true;
            }
        } catch {
          // Chillax
        }
        return false;
    };

    setTimeout(ping, 3000);
    setInterval(ping, 300000);
})();
