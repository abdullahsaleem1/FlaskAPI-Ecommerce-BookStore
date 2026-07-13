// API Service Layer

/**
 * Make API request
 */
async function apiRequest(endpoint, method = 'GET', data = null, requiresAuth = false) {
    const url = `${CONFIG.API_BASE_URL}${endpoint}`;
    const headers = {
        'Content-Type': 'application/json'
    };
    
    // Add auth token if required
    if (requiresAuth) {
        const token = getAccessToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
    }
    
    const options = {
        method,
        headers
    };
    
    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        const responseData = await response.json();
        
        // Handle 401 (unauthorized) - token expired
        if (response.status === 401 && requiresAuth) {
            // Try to refresh token
            const refreshed = await refreshAccessToken();
            if (refreshed) {
                // Retry original request
                headers['Authorization'] = `Bearer ${getAccessToken()}`;
                const retryResponse = await fetch(url, { ...options, headers });
                return await retryResponse.json();
            } else {
                // Refresh failed, logout
                logout();
                throw new Error('Session expired. Please login again.');
            }
        }
        
        if (!response.ok) {
            throw new Error(responseData.error || responseData.message || 'Request failed');
        }
        
        return responseData;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * Refresh access token
 */
async function refreshAccessToken() {
    const refreshToken = getRefreshToken();
    if (!refreshToken) return false;
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}${ENDPOINTS.REFRESH}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${refreshToken}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            saveTokens(data.access_token, null);
            return true;
        }
        return false;
    } catch (error) {
        console.error('Token refresh failed:', error);
        return false;
    }
}

/**
 * API GET request
 */
async function apiGet(endpoint, requiresAuth = false) {
    return await apiRequest(endpoint, 'GET', null, requiresAuth);
}

/**
 * API POST request
 */
async function apiPost(endpoint, data, requiresAuth = false) {
    return await apiRequest(endpoint, 'POST', data, requiresAuth);
}

/**
 * API PUT request
 */
async function apiPut(endpoint, data, requiresAuth = false) {
    return await apiRequest(endpoint, 'PUT', data, requiresAuth);
}

/**
 * API DELETE request
 */
async function apiDelete(endpoint, requiresAuth = false) {
    return await apiRequest(endpoint, 'DELETE', null, requiresAuth);
}

/**
 * Login user
 */
async function loginUser(username, password) {
    const data = await apiPost(ENDPOINTS.LOGIN, { username, password });
    saveTokens(data.access_token, data.refresh_token);
    saveUserData(data.user);
    return data;
}

/**
 * Register user
 */
async function registerUser(userData) {
    return await apiPost(ENDPOINTS.REGISTER, userData);
}

/**
 * Get current user
 */
async function getCurrentUser() {
    return await apiGet(ENDPOINTS.ME, true);
}

/**
 * Get books with filters
 */
async function getBooks(filters = {}) {
    const params = new URLSearchParams();
    if (filters.category_id) params.append('category_id', filters.category_id);
    if (filters.author_id) params.append('author_id', filters.author_id);
    if (filters.min_price) params.append('min_price', filters.min_price);
    if (filters.max_price) params.append('max_price', filters.max_price);
    
    const queryString = params.toString();
    const endpoint = queryString ? `${ENDPOINTS.BOOKS}?${queryString}` : ENDPOINTS.BOOKS;
    return await apiGet(endpoint);
}

/**
 * Get book by ID
 */
async function getBookById(id) {
    return await apiGet(ENDPOINTS.BOOK_DETAIL(id));
}

/**
 * Get categories
 */
async function getCategories() {
    return await apiGet(ENDPOINTS.CATEGORIES);
}

/**
 * Get authors
 */
async function getAuthors() {
    return await apiGet(ENDPOINTS.AUTHORS);
}

/**
 * Get cart
 */
async function getCart() {
    return await apiGet(ENDPOINTS.CART, true);
}

/**
 * Add to cart
 */
async function addToCart(bookId, quantity = 1) {
    return await apiPost(ENDPOINTS.CART_ADD, { book_id: bookId, quantity }, true);
}

/**
 * Update cart item
 */
async function updateCartItem(itemId, quantity) {
    return await apiPut(ENDPOINTS.CART_ITEM(itemId), { quantity }, true);
}

/**
 * Remove from cart
 */
async function removeFromCart(itemId) {
    return await apiDelete(ENDPOINTS.CART_ITEM(itemId), true);
}

/**
 * Place order
 */
async function placeOrder(orderData) {
    return await apiPost(ENDPOINTS.ORDER_CHECKOUT, orderData, true);
}

/**
 * Get user orders
 */
async function getUserOrders() {
    return await apiGet(ENDPOINTS.ORDERS, true);
}

/**
 * Get order details
 */
async function getOrderDetails(orderId) {
    return await apiGet(ENDPOINTS.ORDER_DETAIL(orderId), true);
}