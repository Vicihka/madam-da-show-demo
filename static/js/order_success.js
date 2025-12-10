// Clear cart on success page load
        localStorage.removeItem('madamda_cart');
        
        // Update cart badge if exists
        const headerBadge = document.getElementById('header-badge');
        if (headerBadge) {
            headerBadge.textContent = '0';
            headerBadge.classList.add('hidden');
        }