// Minimal with verification
(() => {
    const BACKEND_URL = 'http://127.0.0.1:3000/ping';
    
    const ping = async () => {
        try {
            const response = await fetch(`${BACKEND_URL}`, {
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