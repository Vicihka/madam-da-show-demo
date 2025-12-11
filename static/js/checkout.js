// ========== PERFORMANCE OPTIMIZATIONS ==========
        // DOM Query Caching - Cache frequently used elements
        const DOMCache = {
            get checkoutItems() { return document.getElementById('checkout-items'); },
            get summaryItems() { return document.getElementById('summary-items'); },
            get summaryTotal() { return document.getElementById('summary-total'); },
            get purchaseBtn() { return document.getElementById('purchase-btn'); },
            get headerBadge() { return document.getElementById('header-badge'); },
            get checkoutForm() { return document.getElementById('checkout-form'); },
            get paymentModal() { return document.getElementById('payment-modal'); },
            get modalBody() { return document.getElementById('modal-body'); },
            get buyerName() { return document.getElementById('buyer-name'); },
            get buyerPhone() { return document.getElementById('buyer-phone'); },
            get deliveryAddress() { return document.getElementById('delivery-address'); },
            get deliveryProvince() { return document.getElementById('delivery-province'); },
            get promoCode() { return document.getElementById('promo-code'); },
            get promoMessage() { return document.getElementById('promo-message'); },
            get promoApplyBtn() { return document.getElementById('promo-apply-btn'); }
        };
        
        // Debounce utility function
        function debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }
        
        // Throttle utility function
        function throttle(func, limit) {
            let inThrottle;
            return function(...args) {
                if (!inThrottle) {
                    func.apply(this, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        }
        
        // ========== TOAST NOTIFICATION SYSTEM ==========
        function showToast(message, type = 'info', duration = 3000) {
            // Remove existing toasts
            const existingToasts = document.querySelectorAll('.toast-notification');
            existingToasts.forEach(toast => toast.remove());
            
            const toast = document.createElement('div');
            toast.className = 'toast-notification';
            const bgColor = type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : type === 'warning' ? '#f59e0b' : '#3b82f6';
            toast.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: ${bgColor};
                color: white;
                padding: 14px 20px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                z-index: 10000;
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 14px;
                font-weight: 500;
                max-width: 400px;
                animation: slideInRight 0.3s ease-out;
                cursor: pointer;
            `;
            
            const icon = type === 'error' ? '❌' : type === 'success' ? '✅' : type === 'warning' ? '⚠️' : 'ℹ️';
            toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
            
            document.body.appendChild(toast);
            
            // Auto-remove after duration
            setTimeout(() => {
                toast.style.animation = 'slideOutRight 0.3s ease-out';
                setTimeout(() => toast.remove(), 300);
            }, duration);
            
            // Click to dismiss
            toast.addEventListener('click', () => {
                toast.style.animation = 'slideOutRight 0.3s ease-out';
                setTimeout(() => toast.remove(), 300);
            });
        }
        
        // Add animation styles
        if (!document.getElementById('toast-animations')) {
            const style = document.createElement('style');
            style.id = 'toast-animations';
            style.textContent = `
                @keyframes slideInRight {
                    from {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
                @keyframes slideOutRight {
                    from {
                        transform: translateX(0);
                        opacity: 1;
                    }
                    to {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
        
        // Load cart from localStorage on page load to ensure sync
        let cart = [];
        try {
            const savedCart = localStorage.getItem('madamda_cart');
            if (savedCart) {
                cart = JSON.parse(savedCart) || [];
            } else {
                // Try to load from sessionStorage backup
                try {
                    const backupCart = sessionStorage.getItem('madamda_cart_backup');
                    if (backupCart) {
                        cart = JSON.parse(backupCart) || [];
                        // Restore to localStorage
                        localStorage.setItem('madamda_cart', JSON.stringify(cart));
                    }
                } catch (e) {
                    cart = [];
                }
            }
        } catch (e) {
            console.error('Error loading cart from localStorage:', e);
            cart = [];
        }
        
        // Clean up any invalid cart data
        if (!Array.isArray(cart)) {
            cart = [];
            try {
                localStorage.setItem('madamda_cart', '[]');
            } catch (e) {
                console.error('Error clearing invalid cart:', e);
            }
        }
        
        // Helper function to save cart with backup (optimized)
        function saveCart() {
            try {
                localStorage.setItem('madamda_cart', JSON.stringify(cart));
                // Also save to sessionStorage as backup
                try {
                    sessionStorage.setItem('madamda_cart_backup', JSON.stringify(cart));
                } catch (e) {
                    console.warn('sessionStorage not available:', e);
                }
            } catch (e) {
                console.error('Error saving cart to localStorage:', e);
                // Try to save to sessionStorage as fallback
                try {
                    sessionStorage.setItem('madamda_cart_backup', JSON.stringify(cart));
                } catch (e2) {
                    console.error('Error saving cart to sessionStorage:', e2);
                }
            }
        }
        
        // Debounced cart save to reduce localStorage writes (saves every 500ms max)
        const debouncedSaveCart = debounce(saveCart, 500);
        
        // Save cart before page unload
        window.addEventListener('beforeunload', function() {
            if (cart.length > 0) {
                try {
                    saveCart();
                } catch (e) {
                    console.error('Error saving cart on page unload:', e);
                }
            }
        });
        
        // Save cart periodically (every 5 seconds) as backup
        setInterval(function() {
            if (cart.length > 0) {
                try {
                    saveCart();
                } catch (e) {
                    console.error('Error in periodic cart save:', e);
                }
            }
        }, 5000);
        
        let pollInterval;
        
        // Optimized updateCheckoutView with DOM caching and requestAnimationFrame
        function updateCheckoutView() {
            requestAnimationFrame(() => {
                const checkoutItems = DOMCache.checkoutItems;
                const summaryItems = DOMCache.summaryItems;
                const summaryTotal = DOMCache.summaryTotal;
                const purchaseBtn = DOMCache.purchaseBtn;
                const headerBadge = DOMCache.headerBadge;
                
                if (!checkoutItems || !summaryItems || !summaryTotal || !purchaseBtn) return;
            
            // Update header badge
            const totalItems = cart.reduce((sum, item) => sum + item.qty, 0);
            if (headerBadge) {
                if (totalItems > 0) {
                    headerBadge.textContent = totalItems;
                    headerBadge.classList.remove('hidden');
                } else {
                    headerBadge.classList.add('hidden');
                }
            }
            
            if (cart.length === 0) {
                checkoutItems.innerHTML = `
                    <div class="empty-cart-state">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="2.37 1.5 19.25 21" stroke-width="1.5" stroke="currentColor" class="empty-cart-icon">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"></path>
                        </svg>
                        <p class="empty-cart-text">Your cart is empty</p>
                        <p class="empty-cart-subtext">Add some products to get started!</p>
                        <a href="${API_URLS.shop}" class="empty-cart-btn">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="1.5 1.97 21 19.78" stroke-width="1.5" stroke="currentColor" style="width: 18px; height: 18px; margin-right: 8px;">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"></path>
                            </svg>
                            Continue Shopping
                        </a>
                    </div>
                `;
                summaryItems.innerHTML = '<div class="summary-item"><p class="summary-item-name">No items</p><p class="summary-item-price">$0</p></div>';
                summaryTotal.textContent = '$0';
                purchaseBtn.disabled = true;
                return;
            }
            
            const subtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
            const deliveryFee = 0;
            const discountAmount = window.promoDiscount || 0;
            // Round to 2 decimal places to avoid floating-point precision issues
            const total = Math.round(Math.max(0, subtotal + deliveryFee - discountAmount) * 100) / 100;
            
            // Render cart items
            checkoutItems.innerHTML = cart.map(item => `
                <div class="cart-item">
                    <div class="cart-item-content">
                        <img src="${item.image}" alt="${item.name}" class="cart-item-image" loading="lazy" width="112" height="112" decoding="async" fetchpriority="low">
                        <div class="cart-item-details">
                            <p class="cart-item-name">${item.name}</p>
                            <div class="qty-input-wrapper">
                                <div class="qty-buttons-inner">
                                    <button class="qty-btn" onclick="updateCartQty('${item.id}', -1)">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke-width="1.5" stroke="currentColor" style="width: 16px; height: 16px;" viewBox="0.75 8.25 22.5 7.5">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 12h-15"></path>
                                        </svg>
                                    </button>
                                    <input class="qty-input" type="number" step="1" placeholder="0" value="${item.qty}" readonly>
                                    <button class="qty-btn" onclick="updateCartQty('${item.id}', 1)">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" style="width: 16px; height: 16px;" viewBox="1 1 22 22">
                                            <path d="M5 12h14M12 5v14"></path>
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="cart-item-remove">
                        <button class="remove-btn remove-btn-desktop" onclick="removeFromCart('${item.id}')">Remove</button>
                        <button class="remove-btn remove-btn-mobile" onclick="removeFromCart('${item.id}')">Remove</button>
                    </div>
                </div>
            `).join('');
            
            // Render summary items
            summaryItems.innerHTML = cart.map(item => `
                <div class="summary-item">
                    <p class="summary-item-name">${item.name} x ${item.qty}</p>
                    <p class="summary-item-price">$${(item.price * item.qty).toFixed(2)}</p>
                </div>
            `).join('') + `
                <div class="summary-item">
                    <p class="summary-item-name">Delivery fee</p>
                    <p class="summary-item-price"><span><del class="text-muted-foreground mr-1" style="color: var(--muted-foreground); margin-right: 4px;">$1.5</del>$0</span></p>
                </div>
            `;
            
            // Update summary to show discount if applied
            if (discountAmount > 0) {
                summaryItems.innerHTML += `
                    <div class="summary-item" style="color: #10b981;">
                        <p class="summary-item-name">Discount</p>
                        <p class="summary-item-price" style="color: #10b981;">-$${discountAmount.toFixed(2)}</p>
                    </div>
                `;
            }
            
                summaryTotal.textContent = `$${total.toFixed(2)}`;
                purchaseBtn.disabled = false;
            });
        }
        
        // Promo code state
        window.promoDiscount = 0;
        window.appliedPromoCode = null;
        
        async function applyPromoCode() {
            const promoInput = DOMCache.promoCode;
            const promoMessage = DOMCache.promoMessage;
            const applyBtn = DOMCache.promoApplyBtn;
            if (!promoInput || !promoMessage || !applyBtn) return;
            
            const code = promoInput.value.trim().toUpperCase();
            
            if (!code) {
                promoMessage.innerHTML = '<span class="promo-error">Please enter a promo code</span>';
                return;
            }
            
            applyBtn.disabled = true;
            applyBtn.textContent = 'Applying...';
            promoMessage.innerHTML = '';
            
            const subtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
            
            try {
                const response = await fetch(API_URLS.validatePromoCode, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        code: code,
                        amount: subtotal
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    window.promoDiscount = data.discount_amount;
                    window.appliedPromoCode = data.code;
                    promoMessage.innerHTML = `<span class="promo-success">✓ Discount applied! Saved $${data.discount_amount.toFixed(2)}</span>`;
                    promoInput.style.borderColor = '#10b981';
                    updateCheckoutView();
                } else {
                    window.promoDiscount = 0;
                    window.appliedPromoCode = null;
                    promoMessage.innerHTML = `<span class="promo-error">${data.message || 'Invalid promo code'}</span>`;
                    promoInput.style.borderColor = 'var(--danger)';
                    updateCheckoutView();
                }
            } catch (error) {
                window.promoDiscount = 0;
                window.appliedPromoCode = null;
                promoMessage.innerHTML = '<span class="promo-error">Error validating promo code. Please try again.</span>';
                updateCheckoutView();
            } finally {
                applyBtn.disabled = false;
                applyBtn.textContent = 'Apply';
            }
        }
        
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        
        function updateCartQty(productId, change) {
            const item = cart.find(i => i.id === productId);
            if (!item) return;
            item.qty += change;
            if (item.qty <= 0) {
                cart = cart.filter(i => i.id !== productId);
            }
            
            // Clear cart from localStorage if empty
            if (cart.length === 0) {
                try {
                    localStorage.setItem('madamda_cart', '[]');
                } catch (e) {
                    console.error('Error clearing cart:', e);
                }
            } else {
                debouncedSaveCart(); // Use debounced save
            }
            
            updateCheckoutView();
        }
        
        function removeFromCart(productId) {
            cart = cart.filter(i => i.id !== productId);
            
            // Clear cart from localStorage if empty
            if (cart.length === 0) {
                try {
                    localStorage.setItem('madamda_cart', '[]');
                } catch (e) {
                    console.error('Error clearing cart:', e);
                }
            } else {
                debouncedSaveCart(); // Use debounced save
            }
            
            updateCheckoutView();
        }
        
        function toggleTelegram(button) {
            const isChecked = button.getAttribute('data-state') === 'checked';
            button.setAttribute('data-state', isChecked ? 'unchecked' : 'checked');
            document.getElementById('telegram-checkbox').checked = !isChecked;
        }
        
        function selectPayment(element) {
            document.querySelectorAll('.payment-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            element.classList.add('selected');
        }
        
        function getSelectedPaymentMethod() {
            const selected = document.querySelector('.payment-option.selected');
            return selected ? selected.getAttribute('data-payment') : 'khqr';
        }
        
        // Optimized form submission with DOM caching
        const checkoutForm = DOMCache.checkoutForm;
        if (checkoutForm) {
            checkoutForm.addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const name = DOMCache.buyerName?.value || '';
                const phone = DOMCache.buyerPhone?.value || '';
                const address = DOMCache.deliveryAddress?.value || '';
                const province = DOMCache.deliveryProvince?.value || '';
            
            if (!name || !phone || !address || !province) {
                showToast('Please fill in all required fields', 'warning');
                return;
            }
            
            if (cart.length === 0) {
                showToast('Your cart is empty', 'warning');
                return;
            }
            
            const subtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
            const discountAmount = window.promoDiscount || 0;
            // Round to 2 decimal places to avoid floating-point precision issues
            const total = Math.round(Math.max(0, subtotal + 0 - discountAmount) * 100) / 100;
            const paymentMethod = getSelectedPaymentMethod();
            
                const modal = DOMCache.paymentModal;
                const modalBody = DOMCache.modalBody;
                if (!modal || !modalBody) return;
                
                modal.classList.add('active');
            // Prevent body scroll when modal is open
            document.body.classList.add('modal-open');
            
            // Handle Cash on Delivery differently
            if (paymentMethod === 'cod') {
                // For COD: Create order immediately without QR code
                modalBody.innerHTML = `
                    <div class="loader"></div>
                    <p style="margin-top: 16px; color: var(--text-light);">Creating your order...</p>
                `;
                
                // Create order for COD
                try {
                    await createOrderForCOD();
                    // Show success and redirect
                    modalBody.innerHTML = `
                        <div style="text-align: center; padding: 20px 0;">
                            <div style="font-size: 48px; color: #22c55e; margin-bottom: 16px;">✓</div>
                            <h3 style="margin-bottom: 8px; color: var(--text);">Order Placed Successfully!</h3>
                            <p style="color: var(--text-light); margin-bottom: 20px;">Your Cash on Delivery order has been created.</p>
                            <p style="color: var(--text-light); font-size: 14px;">You will pay when you receive your order.</p>
                        </div>
                    `;
                    
                    // Redirect to success page after delay
                    setTimeout(() => {
                        redirectToSuccessPage();
                    }, 2000);
                } catch (error) {
                    modalBody.innerHTML = `
                        <div style="color: var(--danger); font-size: 48px; margin: 24px 0;">✕</div>
                        <h3 style="margin-bottom: 8px;">Order Error</h3>
                        <div style="color: var(--text-light);">${error.message || 'Failed to create order. Please try again.'}</div>
                    `;
                }
                return; // Exit early for COD
            }
            
            // KHQR Payment (existing flow)
            modalBody.innerHTML = `
                <div class="loader"></div>
                <p style="margin-top: 16px; color: var(--text-light);">Connecting to payment gateway...</p>
            `;
            
            try {
                // Round to 2 decimal places to avoid floating-point precision issues
                const roundedTotal = Math.round(total * 100) / 100;
                const response = await fetch(`${API_URLS.createKhqr}?amount=${roundedTotal.toFixed(2)}&currency=USD`);
                
                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({ message: 'Unknown error' }));
                    throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
                }
                
                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.message || 'Payment generation failed');
                }
                
                if (!data.qr || !data.md5) {
                    throw new Error('Invalid response from payment gateway: missing QR code or MD5');
                }
                
                // Store QR URL for order success page
                window.currentQRUrl = data.qr;
                
                // Store QR URL and expiration time
                window.currentQRUrl = data.qr;
                const expiresAt = new Date(Date.now() + 5 * 60 * 1000); // 5 minutes from now
                window.qrExpiresAt = expiresAt.toISOString();
                
                // Store QR URL and MD5 for payment checking
                window.currentQRUrl = data.qr;
                window.currentMD5 = data.md5; // Store MD5 for payment checking
                
                // Detect mobile device
                const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent) || 
                                (window.innerWidth <= 768 && 'ontouchstart' in window);
                
                modalBody.innerHTML = `
                    <div style="text-align: center; padding: 20px 0;">
                        <!-- Countdown Timer -->
                        <div id="qr-timer" style="font-size: 24px; font-weight: 700; margin-bottom: 16px; padding: 12px; border-radius: 8px; background: rgba(34, 197, 94, 0.1); color: rgb(34, 197, 94);" class="green">
                            <span id="timer-text">05:00</span>
                        </div>
                        
                        <!-- QR Code Image - Clickable to open bank selection -->
                        <div id="qr-code-container" style="display: flex; justify-content: center; align-items: center; margin: 20px 0;">
                            <div style="margin: 24px 0;">
                                <img src="https://bakong-khqr.web.app/images/khqr_logo.png" alt="BAKONG" style="width: 100px; margin: 0 auto 16px; display: block;" onerror="this.style.display='none'">
                                <img src="${data.qr}" alt="QR Code - Scan with your banking app" id="qr-code-image" class="qr-image" style="width: 250px; height: 250px; max-width: 100%; border: 2px solid var(--border); border-radius: 12px; padding: 10px; background: white; box-shadow: var(--shadow-lg);">
                                <p style="margin-top: 12px; font-size: 13px; color: var(--text-light); text-align: center;">📱 Scan this QR code with your banking app</p>
                            </div>
                        </div>
                        
                        <!-- Expired Message (hidden initially) -->
                        <div id="qr-expired" style="display: none; padding: 20px; background: rgba(239, 68, 68, 0.1); border-radius: 8px; color: #ef4444; font-weight: 600; margin: 20px 0; text-align: center;">
                            <p style="margin: 0 0 8px 0; font-size: 18px;">⏰ QR Code Expired</p>
                            <p style="margin: 0; font-size: 14px; font-weight: 400; opacity: 0.9;">This QR code is no longer valid. Please contact us or create a new order.</p>
                        </div>
                        
                        <div class="qr-amount">$${total.toFixed(2)}</div>
                        
                        <!-- Payment Instructions -->
                        <div style="margin-top: 20px; padding: 16px; background: rgba(24, 119, 242, 0.05); border-radius: 8px;">
                            <p style="font-weight: 600; margin-bottom: 8px; color: rgb(var(--text));">Payment Instructions:</p>
                            <p style="color: var(--text-light); font-size: 14px; margin-bottom: 4px;">Scan the QR code above with your banking app to complete payment. You can use any bank that supports KHQR.</p>
                            <p style="color: var(--text-light); font-size: 14px; margin-bottom: 8px;">ស្កេន QR code ខាងលើដោយប្រើកម្មវិធីធនាគាររបស់អ្នកដើម្បីបញ្ចប់ការទូទាត់។ អ្នកអាចប្រើធនាគារណាមួយដែលគាំទ្រ KHQR។</p>
                            <p style="color: var(--text-light); font-size: 13px; margin-top: 12px; font-weight: 500;">✅ Supported Banks: <strong>ABA Bank</strong>, <strong>ACLEDA Bank</strong>, <strong>Wing Money</strong>, <strong>Sathapana</strong>, <strong>Canadia</strong>, and all banks that support KHQR</p>
                            <p style="color: var(--text-light); font-size: 12px; margin-top: 8px; font-style: italic;">💡 Tip: Tap the QR code or "Open Bank Selection" button to automatically open your banking app</p>
                        </div>
                    </div>
                `;
                
                // Start QR code timer
                startQRTimer(expiresAt);
                
                // Note: Users must scan the QR code with their banking app to complete payment.
                
                startPaymentPolling(data.md5);
            } catch (error) {
                let errorMessage = error.message;
                
                if (errorMessage.includes('403') || errorMessage.includes('forbidden')) {
                    errorMessage = `
                        <div style="text-align: left; max-width: 400px; margin: 0 auto;">
                            <h4 style="margin-bottom: 12px;">Access Forbidden (403)</h4>
                            <p style="color: var(--text-light); margin-bottom: 8px;">This usually means:</p>
                            <ul style="text-align: left; color: var(--text-light); padding-left: 20px;">
                                <li>Bakong ID is not registered</li>
                                <li>Merchant name is not whitelisted</li>
                                <li>Subscription has expired</li>
                            </ul>
                        </div>
                    `;
                }
                
                modalBody.innerHTML = `
                    <div style="color: var(--danger); font-size: 48px; margin: 24px 0;">✕</div>
                    <h3 style="margin-bottom: 8px;">Payment Error</h3>
                    <div style="color: var(--text-light);">${errorMessage}</div>
                `;
                }
            });
        }
        
        // PHASE 1: Faster Payment Polling (1-1.5 seconds instead of 3)
        function startPaymentPolling(md5) {
            let attempts = 0;
            const maxAttempts = 90; // Increased since we're polling faster
            
            pollInterval = setInterval(async () => {
                attempts++;
                if (attempts > maxAttempts) {
                    clearInterval(pollInterval);
                    return;
                }
                
                try {
                    const response = await fetch(`${API_URLS.checkPayment}?md5=${md5}`);
                    
                    if (!response.ok) {
                        console.error(`Payment check failed: HTTP ${response.status}`);
                        return;
                    }
                    
                    const data = await response.json();
                    
                    if (data.error) {
                        console.error('Payment check error:', data.message);
                        if (data.code === 'MD5_NOT_FOUND') {
                            return;
                        }
                        clearInterval(pollInterval);
                        return;
                    }
                    
                    if (data.responseCode === 0) {
                        clearInterval(pollInterval);
                        // Create order immediately when payment is confirmed
                        createOrderOnPaymentConfirmation();
                        showPaymentSuccess();
                    }
                } catch (error) {
                    console.error('Polling error:', error);
                }
            }, attempts <= 5 ? 1000 : 1500); // First 5 checks: 1 second, then 1.5 seconds
        }
        
        // Create order for Cash on Delivery (optimized with DOM cache)
        async function createOrderForCOD() {
            const name = DOMCache.buyerName?.value || '';
            const phone = DOMCache.buyerPhone?.value || '';
            const address = DOMCache.deliveryAddress?.value || '';
            const provinceSelect = DOMCache.deliveryProvince;
            if (!provinceSelect) throw new Error('Province field not found');
            const province = provinceSelect.options[provinceSelect.selectedIndex].text;
            const subtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
            const discountAmount = window.promoDiscount || 0;
            const total = Math.round(Math.max(0, subtotal + 0 - discountAmount) * 100) / 100;
            
            const orderData = {
                name: name,
                phone: phone,
                address: address,
                province: province,
                payment_method: 'Cash on Delivery',
                total: total.toFixed(2),
                subtotal: subtotal.toFixed(2),
                discount: discountAmount.toFixed(2),
                items: cart
            };
            
            try {
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                                 document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';
                
                const response = await fetch(API_URLS.createOrderOnPayment, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify(orderData)
                });
                
                const result = await response.json();
                if (result.success) {
                    console.log('COD Order created:', result.order_number);
                    window.lastOrderNumber = result.order_number;
                    window.currentOrderNumber = result.order_number;
                } else {
                    throw new Error(result.message || 'Failed to create order');
                }
            } catch (error) {
                console.error('Error creating COD order:', error);
                throw error;
            }
        }
        
        async function createOrderOnPaymentConfirmation() {
            // Create order immediately when payment is confirmed (optimized with DOM cache)
            const name = DOMCache.buyerName?.value || '';
            const phone = DOMCache.buyerPhone?.value || '';
            const address = DOMCache.deliveryAddress?.value || '';
            const provinceSelect = DOMCache.deliveryProvince;
            if (!provinceSelect) {
                console.error('Province field not found');
                return;
            }
            const province = provinceSelect.options[provinceSelect.selectedIndex].text;
            const paymentMethod = getSelectedPaymentMethod();
            const subtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
            const discountAmount = window.promoDiscount || 0;
            const total = Math.round(Math.max(0, subtotal + 0 - discountAmount) * 100) / 100;
            
            // Don't generate order number - let backend generate sequential number
            // Map payment method
            const paymentMethodMap = {
                'khqr': 'KHQR',
                'acleda': 'ACLEDA Bank',
                'wing': 'Wing Money',
                'cod': 'Cash on Delivery'
            };
            const paymentMethodName = paymentMethodMap[paymentMethod] || 'KHQR';
            
            const orderData = {
                // order_number will be generated by backend sequentially (don't send it)
                name: name,
                phone: phone,
                address: address,
                province: province,
                payment_method: paymentMethodName,
                total: total.toFixed(2),
                subtotal: subtotal.toFixed(2),
                discount: discountAmount.toFixed(2),
                items: cart
            };
            
            try {
                // Get CSRF token
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                                 document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';
                
                const response = await fetch(API_URLS.createOrderOnPayment, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify(orderData)
                });
                
                const result = await response.json();
                if (result.success) {
                    console.log('Order created and notification sent:', result.order_number);
                    // Store the actual sequential order number from backend for redirect
                    window.lastOrderNumber = result.order_number;
                } else {
                    console.error('Failed to create order:', result.message);
                }
            } catch (error) {
                console.error('Error creating order:', error);
            }
        }
        
        function showPaymentSuccess() {
            const modalBody = DOMCache.modalBody;
            if (!modalBody) return;
            modalBody.innerHTML = `
                <div class="success-icon">
                    <span class="material-symbols-rounded">check</span>
                </div>
                <h3 style="margin-bottom: 8px;">Payment Successful!</h3>
                <p style="color: var(--text-light);">Your order has been placed successfully</p>
            `;
            
            setTimeout(() => {
                redirectToSuccessPage();
            }, 2500);
        }
        
        function redirectToSuccessPage() {
            const name = DOMCache.buyerName?.value || '';
            const phone = DOMCache.buyerPhone?.value || '';
            const address = DOMCache.deliveryAddress?.value || '';
            const provinceSelect = DOMCache.deliveryProvince;
            if (!provinceSelect) {
                console.error('Province field not found');
                return;
            }
            const province = provinceSelect.options[provinceSelect.selectedIndex].text;
            const paymentMethod = getSelectedPaymentMethod();
            const subtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
            const discountAmount = window.promoDiscount || 0;
            // Round to 2 decimal places to avoid floating-point precision issues
            const total = Math.round(Math.max(0, subtotal + 0 - discountAmount) * 100) / 100;
            
            // Use order number from backend (generated sequentially)
            // If not available yet, use placeholder - backend will handle it
            const orderNumber = window.lastOrderNumber || 'NEW';
            
            // Format date
            const now = new Date();
            const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
            const dateStr = `${months[now.getMonth()]} ${now.getDate()}, ${now.getFullYear()} - ${now.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })}`;
            
            // Map payment method names
            const paymentMethodMap = {
                'khqr': 'KHQR',
                'acleda': 'ACLEDA Bank',
                'wing': 'Wing Money',
                'cod': 'Cash on Delivery'
            };
            const paymentMethodName = paymentMethodMap[paymentMethod] || 'KHQR';
            
            // Encode items for URL
            const itemsJson = encodeURIComponent(JSON.stringify(cart));
            
            // Get QR URL if KHQR payment
            const qrUrl = paymentMethod === 'khqr' && window.currentQRUrl ? window.currentQRUrl : '';
            
            // Build success page URL
            const successUrl = `${API_URLS.orderSuccess}?` +
                `order=${orderNumber}&` +
                `name=${encodeURIComponent(name)}&` +
                `phone=${encodeURIComponent(phone)}&` +
                `address=${encodeURIComponent(address)}&` +
                `province=${encodeURIComponent(province)}&` +
                `payment=${encodeURIComponent(paymentMethodName)}&` +
                `total=${total.toFixed(2)}&` +
                `subtotal=${subtotal.toFixed(2)}&` +
                `discount=${discountAmount.toFixed(2)}&` +
                `items=${itemsJson}` +
                (qrUrl ? `&qr_url=${encodeURIComponent(qrUrl)}` : '');
            
            // Clear cart
            cart = [];
            saveCart();
            closeModal();
            
            // Redirect to success page
            window.location.href = successUrl;
        }
        // QR Code Timer Function
        let qrTimerInterval = null;
        
        function startQRTimer(expiresAt) {
            // Clear any existing timer
            if (qrTimerInterval) {
                clearInterval(qrTimerInterval);
            }
            
            const timerElement = document.getElementById('qr-timer');
            const timerText = document.getElementById('timer-text');
            const qrCodeContainer = document.getElementById('qr-code-container');
            const qrCodeImage = document.getElementById('qr-code-image');
            const qrExpired = document.getElementById('qr-expired');
            
            if (!timerElement || !timerText) return;
            
            function updateTimer() {
                const now = new Date();
                const diff = expiresAt - now;
                
                if (diff <= 0) {
                    // Timer expired - QR code is now invalid and cannot be used for payment
                    timerText.textContent = '00:00';
                    timerElement.className = 'red';
                    if (qrCodeContainer) qrCodeContainer.style.display = 'none';
                    if (qrCodeImage) qrCodeImage.style.display = 'none';
                    if (qrExpired) qrExpired.style.display = 'block';
                    if (qrTimerInterval) clearInterval(qrTimerInterval);
                    
                    // Stop payment polling - QR code expired, payment is no longer possible
                    if (pollInterval) {
                        clearInterval(pollInterval);
                        pollInterval = null;
                    }
                    return;
                }
                
                const minutes = Math.floor(diff / 60000);
                const seconds = Math.floor((diff % 60000) / 1000);
                const timeString = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
                timerText.textContent = timeString;
                
                // Update color based on time remaining
                if (minutes >= 2) {
                    timerElement.className = 'green';
                } else if (minutes >= 1) {
                    timerElement.className = 'orange';
                } else {
                    timerElement.className = 'red';
                }
            }
            
            // Update timer immediately and then every second
            updateTimer();
            qrTimerInterval = setInterval(updateTimer, 1000);
        }
        
        function closeModal() {
            const modal = DOMCache.paymentModal;
            if (modal) {
                modal.classList.remove('active');
            }
            // Re-enable body scroll when modal closes
            document.body.classList.remove('modal-open');
            // CRITICAL: Stop polling when modal closes to prevent memory leaks
            if (pollInterval) {
                clearInterval(pollInterval);
                pollInterval = null;
            }
            if (qrTimerInterval) {
                clearInterval(qrTimerInterval);
                qrTimerInterval = null;
            }
        }
        
        // Also stop polling when modal is closed by clicking outside
        const paymentModal = DOMCache.paymentModal;
        if (paymentModal) {
            paymentModal.addEventListener('click', function(e) {
                if (e.target === paymentModal) {
                    closeModal();
                }
            });
        }
        
        // Make select dropdown open upward on mobile when near bottom (optimized)
        function setupSelectDropdown() {
            const select = DOMCache.deliveryProvince;
            if (!select) return;
            
            // On mobile, try to position select better
            select.addEventListener('focus', function() {
                // Check if select is in bottom half of viewport
                const rect = this.getBoundingClientRect();
                const viewportHeight = window.innerHeight;
                const isNearBottom = rect.bottom > viewportHeight * 0.6;
                
                if (isNearBottom && window.innerWidth <= 768) {
                    // Scroll select into view from top
                    setTimeout(() => {
                        this.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 100);
                }
            });
        }
        
        // Initialize on page load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', setupSelectDropdown);
        } else {
            setupSelectDropdown();
        }
        
        async function confirmOrder(paymentMethod) {
            // For COD, create order first, then redirect
            if (paymentMethod === 'cod') {
                try {
                    await createOrderForCOD();
                    // Small delay to ensure order is saved
                    setTimeout(() => {
                        redirectToSuccessPage();
                    }, 100);
                } catch (error) {
                    console.error('Error creating COD order:', error);
                    alert('Failed to create order. Please try again.');
                }
            } else {
                // For other payment methods, redirect immediately
                redirectToSuccessPage();
            }
        }
        
        // ========== HEADER MENU FUNCTIONS (Optimized) ==========
        const menuCache = {
            get menu() { return document.getElementById('dropdown-menu'); },
            get trigger() { return document.getElementById('menu-btn'); }
        };
        
        function toggleMenu() {
            const menu = menuCache.menu;
            if (menu) menu.classList.toggle('open');
        }

        function closeMenu() {
            const menu = menuCache.menu;
            if (menu) menu.classList.remove('open');
        }

        // Close menu when clicking outside (optimized with throttling)
        document.addEventListener('click', throttle(function(event) {
            const menu = menuCache.menu;
            const trigger = menuCache.trigger;
            
            if (menu && trigger && !menu.contains(event.target) && !trigger.contains(event.target)) {
                closeMenu();
            }
        }, 100));

        function setLanguage(lang) {
            // Language switching logic can be added here
            console.log('Language set to:', lang);
            closeMenu();
        }
        
        // ========== PHASE 1: FASTER AUTO-FILL (400ms debounce) ==========
        let autoFillTimeout;
        let manualEdits = {
            name: false,
            address: false,
            province: false
        };
        
        // Optimized auto-fill with debouncing (already has 400ms debounce)
        const buyerPhone = DOMCache.buyerPhone;
        if (buyerPhone) {
            buyerPhone.addEventListener('input', function(e) {
            const phone = e.target.value.trim();
            
            // Clear previous timeout
            clearTimeout(autoFillTimeout);
            
            // Only auto-fill if phone is valid length (at least 8 digits)
            if (phone.length < 8) {
                return;
            }
            
            // PHASE 1: 400ms debounce (faster than before)
            autoFillTimeout = setTimeout(async () => {
                try {
                    const response = await fetch(`/api/customer/lookup/?phone=${encodeURIComponent(phone)}`);
                    
                    // Check if response is OK and is JSON
                    if (!response.ok) {
                        // If 404 or other error, silently fail (customer not found)
                        return;
                    }
                    
                    // Check content type to ensure it's JSON
                    const contentType = response.headers.get('content-type');
                    if (!contentType || !contentType.includes('application/json')) {
                        // Response is not JSON, silently fail
                        return;
                    }
                    
                    const data = await response.json();
                    
                    if (data.success && data.customer) {
                        const nameField = DOMCache.buyerName;
                        const addressField = DOMCache.deliveryAddress;
                        const provinceField = DOMCache.deliveryProvince;
                        
                        // Only auto-fill if fields are empty and not manually edited
                        if (nameField && !nameField.value && !manualEdits.name) {
                            nameField.value = data.customer.name || '';
                            nameField.style.borderColor = '#10b981';
                            setTimeout(() => nameField.style.borderColor = '', 2000);
                        }
                        
                        if (addressField && !addressField.value && !manualEdits.address) {
                            addressField.value = data.customer.address || '';
                            addressField.style.borderColor = '#10b981';
                            setTimeout(() => addressField.style.borderColor = '', 2000);
                        }
                        
                        if (provinceField && !provinceField.value && !manualEdits.province) {
                            // Try to match province
                            const options = Array.from(provinceField.options);
                            const matchedOption = options.find(opt => 
                                opt.text.toLowerCase().includes((data.customer.province || '').toLowerCase())
                            );
                            if (matchedOption) {
                                provinceField.value = matchedOption.value;
                                provinceField.style.borderColor = '#10b981';
                                setTimeout(() => provinceField.style.borderColor = '', 2000);
                            }
                        }
                        
                        // Show success toast
                        showToast('Customer information auto-filled!', 'success', 2000);
                    }
                } catch (error) {
                    // Silently handle errors (customer not found or network issues)
                    // Don't show error to user as this is a background feature
                    if (error.name !== 'SyntaxError') {
                        // Only log non-JSON parsing errors
                        console.debug('Auto-fill lookup:', error.message);
                    }
                }
            }, 400); // 400ms debounce for optimal performance
            });
        }
        
        // Track manual edits to prevent overwriting (optimized)
        const buyerName = DOMCache.buyerName;
        if (buyerName) {
            buyerName.addEventListener('input', function() {
                manualEdits.name = true;
            });
        }
        
        const deliveryAddress = DOMCache.deliveryAddress;
        if (deliveryAddress) {
            deliveryAddress.addEventListener('input', function() {
                manualEdits.address = true;
            });
        }
        
        const deliveryProvince = DOMCache.deliveryProvince;
        if (deliveryProvince) {
            deliveryProvince.addEventListener('change', function() {
                manualEdits.province = true;
            });
        }
        
        updateCheckoutView();
        
        // ========== EXPOSE FUNCTIONS TO GLOBAL SCOPE ==========
        // Required for onclick handlers in HTML
        window.toggleMenu = toggleMenu;
        window.closeMenu = closeMenu;
        window.setLanguage = setLanguage;
        window.toggleTelegram = toggleTelegram;
        window.applyPromoCode = applyPromoCode;
        window.selectPayment = selectPayment;
        window.closeModal = closeModal;
        window.updateCartQty = updateCartQty;
        window.removeFromCart = removeFromCart;