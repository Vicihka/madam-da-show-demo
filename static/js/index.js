// ========== PERFORMANCE OPTIMIZATIONS ==========
// DOM Query Caching
const DOMCache = {
    get headerBadge() { return document.getElementById('header-badge'); },
    get floatingCart() { return document.getElementById('floating-cart'); },
    get cartCount() { return document.getElementById('cart-count'); },
    get cartThumbs() { return document.getElementById('cart-thumbs'); }
};

// Debounce utility
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

// Debounced cart save
const debouncedSaveCart = debounce(() => {
    try {
        localStorage.setItem('madamda_cart', JSON.stringify(cart));
        try {
            sessionStorage.setItem('madamda_cart_backup', JSON.stringify(cart));
        } catch (e) {
            console.warn('sessionStorage not available:', e);
        }
    } catch (e) {
        console.error('Error saving cart:', e);
        try {
            sessionStorage.setItem('madamda_cart_backup', JSON.stringify(cart));
        } catch (e2) {
            console.error('Error saving to sessionStorage:', e2);
        }
    }
}, 300);

// ========== PRODUCTS DATA ==========
// PRODUCTS array will be defined inline in HTML template (needs Django template processing)
// This ensures it's available globally before this script runs

// ========== STATE MANAGEMENT ==========
let cart = JSON.parse(localStorage.getItem('madamda_cart')) || [];
let heroSlideIndex = 0;

// ========== INITIALIZATION ==========
function init() {
    // Load cart from localStorage on page load to ensure sync
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
                } else {
                    cart = [];
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
    
    updateCartUI();
    // Initialize all product states on page load (only called once)
    updateProductStates();
    startHeroCarousel();
    
    // Listen for storage changes to sync cart across tabs/pages
    window.addEventListener('storage', function(e) {
        if (e.key === 'madamda_cart') {
            cart = JSON.parse(e.newValue || '[]') || [];
            updateCartUI();
            updateProductStates();
        }
    });
    
    // Set interval for hero carousel
    setInterval(() => {
        const slides = document.querySelectorAll('.hero-slide');
        heroSlideIndex = (heroSlideIndex + 1) % slides.length;
        setHeroSlide(heroSlideIndex);
    }, 5000);
    
    // Initialize video playback for active slide
    startHeroCarousel();
    
    // Save cart before page unload (when user closes window/tab)
    window.addEventListener('beforeunload', function() {
        try {
            saveCart();
        } catch (e) {
            console.error('Error saving cart on page unload:', e);
        }
    });
    
    // Also save cart periodically (every 5 seconds) as backup
    setInterval(function() {
        if (cart.length > 0) {
            try {
                saveCart();
            } catch (e) {
                console.error('Error in periodic cart save:', e);
            }
        }
    }, 5000);
    
    // Save cart when page visibility changes (user switches tabs)
    document.addEventListener('visibilitychange', function() {
        if (document.hidden && cart.length > 0) {
            try {
                saveCart();
            } catch (e) {
                console.error('Error saving cart on visibility change:', e);
            }
        }
    });
}

// ========== CART FUNCTIONS ==========
function addToCart(productId) {
    const product = PRODUCTS.find(p => p.id === productId);
    if (!product) return;

    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.qty++;
    } else {
        cart.push({
            id: product.id,
            name: product.name,
            price: product.price,
            image: product.image,
            qty: 1
        });
    }

    debouncedSaveCart(); // Use debounced save
    updateCartUI();
    // Update only the specific product that was added
    updateSingleProductState(productId);
}

function updateCartQty(productId, change) {
    // Find the specific item in cart
    let item = cart.find(i => i.id === productId);
    
    // If item not in cart and trying to increase, add it first
    if (!item && change > 0) {
        addToCart(productId);
        return; // addToCart will handle UI updates
    }
    
    // If item not in cart and trying to decrease, silently return
    // (This shouldn't happen if UI is correct, but handle gracefully)
    if (!item && change < 0) {
        return;
    }
    
    // Item exists, update quantity
    item.qty += change;
    
    if (item.qty <= 0) {
        cart = cart.filter(i => i.id !== productId);
    }

    // Clear cart from localStorage if empty
    if (cart.length === 0) {
        localStorage.setItem('madamda_cart', '[]');
    } else {
        debouncedSaveCart(); // Use debounced save
    }

    updateCartUI();
    // Update ONLY the specific product that was changed - scoped to this product card
    updateSingleProductState(productId);
}

function updateSingleProductState(productId) {
    // Use specific selector scoped to the product card
    const card = document.querySelector(`.product-card[data-id="${productId}"]`);
    if (!card) {
        console.warn(`Product card not found for ID: ${productId}`);
        return;
    }
    
    // Find elements scoped to this specific card only
    const addBtn = card.querySelector('.btn-add-cart');
    const qtyControl = card.querySelector('.qty-control');
    const qtyValue = card.querySelector('.qty-value');
    
    if (!addBtn || !qtyControl || !qtyValue) {
        console.warn(`Missing elements for product card ID: ${productId}`);
        return;
    }
    
    // Check cart state for this specific product only
    const cartItem = cart.find(i => i.id === productId);

    if (cartItem && cartItem.qty > 0) {
        // Product is in cart: hide add button, show quantity control
        addBtn.style.display = 'none';
        qtyControl.classList.add('active');
        qtyValue.textContent = cartItem.qty;
    } else {
        // Product is not in cart: show add button, hide quantity control
        addBtn.style.display = 'flex';
        qtyControl.classList.remove('active');
        if (qtyValue) {
            qtyValue.textContent = '1';
        }
    }
}

