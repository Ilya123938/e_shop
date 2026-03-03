/* ============ Custom JavaScript for E-Shop ============ */

// Initialize animations
document.addEventListener('DOMContentLoaded', function() {
    initializeAnimations();
    initializeCartFunctionality();
    initializeFormValidation();
});

// Animations on scroll
function initializeAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.product-card, .feature-box').forEach(el => {
        observer.observe(el);
    });
}

// Cart functionality
function initializeCartFunctionality() {
    // Update cart badge on page load
    updateCartBadge();

    // Add to cart button
    document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const productId = this.dataset.productId;
            addToCart(productId);
        });
    });

    // Remove from cart
    document.querySelectorAll('.remove-from-cart-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const productId = this.dataset.productId;
            removeFromCart(productId);
        });
    });
}

// Add to cart with feedback
function addToCart(productId) {
    // Get current cart from localStorage
    let cart = JSON.parse(localStorage.getItem('cart') || '{}');
    cart[productId] = (cart[productId] || 0) + 1;
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartBadge();
    
    // Show success message
    showNotification('Product added to cart!', 'success');
}

// Remove from cart
function removeFromCart(productId) {
    let cart = JSON.parse(localStorage.getItem('cart') || '{}');
    delete cart[productId];
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartBadge();
    showNotification('Product removed from cart!', 'info');
}

// Update cart badge
function updateCartBadge() {
    const cart = JSON.parse(localStorage.getItem('cart') || '{}');
    const count = Object.values(cart).reduce((a, b) => a + b, 0);
    const badge = document.getElementById('cart-badge');
    if (badge) {
        badge.textContent = count;
        badge.style.display = count > 0 ? 'flex' : 'none';
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    const alertBox = `
        <div class="fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg text-white animate-fade-in
            ${type === 'success' ? 'bg-green-500' : type === 'error' ? 'bg-red-500' : 'bg-blue-500'}">
            <div class="flex items-center gap-2">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
                <span>${message}</span>
            </div>
        </div>
    `;
    
    const container = document.createElement('div');
    container.innerHTML = alertBox;
    document.body.appendChild(container.firstElementChild);
    
    setTimeout(() => {
        container.firstElementChild.remove();
    }, 3000);
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showNotification('Please fill in all required fields', 'error');
            }
        });
    });
}

// Simple form validation
function validateForm(form) {
    const inputs = form.querySelectorAll('[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('border-red-500');
            isValid = false;
        } else {
            input.classList.remove('border-red-500');
        }
    });
    
    return isValid;
}

// Search functionality
function initializeSearch() {
    const searchInput = document.querySelector('[name="query"]');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            filterProducts(query);
        });
    }
}

// Filter products by search
function filterProducts(query) {
    const products = document.querySelectorAll('.product-card');
    products.forEach(product => {
        const title = product.querySelector('.product-title')?.textContent.toLowerCase() || '';
        const description = product.querySelector('.product-description')?.textContent.toLowerCase() || '';
        
        if (title.includes(query) || description.includes(query)) {
            product.style.display = 'block';
        } else {
            product.style.display = 'none';
        }
    });
}

// Price filter
function filterByPrice(minPrice, maxPrice) {
    const products = document.querySelectorAll('.product-card');
    products.forEach(product => {
        const priceText = product.querySelector('.product-price')?.textContent;
        const price = parseFloat(priceText?.replace(/[^0-9.-]+/g, ''));
        
        if (price >= minPrice && price <= maxPrice) {
            product.style.display = 'block';
        } else {
            product.style.display = 'none';
        }
    });
}

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// Mobile menu toggle
function toggleMobileMenu() {
    const menu = document.querySelector('#mobileMenu');
    if (menu) {
        menu.classList.toggle('show');
    }
}

// Lazy loading images
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-lazy]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.lazy;
                img.removeAttribute('data-lazy');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Initialize lazy loading
initializeLazyLoading();

// Export functions if needed
window.shopUtils = {
    addToCart,
    removeFromCart,
    showNotification,
    filterProducts,
    filterByPrice,
    toggleMobileMenu,
    updateCartBadge
};
