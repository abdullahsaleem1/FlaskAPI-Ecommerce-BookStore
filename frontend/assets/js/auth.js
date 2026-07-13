// Authentication Module

/**
 * Save tokens to localStorage
 */
function saveTokens(accessToken, refreshToken) {
    localStorage.setItem(CONFIG.TOKEN_KEY, accessToken);
    if (refreshToken) {
        localStorage.setItem(CONFIG.REFRESH_TOKEN_KEY, refreshToken);
    }
}

/**
 * Get access token
 */
function getAccessToken() {
    return localStorage.getItem(CONFIG.TOKEN_KEY);
}

/**
 * Get refresh token
 */
function getRefreshToken() {
    return localStorage.getItem(CONFIG.REFRESH_TOKEN_KEY);
}

/**
 * Save user data
 */
function saveUserData(user) {
    localStorage.setItem(CONFIG.USER_KEY, JSON.stringify(user));
}

/**
 * Get user data
 */
function getUserData() {
    const userData = localStorage.getItem(CONFIG.USER_KEY);
    return userData ? JSON.parse(userData) : null;
}

/**
 * Check if user is logged in
 */
function isLoggedIn() {
    return !!getAccessToken();
}

/**
 * Check if user is admin
 */
function isAdmin() {
    const user = getUserData();
    return user && user.role === ROLES.ADMIN;
}

/**
 * Logout user
 */
function logout() {
    localStorage.removeItem(CONFIG.TOKEN_KEY);
    localStorage.removeItem(CONFIG.REFRESH_TOKEN_KEY);
    localStorage.removeItem(CONFIG.USER_KEY);
    localStorage.removeItem(CONFIG.CART_KEY);
    redirectTo('index.html');
}

/**
 * Redirect if not authenticated
 */
function requireAuth() {
    if (!isLoggedIn()) {
        redirectTo('login.html');
        return false;
    }
    return true;
}

/**
 * Redirect if not admin
 */
function requireAdmin() {
    if (!isLoggedIn() || !isAdmin()) {
        showToast('Access denied. Admin privileges required.', 'danger');
        redirectTo('index.html');
        return false;
    }
    return true;
}

/**
 * Update navbar based on auth status
 */
function updateNavbar() {
    const authLinks = document.getElementById('auth-links');
    const cartBadge = document.getElementById('cart-badge');
    
    // Check if elements exist (some pages may not have navbar)
    if (!authLinks) return;
    
    if (isLoggedIn()) {
        const user = getUserData();
        authLinks.innerHTML = `
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" 
                   data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="fas fa-user"></i> ${user.username}
                </a>
                <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                    <li><a class="dropdown-item" href="orders.html">My Orders</a></li>
                    ${user.role === ROLES.ADMIN ? '<li><a class="dropdown-item" href="admin.html">Admin Panel</a></li>' : ''}
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="#" onclick="logout()">Logout</a></li>
                </ul>
            </li>
        `;
        
        // Update cart badge
        updateCartBadge();
    } else {
        authLinks.innerHTML = `
            <li class="nav-item">
                <a class="nav-link" href="login.html">
                    <i class="fas fa-sign-in-alt"></i> Login
                </a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="register.html">
                    <i class="fas fa-user-plus"></i> Register
                </a>
            </li>
        `;
        
        if (cartBadge) {
            cartBadge.textContent = '0';
        }
    }
}

/**
 * Update cart badge count
 */
async function updateCartBadge() {
    if (!isLoggedIn()) return;
    
    try {
        const response = await apiGet(ENDPOINTS.CART, true);
        const cartBadge = document.getElementById('cart-badge');
        if (cartBadge && response.cart) {
            const totalItems = response.cart.reduce((sum, item) => sum + item.quantity, 0);
            cartBadge.textContent = totalItems;
        }
    } catch (error) {
        console.error('Error updating cart badge:', error);
    }
}

// Initialize navbar on page load
document.addEventListener('DOMContentLoaded', updateNavbar);