function updateProductStates() {
    // This function is only for initialization - updates all products on page load
    // For individual product updates, use updateSingleProductState() instead
    document.querySelectorAll('.product-card').forEach(card => {
        const productId = card.dataset.id;
        if (!productId) return;
        
        // Scope selectors to this specific card only
        const cartItem = cart.find(i => i.id === productId);
        const addBtn = card.querySelector('.btn-add-cart');
        const qtyControl = card.querySelector('.qty-control');
        const qtyValue = card.querySelector('.qty-value');
        
        if (!addBtn || !qtyControl || !qtyValue) return;

        if (cartItem && cartItem.qty > 0) {
            // Product is in cart: hide add button, show quantity control
            addBtn.style.display = 'none';
            qtyControl.classList.add('active');
            qtyValue.textContent = cartItem.qty;
        } else {
            // Product is not in cart: show add button, hide quantity control
            addBtn.style.display = 'flex';
            qtyControl.classList.remove('active');
            qtyValue.textContent = '1';
        }
    });
}

// Legacy saveCart function (kept for compatibility, but use debouncedSaveCart instead)
function saveCart() {
    debouncedSaveCart();
}

// Optimized updateCartUI with DOM caching and requestAnimationFrame
function updateCartUI() {
    requestAnimationFrame(() => {
        // Reload cart from localStorage to ensure sync
        cart = JSON.parse(localStorage.getItem('madamda_cart')) || [];
        
        const count = cart.reduce((sum, item) => sum + item.qty, 0);
        
        // Header badge (using cached DOM)
        const headerBadge = DOMCache.headerBadge;
        if (headerBadge) {
            headerBadge.textContent = count;
            headerBadge.classList.toggle('hidden', count === 0);
        }

        // Floating cart (using cached DOM)
        const floatingCart = DOMCache.floatingCart;
        const cartCount = DOMCache.cartCount;
        const cartThumbs = DOMCache.cartThumbs;

    if (count > 0) {
        if (floatingCart) floatingCart.classList.add('active');
        if (cartCount) cartCount.textContent = count;
        
        // Show up to 3 product thumbnails (use WebP if available)
        if (cartThumbs) {
            const thumbnails = cart.slice(0, 3).map(item => {
                const imageUrl = item.image || '';
                // Try to use WebP version if available
                const webpUrl = imageUrl.replace(/\.(png|jpg|jpeg)$/i, '.webp');
                return `<img src="${imageUrl}" alt="${item.name}" class="cart-thumb" loading="lazy" width="32" height="32" decoding="async" fetchpriority="low" onerror="this.onerror=null;">`;
            }).join('');
            cartThumbs.innerHTML = thumbnails;
        }
    } else {
        // Cart is empty - hide floating cart and clear count
        if (floatingCart) floatingCart.classList.remove('active');
        if (cartCount) cartCount.textContent = '0';
        if (cartThumbs) cartThumbs.innerHTML = '';
        // Ensure localStorage is cleared
        localStorage.setItem('madamda_cart', '[]');
    }
    });
}

// ========== HERO CAROUSEL ==========
function setHeroSlide(index) {
    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.hero-dot');
    const videos = document.querySelectorAll('.hero-video');
    
    // Pause all videos
    videos.forEach(video => {
        video.pause();
    });
    
    slides.forEach(s => s.classList.remove('active'));
    dots.forEach(d => d.classList.remove('active'));
    
    heroSlideIndex = index;
    slides[heroSlideIndex].classList.add('active');
    dots[heroSlideIndex].classList.add('active');
    
    // Play video in active slide
    const activeSlide = slides[heroSlideIndex];
    const activeVideo = activeSlide.querySelector('.hero-video');
    if (activeVideo) {
        activeVideo.play().catch(e => console.log('Video autoplay prevented:', e));
    }
}

function startHeroCarousel() {
    // Play video in active slide on page load
    const activeSlide = document.querySelector('.hero-slide.active');
    if (activeSlide) {
        const activeVideo = activeSlide.querySelector('.hero-video');
        if (activeVideo) {
            activeVideo.play().catch(e => console.log('Video autoplay prevented:', e));
        }
    }
}


// ========== DROPDOWN MENU ==========
function toggleMenu() {
    const menu = document.getElementById('dropdown-menu');
    menu.classList.toggle('open');
}

function closeMenu() {
    const menu = document.getElementById('dropdown-menu');
    menu.classList.remove('open');
}

