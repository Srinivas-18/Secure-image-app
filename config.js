// Configuration for deployment
const CONFIG = {
    // Backend API URLs for different environments
    API_URLS: {
        development: 'http://localhost:5000',
        production: 'https://your-backend-url.onrender.com' // Replace with your actual Render URL
    },
    
    // Get current environment
    getEnvironment() {
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return 'development';
        }
        return 'production';
    },
    
    // Get API URL for current environment
    getApiUrl() {
        return this.API_URLS[this.getEnvironment()];
    }
};

// Make config available globally
window.APP_CONFIG = CONFIG;
