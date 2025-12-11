// Clear cart on success page load
        localStorage.removeItem('madamda_cart');
        
        // Update cart badge if exists
        const headerBadge = document.getElementById('header-badge');
        if (headerBadge) {
            headerBadge.textContent = '0';
            headerBadge.classList.add('hidden');
        }

        // ========== DOWNLOAD RECEIPT FUNCTIONALITY ==========
        // Wait for fonts to load (especially important for Khmer fonts)
        function waitForFonts() {
            return new Promise((resolve) => {
                if (document.fonts && document.fonts.ready) {
                    document.fonts.ready.then(() => {
                        // Additional wait to ensure all fonts are fully loaded
                        setTimeout(resolve, 300);
                    });
                } else {
                    // Fallback for browsers without Font Loading API
                    setTimeout(resolve, 500);
                }
            });
        }
        
        async function downloadReceipt() {
            const downloadBtn = document.getElementById('download-receipt-btn');
            const downloadText = document.getElementById('download-receipt-text');
            const receiptContainer = document.getElementById('receipt-container');
            
            if (!receiptContainer) {
                console.error('Receipt container not found');
                return;
            }
            
            // Check if html2canvas is loaded
            if (typeof html2canvas === 'undefined') {
                alert('Receipt download feature is loading. Please try again in a moment.');
                return;
            }
            
            // Disable button during download
            if (downloadBtn) {
                downloadBtn.disabled = true;
                if (downloadText) downloadText.textContent = 'Generating...';
            }
            
            try {
                // Wait for fonts to load (critical for Khmer text)
                await waitForFonts();
                
                // Hide action buttons temporarily for cleaner receipt
                const actionButtons = document.getElementById('action-buttons');
                const originalDisplay = actionButtons ? actionButtons.style.display : '';
                if (actionButtons) {
                    actionButtons.style.display = 'none';
                }
                
                // Get order number for filename
                const orderNumberElement = document.querySelector('.order-number');
                const orderNumber = orderNumberElement ? orderNumberElement.textContent.trim().replace('#', '') : 'receipt';
                const filename = `Receipt_${orderNumber}_${new Date().toISOString().split('T')[0]}.png`;
                
                // Wait a bit for DOM to update
                await new Promise(resolve => setTimeout(resolve, 200));
                
                // Capture the receipt container with improved font handling
                const canvas = await html2canvas(receiptContainer, {
                    backgroundColor: '#fafafa',
                    scale: 2, // Higher quality for better image
                    useCORS: true,
                    logging: false,
                    allowTaint: false,
                    foreignObjectRendering: true, // Better font rendering
                    width: receiptContainer.scrollWidth,
                    height: receiptContainer.scrollHeight,
                    windowWidth: receiptContainer.scrollWidth,
                    windowHeight: receiptContainer.scrollHeight,
                    onclone: function(clonedDoc, element) {
                        // Ensure all styles and fonts are applied in cloned document
                        const clonedContainer = clonedDoc.getElementById('receipt-container');
                        if (clonedContainer) {
                            clonedContainer.style.backgroundColor = '#fafafa';
                        }
                        
                        // Ensure UTF-8 encoding and proper charset
                        if (clonedDoc.documentElement) {
                            clonedDoc.documentElement.setAttribute('lang', 'en');
                            clonedDoc.documentElement.setAttribute('dir', 'ltr');
                            clonedDoc.documentElement.setAttribute('charset', 'UTF-8');
                        }
                        
                        // Add Khmer font fallbacks to body
                        const clonedBody = clonedDoc.body;
                        if (clonedBody) {
                            clonedBody.style.fontFamily = "'Inter', 'Dangrek', 'AkbalthomMonstera', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif";
                        }
                        
                        // Apply fonts to all text elements in cloned document
                        const textElements = clonedDoc.querySelectorAll('p, span, div, h1, h2, h3, h4, h5, h6, a, button, label, .info-value, .info-label, .order-item-name, .customer-info, .delivery-message');
                        textElements.forEach(el => {
                            let originalEl = null;
                            
                            // Try to find original element by ID (if ID exists and is valid)
                            if (el.id && el.id.trim() !== '') {
                                try {
                                    originalEl = receiptContainer.querySelector(`#${el.id}`);
                                } catch (e) {
                                    // Invalid selector, skip ID lookup
                                }
                            }
                            
                            // If not found by ID, try to find by tag name and text content
                            if (!originalEl) {
                                const sameTagElements = receiptContainer.querySelectorAll(el.tagName);
                                originalEl = Array.from(sameTagElements).find(e => {
                                    // Match by text content (trimmed and normalized)
                                    const clonedText = el.textContent.trim();
                                    const originalText = e.textContent.trim();
                                    return clonedText && originalText && clonedText === originalText;
                                });
                            }
                            
                            // Apply font family
                            if (originalEl) {
                                try {
                                    const computedStyle = window.getComputedStyle(originalEl);
                                    const fontFamily = computedStyle.getPropertyValue('font-family');
                                    if (fontFamily && fontFamily.trim() !== '') {
                                        el.style.fontFamily = fontFamily;
                                    } else {
                                        el.style.fontFamily = "'Inter', 'Dangrek', 'AkbalthomMonstera', sans-serif";
                                    }
                                } catch (e) {
                                    // Fallback if getComputedStyle fails
                                    el.style.fontFamily = "'Inter', 'Dangrek', 'AkbalthomMonstera', sans-serif";
                                }
                            } else {
                                // No original element found, use default font stack
                                el.style.fontFamily = "'Inter', 'Dangrek', 'AkbalthomMonstera', sans-serif";
                            }
                        });
                    }
                });
                
                // Convert canvas to blob
                canvas.toBlob(function(blob) {
                    if (!blob) {
                        throw new Error('Failed to create image blob');
                    }
                    
                    // Create download link
                    const url = URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.download = filename;
                    link.style.display = 'none';
                    
                    // Trigger download
                    document.body.appendChild(link);
                    link.click();
                    
                    // Clean up
                    setTimeout(() => {
                        document.body.removeChild(link);
                        URL.revokeObjectURL(url);
                    }, 100);
                    
                    // Restore action buttons
                    if (actionButtons) {
                        actionButtons.style.display = originalDisplay;
                    }
                    
                    // Re-enable button
                    if (downloadBtn) {
                        downloadBtn.disabled = false;
                        if (downloadText) downloadText.textContent = 'Download Receipt';
                    }
                }, 'image/png', 0.95);
                
            } catch (error) {
                console.error('Error downloading receipt:', error);
                alert('Failed to download receipt. Please try again.');
                
                // Restore action buttons
                const actionButtons = document.getElementById('action-buttons');
                if (actionButtons) {
                    actionButtons.style.display = '';
                }
                
                // Re-enable button
                if (downloadBtn) {
                    downloadBtn.disabled = false;
                    if (downloadText) downloadText.textContent = 'Download Receipt';
                }
            }
        }
        
        // Expose function globally for onclick handler
        window.downloadReceipt = downloadReceipt;