// DOM Elements
const encryptForm = document.getElementById('encryptForm');
const decryptForm = document.getElementById('decryptForm');
const encryptPin = document.getElementById('encryptPin');
const pinStrength = document.getElementById('pinStrength');
const imageFile = document.getElementById('imageFile');
const encryptedFile = document.getElementById('encryptedFile');
const imageInfo = document.getElementById('imageInfo');
const encryptedInfo = document.getElementById('encryptedInfo');
const encryptResult = document.getElementById('encryptResult');
const decryptResult = document.getElementById('decryptResult');
const statsSection = document.getElementById('statsSection');
const loadingSpinner = document.getElementById('loadingSpinner');
const viewLogsBtn = document.getElementById('viewLogsBtn');
const logModal = document.getElementById('logModal');
const logDisplayModal = document.getElementById('logDisplayModal');
const logAuthForm = document.getElementById('logAuthForm');

// Utility Functions
function showLoading() {
    loadingSpinner.style.display = 'flex';
}

function hideLoading() {
    loadingSpinner.style.display = 'none';
}

function showResult(element, message, isSuccess = true) {
    element.innerHTML = message;
    element.className = `result-section ${isSuccess ? 'success' : 'error'}`;
    element.style.display = 'block';
}

function hideResult(element) {
    element.style.display = 'none';
}

function formatFileSize(bytes) {
    return (bytes / 1024).toFixed(2);
}

// PIN Strength Checker
encryptPin.addEventListener('input', async function() {
    const pin = this.value;
    if (pin.length === 0) {
        pinStrength.style.display = 'none';
        return;
    }

    try {
        const response = await fetch('/check_pin_strength', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ pin: pin })
        });

        const data = await response.json();
        pinStrength.textContent = `PIN Strength: ${data.strength}`;
        pinStrength.className = `pin-strength ${data.strength.toLowerCase()}`;
        pinStrength.style.display = 'block';
    } catch (error) {
        console.error('Error checking PIN strength:', error);
    }
});

// File Info Display
imageFile.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        imageInfo.innerHTML = `
            <strong>Selected:</strong> ${file.name}<br>
            <strong>Size:</strong> ${formatFileSize(file.size)} KB<br>
            <strong>Type:</strong> ${file.type}
        `;
        imageInfo.style.display = 'block';
    } else {
        imageInfo.style.display = 'none';
    }
});

encryptedFile.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        encryptedInfo.innerHTML = `
            <strong>Selected:</strong> ${file.name}<br>
            <strong>Size:</strong> ${formatFileSize(file.size)} KB
        `;
        encryptedInfo.style.display = 'block';
    } else {
        encryptedInfo.style.display = 'none';
    }
});

// Meta file info display
const metaFile = document.getElementById('metaFile');
const metaInfo = document.getElementById('metaInfo');

metaFile.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        metaInfo.innerHTML = `
            <strong>Selected:</strong> ${file.name}<br>
            <strong>Size:</strong> ${formatFileSize(file.size)} KB<br>
            <span style="color: green;">✅ Integrity check will be performed</span>
        `;
        metaInfo.style.display = 'block';
    } else {
        metaInfo.style.display = 'none';
    }
});

// Encryption Form Handler
encryptForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const file = imageFile.files[0];
    const pin = document.getElementById('encryptPin').value;

    if (!file || !pin) {
        showResult(encryptResult, '❌ Please select an image and enter a PIN.', false);
        return;
    }

    showLoading();
    hideResult(encryptResult);

    try {
        const response = await fetch('/encrypt', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        hideLoading();

        if (data.success) {
            showResult(encryptResult, `
                ✅ <strong>Encryption Successful!</strong><br>
                📁 Encrypted file: ${data.encrypted_filename}<br>
                🔑 Hash file: ${data.meta_filename}<br>
                <div style="margin-top: 15px;">
                    <a href="/download/${data.encrypted_filename}" class="download-link">📥 Download Encrypted File</a>
                    <a href="/download/${data.meta_filename}" class="download-link" style="margin-left: 10px;">📄 Download Hash File</a>
                </div>
                <div style="margin-top: 10px; padding: 10px; background: #e6f3ff; border-radius: 5px; font-size: 14px;">
                    💡 <strong>Important:</strong> Keep both files together for decryption and integrity verification.<br>
                    🔐 <strong>Security:</strong> Don't share your PIN with anyone you don't trust completely.
                </div>
            `);
            
            // Show statistics
            displayStats(data.stats, 'encrypt');
        } else {
            showResult(encryptResult, `❌ Encryption failed: ${data.error}`, false);
        }
    } catch (error) {
        hideLoading();
        showResult(encryptResult, `❌ Error: ${error.message}`, false);
    }
});

