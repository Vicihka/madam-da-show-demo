// Notes character counter
        const notesInput = document.getElementById('notes');
        const notesCount = document.getElementById('notes-count');
        if (notesInput && notesCount) {
            notesInput.addEventListener('input', function() {
                notesCount.textContent = this.value.length;
            });
        }
        
        // Auto-uppercase and format order number
        const orderInput = document.getElementById('order_number');
        if (orderInput) {
            orderInput.addEventListener('input', function(e) {
                let value = e.target.value.toUpperCase().replace(/[^MD0-9]/g, '');
                // Ensure it starts with MD
                if (value.length > 0 && !value.startsWith('MD')) {
                    if (value.startsWith('M')) {
                        value = 'M' + value.substring(1).replace(/[^D0-9]/g, '');
                        if (!value.startsWith('MD')) {
                            value = 'MD' + value.substring(1).replace(/[^0-9]/g, '');
                        }
                    } else {
                        value = 'MD' + value.replace(/[^0-9]/g, '');
                    }
                }
                e.target.value = value;
                
                // Show error if invalid format
                const errorDiv = document.getElementById('error-message');
                if (value.length > 0 && (!value.startsWith('MD') || value.length < 3)) {
                    errorDiv.style.display = 'block';
                    errorDiv.className = 'error-message';
                    errorDiv.textContent = '⚠️ Invalid format. Must start with MD followed by numbers';
                } else {
                    errorDiv.style.display = 'none';
                }
            });
            
            // Auto-submit if valid order number (MD + 5+ digits)
            orderInput.addEventListener('input', function(e) {
                const value = e.target.value.trim().toUpperCase();
                if (value.match(/^MD\d{5,}$/)) {
                    // Auto-submit after short delay
                    clearTimeout(window.autoSubmitTimeout);
                    window.autoSubmitTimeout = setTimeout(() => {
                        if (value === e.target.value.trim().toUpperCase()) {
                            document.getElementById('order-form').submit();
                        }
                    }, 800);
                }
            });
        }
        
        // QR Code Scanner using html5-qrcode library
        let html5QrcodeScanner = null;
        
        function startQRScan() {
            // Check if library is loaded
            if (typeof Html5Qrcode === 'undefined') {
                alert('QR code scanner library is loading. Please wait a moment and try again.');
                return;
            }
            
            // Create modal for QR scanner
            const modal = document.createElement('div');
            modal.id = 'qr-scanner-modal';
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.95);
                z-index: 10000;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 20px;
            `;
            
            modal.innerHTML = `
                <div style="background: white; border-radius: 16px; padding: 25px; max-width: 100%; width: 100%; max-width: 500px; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.3);">
                    <h3 style="margin-bottom: 15px; color: #333; font-size: 22px;">📷 Scan QR Code</h3>
                    <div id="qr-reader" style="width: 100%; margin: 0 auto 15px; border-radius: 12px; overflow: hidden;"></div>
                    <p style="color: #666; font-size: 14px; margin-bottom: 15px;">Point camera at QR code</p>
                    <button onclick="stopQRScan()" style="padding: 12px 24px; background: #dc3545; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 16px; width: 100%;">
                        Cancel
                    </button>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            // Initialize scanner
            const qrReaderElement = document.getElementById('qr-reader');
            html5QrcodeScanner = new Html5Qrcode(qrReaderElement.id);
            
            // Start scanning
            html5QrcodeScanner.start(
                { facingMode: "environment" }, // Use back camera on mobile
                {
                    fps: 10,
                    qrbox: { width: 250, height: 250 },
                    aspectRatio: 1.0
                },
                function(decodedText, decodedResult) {
                    // Successfully scanned QR code
                    handleQRCodeScanned(decodedText);
                    stopQRScan();
                },
                function(errorMessage) {
                    // Ignore scanning errors (just keep scanning)
                }
            ).catch(function(err) {
                console.error("Error starting QR scanner:", err);
                
                // Remove modal
                const modal = document.getElementById('qr-scanner-modal');
                if (modal) {
                    modal.remove();
                }
                
                // Show user-friendly error message based on error type
                let errorMsg = 'Could not access camera. ';
                if (err.name === 'NotAllowedError' || err.message.includes('Permission denied') || err.message.includes('NotAllowedError')) {
                    errorMsg += 'Please allow camera access in your browser settings and try again.';
                } else if (err.name === 'NotFoundError' || err.message.includes('no camera') || err.message.includes('NotFoundError')) {
                    errorMsg += 'No camera found on this device.';
                } else if (err.message.includes('Permissions policy')) {
                    errorMsg += 'Camera access is blocked by browser policy. Please contact administrator.';
                } else {
                    errorMsg += 'Please check camera permissions and try again, or enter order number manually.';
                }
                
                alert(errorMsg);
                
                // Clean up scanner
                if (html5QrcodeScanner) {
                    try {
                        html5QrcodeScanner.stop().catch(() => {
                            // Ignore cleanup errors
                        });
                    } catch (e) {
                        // Ignore cleanup errors
                    }
                    html5QrcodeScanner = null;
                }
            });
        }
        
        function handleQRCodeScanned(decodedText) {
            console.log("QR Code scanned:", decodedText);
            
            // Extract order number from URL or direct text
            let orderNumber = null;
            
            // Check if it's a URL containing /cod/confirm/
            if (decodedText.includes('/cod/confirm/')) {
                // Extract order number from URL like: http://host/cod/confirm/MD00001/
                const match = decodedText.match(/\/cod\/confirm\/([^\/]+)/);
                if (match) {
                    orderNumber = match[1].toUpperCase();
                }
            } else if (decodedText.match(/^MD\d+$/i)) {
                // Direct order number format
                orderNumber = decodedText.toUpperCase();
            } else {
                // Try to extract any MD followed by numbers
                const match = decodedText.match(/MD\d+/i);
                if (match) {
                    orderNumber = match[0].toUpperCase();
                }
            }
            
            if (orderNumber) {
                // Auto-confirm payment when QR code is scanned
                console.log('QR Code scanned, auto-confirming payment for:', orderNumber);
                
                // Call API to auto-confirm payment
                fetch('/api/cod/confirm/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        order_number: orderNumber,
                        driver_name: 'QR Scanner',
                        notes: 'Payment confirmed via QR code scan'
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Show success message
                        stopQRScan();
                        
                        // Redirect to confirmation page to show success
                        window.location.href = `/cod/confirm/${orderNumber}/?auto_confirmed=true`;
                    } else {
                        // If auto-confirm fails, redirect to manual confirmation page
                        console.error('Auto-confirm failed:', data.message);
                        stopQRScan();
                        window.location.href = `/cod/confirm/${orderNumber}/`;
                    }
                })
                .catch(error => {
                    console.error('Error auto-confirming payment:', error);
                    // If API call fails, redirect to manual confirmation page
                    stopQRScan();
                    window.location.href = `/cod/confirm/${orderNumber}/`;
                });
            } else {
                alert('Could not find order number in QR code. Please enter manually.');
                stopQRScan();
            }
        }
        
        function stopQRScan() {
            if (html5QrcodeScanner) {
                html5QrcodeScanner.stop().then(() => {
                    html5QrcodeScanner.clear();
                    html5QrcodeScanner = null;
                }).catch((err) => {
                    // Ignore "scanner is not running" errors - this is normal if scanner failed to start
                    if (!err.message || (!err.message.includes('not running') && !err.message.includes('not started'))) {
                        console.error("Error stopping scanner:", err);
                    }
                    // Clean up anyway
                    try {
                        html5QrcodeScanner.clear();
                    } catch (e) {
                        // Ignore cleanup errors
                    }
                    html5QrcodeScanner = null;
                });
            }
            
            const modal = document.getElementById('qr-scanner-modal');
            if (modal) {
                modal.remove();
            }
        }
        
        // Handle form submission
        const confirmForm = document.getElementById('confirm-form');
        if (confirmForm) {
            confirmForm.addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const btn = document.getElementById('confirm-btn');
                const originalText = btn.textContent;
                btn.disabled = true;
                btn.textContent = '⏳ Processing...';
                btn.style.opacity = '0.7';
                
                const formData = new FormData(confirmForm);
                
                try {
                    const response = await fetch(window.location.href, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        // Show success animation
                        document.getElementById('message').innerHTML = 
                            `<div class="success-message" style="animation: slideIn 0.5s;">
                                <div style="font-size: 48px; margin-bottom: 10px;">✅</div>
                                <div style="font-size: 20px; font-weight: 700; margin-bottom: 5px;">Payment Confirmed!</div>
                                <div>${data.message}</div>
                            </div>`;
                        confirmForm.style.display = 'none';
                        
                        // Show success details
                        const orderInfo = document.querySelector('.order-info');
                        if (orderInfo) {
                            orderInfo.innerHTML = `
                                <div style="text-align: center; padding: 30px;">
                                    <div style="font-size: 64px; margin-bottom: 15px;">✅</div>
                                    <div style="font-size: 24px; font-weight: 700; color: #22c55e; margin-bottom: 10px;">Payment Confirmed</div>
                                    <div style="color: #666; margin-bottom: 20px;">Order #${data.order.number}</div>
                                    <div style="font-size: 32px; color: #22c55e; font-weight: 700;">$${data.order.total}</div>
                                </div>
                            `;
                        }
                        
                        // Redirect after 3 seconds
                        setTimeout(() => {
                            window.location.href = window.location.pathname;
                        }, 3000);
                    } else {
                        document.getElementById('message').innerHTML = 
                            `<div class="error-message" style="animation: shake 0.5s;">
                                <div style="font-size: 24px; margin-bottom: 5px;">❌</div>
                                <div>${data.message}</div>
                            </div>`;
                        btn.disabled = false;
                        btn.textContent = originalText;
                        btn.style.opacity = '1';
                    }
                } catch (error) {
                    document.getElementById('message').innerHTML = 
                        `<div class="error-message">
                            <div style="font-size: 24px; margin-bottom: 5px;">❌</div>
                            <div>Error: ${error.message}</div>
                        </div>`;
                    btn.disabled = false;
                    btn.textContent = originalText;
                    btn.style.opacity = '1';
                }
            });
        }
        
        // Add shake animation for errors
        const style = document.createElement('style');
        style.textContent = `
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-10px); }
                75% { transform: translateX(10px); }
            }
        `;
        document.head.appendChild(style);
        
        // ========== EXPOSE FUNCTIONS TO GLOBAL SCOPE ==========
        // Required for onclick handlers in HTML
        window.startQRScan = startQRScan;
        window.stopQRScan = stopQRScan;