// Authentication UI and logic
import { loginUser, registerUser, logoutUser, onAuthChange, loginWithGoogle } from './firebase-config.js';

class AuthManager {
    constructor() {
        this.currentUser = null;
        this.init();
    }

    init() {
        // Listen for auth state changes
        onAuthChange((user) => {
            this.currentUser = user;
            this.updateUI();
        });

        // Setup event listeners
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Login form
        document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            
            const result = await loginUser(email, password);
            if (result.success) {
                this.showMessage('✅ Login successful!', 'success');
            } else {
                this.showMessage(`❌ Login failed: ${result.error}`, 'error');
            }
        });

        // Register form
        document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('registerEmail').value;
            const password = document.getElementById('registerPassword').value;
            
            const result = await registerUser(email, password);
            if (result.success) {
                this.showMessage('✅ Registration successful!', 'success');
            } else {
                this.showMessage(`❌ Registration failed: ${result.error}`, 'error');
            }
        });

        // Google login button
        document.getElementById('googleLoginBtn')?.addEventListener('click', async () => {
            const result = await loginWithGoogle();
            if (result.success) {
                this.showMessage('✅ Google login successful!', 'success');
            } else {
                this.showMessage(`❌ Google login failed: ${result.error}`, 'error');
            }
        });

        // Logout button
        document.getElementById('logoutBtn')?.addEventListener('click', async () => {
            const result = await logoutUser();
            if (result.success) {
                this.showMessage('✅ Logged out successfully!', 'success');
            }
        });

        // Toggle between login/register
        document.getElementById('showRegister')?.addEventListener('click', () => {
            document.getElementById('loginSection').style.display = 'none';
            document.getElementById('registerSection').style.display = 'block';
        });

        document.getElementById('showLogin')?.addEventListener('click', () => {
            document.getElementById('registerSection').style.display = 'none';
            document.getElementById('loginSection').style.display = 'block';
        });
    }

    updateUI() {
        const authContainer = document.getElementById('authContainer');
        const appContainer = document.getElementById('appContainer');
        const userInfo = document.getElementById('userInfo');

        if (this.currentUser) {
            // User is logged in
            authContainer.style.display = 'none';
            appContainer.style.display = 'block';
            userInfo.innerHTML = `
                <span>Welcome, ${this.currentUser.email}</span>
                <button id="logoutBtn" class="btn btn-secondary">Logout</button>
            `;
            // Re-attach logout listener
            document.getElementById('logoutBtn').addEventListener('click', async () => {
                await logoutUser();
            });
        } else {
            // User is not logged in
            authContainer.style.display = 'block';
            appContainer.style.display = 'none';
            userInfo.innerHTML = '';
        }
    }

    showMessage(message, type) {
        const messageDiv = document.getElementById('authMessage');
        messageDiv.innerHTML = message;
        messageDiv.className = `message ${type}`;
        messageDiv.style.display = 'block';
        
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    }
}

// Initialize auth manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AuthManager();
});
