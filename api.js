// API Configuration
const API_CONFIG = {
    BASE_URL: 'https://xxxxx.trycloudflare.com', // Replace with your Cloudflare tunnel URL
    TIMEOUT: 10000
};

// API Status
let isBackendOnline = false;

// Test backend connectivity
async function testAPI() {
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/health`, {
            method: 'GET',
            signal: AbortSignal.timeout(API_CONFIG.TIMEOUT)
        });
        isBackendOnline = response.ok;
        return response.ok;
    } catch (error) {
        console.error('Backend offline:', error);
        isBackendOnline = false;
        return false;
    }
}

// Get video feed URL
function getVideoFeedURL(cameraId = 0) {
    return `${API_CONFIG.BASE_URL}/video_feed?camera=${cameraId}`;
}

// Get accumulated text
async function getText() {
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/get_text`, {
            method: 'GET',
            signal: AbortSignal.timeout(API_CONFIG.TIMEOUT)
        });
        if (!response.ok) throw new Error('Failed to get text');
        return await response.json();
    } catch (error) {
        console.error('Error getting text:', error);
        throw error;
    }
}

// Clear accumulated text
async function clearText() {
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/clear_text`, {
            method: 'POST',
            signal: AbortSignal.timeout(API_CONFIG.TIMEOUT)
        });
        if (!response.ok) throw new Error('Failed to clear text');
        return await response.json();
    } catch (error) {
        console.error('Error clearing text:', error);
        throw error;
    }
}

// Backspace last character
async function backspaceText() {
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/backspace`, {
            method: 'POST',
            signal: AbortSignal.timeout(API_CONFIG.TIMEOUT)
        });
        if (!response.ok) throw new Error('Failed to backspace');
        return await response.json();
    } catch (error) {
        console.error('Error backspacing:', error);
        throw error;
    }
}

// Show error notification
function showError(message) {
    const errorDiv = document.getElementById('errorNotification');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    }
}

// Show loading state
function setLoading(isLoading) {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.display = isLoading ? 'block' : 'none';
    }
}

// Update backend URL
function setBackendURL(url) {
    API_CONFIG.BASE_URL = url.replace(/\/$/, ''); // Remove trailing slash
    localStorage.setItem('backend_url', API_CONFIG.BASE_URL);
}

// Load backend URL from storage
function loadBackendURL() {
    const saved = localStorage.getItem('backend_url');
    if (saved) {
        API_CONFIG.BASE_URL = saved;
    }
    return API_CONFIG.BASE_URL;
}