// Decryption Form Handler
decryptForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const file = encryptedFile.files[0];
    const pin = document.getElementById('decryptPin').value;

    if (!file || !pin) {
        showResult(decryptResult, '❌ Please select an encrypted file and enter the PIN.', false);
        return;
    }

    showLoading();
    hideResult(decryptResult);

    try {
        const response = await fetch('/decrypt', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        hideLoading();

        if (data.success) {
            showResult(decryptResult, `
                ✅ <strong>Decryption Successful!</strong><br>
                🖼️ Image decrypted successfully<br>
                ${data.stats.integrity_verified ? '✅ Integrity verified' : '⚠️ No integrity check'}
                <br><br>
                <img src="data:image/png;base64,${data.decrypted_image}" class="image-preview" alt="Decrypted Image">
                <br>
                <a href="/download/${data.decrypted_filename}" class="download-link">📥 Download Decrypted Image</a>
                <div style="margin-top: 10px; padding: 10px; background: #fff3cd; border-radius: 5px; font-size: 14px;">
                    🗑️ <strong>Note:</strong> Encrypted files (.enc and .meta) have been automatically deleted.
                </div>
            `);
            
            // Show statistics
            displayStats(data.stats, 'decrypt');
        } else {
            showResult(decryptResult, `❌ Decryption failed: ${data.error}`, false);
        }
    } catch (error) {
        hideLoading();
        showResult(decryptResult, `❌ Error: ${error.message}`, false);
    }
});

// Display Statistics
function displayStats(stats, operation) {
    document.getElementById('entropyBefore').textContent = stats.entropy_before.toFixed(4);
    document.getElementById('entropyAfter').textContent = stats.entropy_after.toFixed(4);
    document.getElementById('sizeBefore').textContent = stats.size_before;
    document.getElementById('sizeAfter').textContent = stats.size_after;
    
    statsSection.style.display = 'block';
    statsSection.scrollIntoView({ behavior: 'smooth' });
}

// Log Viewer Functionality
viewLogsBtn.addEventListener('click', function() {
    logModal.style.display = 'block';
});

logAuthForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const username = document.getElementById('logUsername').value;
    const password = document.getElementById('logPassword').value;

    try {
        const response = await fetch('/authenticate_logs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (data.success) {
            logModal.style.display = 'none';
            await loadAndDisplayLogs();
        } else {
            alert('❌ Invalid credentials');
        }
    } catch (error) {
        alert('❌ Authentication error');
    }
});

async function loadAndDisplayLogs() {
    try {
        const response = await fetch('/get_logs');
        const data = await response.json();

        if (data.logs) {
            displayLogs(data.logs);
            logDisplayModal.style.display = 'block';
        } else {
            alert('❌ Failed to load logs');
        }
    } catch (error) {
        alert('❌ Error loading logs');
    }
}

function displayLogs(logs) {
    const logDisplay = document.getElementById('logDisplay');
    
    if (logs.length === 0) {
        logDisplay.innerHTML = '<p>No logs available.</p>';
        return;
    }

    let html = '<table class="log-table"><thead><tr><th>Timestamp</th><th>Event</th></tr></thead><tbody>';
    logs.forEach(row => {
        html += `<tr><td>${row[0]}</td><td>${row[1]}</td></tr>`;
    });
    html += '</tbody></table>';
    logDisplay.innerHTML = html;
}

// Modal Close Handlers
document.querySelectorAll('.close').forEach(closeBtn => {
    closeBtn.addEventListener('click', function() {
        this.closest('.modal').style.display = 'none';
    });
});

window.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        e.target.style.display = 'none';
    }
});

// Form Reset on Success
function resetForm(formId) {
    document.getElementById(formId).reset();
    if (formId === 'encryptForm') {
        imageInfo.style.display = 'none';
        pinStrength.style.display = 'none';
    } else {
        encryptedInfo.style.display = 'none';
    }
}