// Close menu when clicking outside
document.addEventListener('click', function(event) {
    const menu = document.getElementById('dropdown-menu');
    const trigger = document.getElementById('menu-btn');
    
    if (menu && trigger && !menu.contains(event.target) && !trigger.contains(event.target)) {
        closeMenu();
    }
});

function setLanguage(lang) {
    // Language switching logic can be added here
    console.log('Language set to:', lang);
    closeMenu();
}

// ========== TRACK ORDER ==========
function openTrackOrder() {
    const modal = document.getElementById('track-order-modal');
    if (modal) {
        modal.classList.add('active');
        // Focus on first input
        setTimeout(() => {
            const input = modal.querySelector('#track-order-number');
            if (input) input.focus();
        }, 100);
    }
}

function closeTrackOrder() {
    const modal = document.getElementById('track-order-modal');
    if (modal) {
        modal.classList.remove('active');
        // Reset form
        const form = document.getElementById('track-order-form');
        if (form) form.reset();
        const result = document.getElementById('track-result');
        if (result) {
            result.classList.remove('show', 'success', 'error');
            result.innerHTML = '';
        }
    }
}

async function trackOrder() {
    const orderNumber = document.getElementById('track-order-number').value.trim().toUpperCase();
    const phone = document.getElementById('track-phone').value.trim();
    const trackBtn = document.getElementById('track-submit-btn');
    const result = document.getElementById('track-result');
    
    // Validation
    if (!orderNumber || !phone) {
        showTrackResult('Please enter both order number and phone number', 'error');
        return;
    }
    
    // Disable button
    trackBtn.disabled = true;
    trackBtn.textContent = 'Tracking...';
    
    try {
        const response = await fetch('/api/order/track/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                order_number: orderNumber,
                phone: phone
            })
        });
        
        const data = await response.json();
        
        if (data.success && data.order) {
            displayOrderDetails(data.order);
        } else {
            showTrackResult(data.message || 'Order not found', 'error');
        }
    } catch (error) {
        showTrackResult('Error tracking order. Please try again.', 'error');
        console.error('Track order error:', error);
    } finally {
        trackBtn.disabled = false;
        trackBtn.textContent = 'Track Order';
    }
}

function showTrackResult(message, type) {
    const result = document.getElementById('track-result');
    if (result) {
        result.className = `track-result show ${type}`;
        result.innerHTML = `<div style="font-weight: 600; margin-bottom: 8px;">${type === 'error' ? '❌' : '✅'} ${message}</div>`;
    }
}

function displayOrderDetails(order) {
    const result = document.getElementById('track-result');
    if (!result) return;
    
    const statusClass = `status-${order.status}`;
    const paymentStatus = order.payment_method === 'Cash on Delivery' 
        ? (order.payment_received ? '✅ Paid' : '⏳ Not Paid')
        : '✅ Paid';
    
    const customerReceived = order.customer_received 
        ? '✅ Received' 
        : '⏳ Not Received';
    
    const itemsList = order.items.map(item => 
        `${item.product_name} x${item.quantity}`
    ).join('<br>');
    
    result.className = 'track-result show success';
    result.innerHTML = `
        <div style="font-weight: 700; font-size: 18px; margin-bottom: 16px; color: #155724;">
            ✅ Order Found
        </div>
        <div class="order-details">
            <div class="detail-row">
                <span class="detail-label">Order Number:</span>
                <span class="detail-value">#${order.order_number}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Status:</span>
                <span class="detail-value">
                    <span class="status-badge ${statusClass}">${order.status_display}</span>
                </span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Customer:</span>
                <span class="detail-value">${order.customer_name}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Phone:</span>
                <span class="detail-value">${order.customer_phone}</span>
            </div>
            ${order.customer_address ? `
            <div class="detail-row">
                <span class="detail-label">Address:</span>
                <span class="detail-value">${order.customer_address}</span>
            </div>
            ` : ''}
            <div class="detail-row">
                <span class="detail-label">Payment Method:</span>
                <span class="detail-value">${order.payment_method}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Payment Status:</span>
                <span class="detail-value">${paymentStatus}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Customer Received:</span>
                <span class="detail-value">${customerReceived}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Total Amount:</span>
                <span class="detail-value" style="color: rgb(var(--primary)); font-size: 18px;">$${order.total}</span>
            </div>
            <div class="detail-row" style="margin-top: 12px; padding-top: 12px; border-top: 2px solid rgba(0,0,0,0.1);">
                <span class="detail-label">Items:</span>
                <span class="detail-value" style="text-align: right;">${itemsList}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Order Date:</span>
                <span class="detail-value">${new Date(order.created_at).toLocaleDateString('en-US', {year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'})}</span>
            </div>
        </div>
    `;
}

// Close modal on outside click
document.addEventListener('click', function(e) {
    const modal = document.getElementById('track-order-modal');
    if (modal && e.target === modal) {
        closeTrackOrder();
    }
});

// Close modal on Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const modal = document.getElementById('track-order-modal');
        if (modal && modal.classList.contains('active')) {
            closeTrackOrder();
        }
    }
});

// ========== INITIALIZE APP ==========
init();