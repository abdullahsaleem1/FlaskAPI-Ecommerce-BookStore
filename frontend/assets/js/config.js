// API Configuration
const CONFIG = {
    API_BASE_URL: 'https://daastan.onrender.com/api/v1',
    TOKEN_KEY: 'access_token',
    REFRESH_TOKEN_KEY: 'refresh_token',
    USER_KEY: 'user_data',
    CART_KEY: 'cart_items'
};

// API Endpoints
const ENDPOINTS = {
    // Auth
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    ME: '/auth/me',
    REFRESH: '/auth/refresh',
    
    // Books
    BOOKS: '/books',
    BOOK_DETAIL: (id) => `/books/${id}`,
    
    // Authors
    AUTHORS: '/authors',
    
    // Categories
    CATEGORIES: '/categories',
    
    // Cart
    CART: '/cart',
    CART_ADD: '/cart/items',
    CART_ITEM: (id) => `/cart/items/${id}`,
    
    // Orders
    ORDERS: '/orders',
    ORDER_CHECKOUT: '/orders/checkout',
    ORDER_DETAIL: (id) => `/orders/${id}`,
    
    // Reviews
    REVIEWS: (bookId) => `/books/${bookId}/reviews`,
    
    // Users
    USERS: '/users',
    USER_PROFILE: '/users/profile',
    
    // Admin
    ADMIN_BOOKS: '/admin/books',
    ADMIN_BOOK: (id) => `/admin/books/${id}`,
    ADMIN_ORDERS: '/admin/orders',
    ADMIN_ORDER_STATUS: (id) => `/admin/orders/${id}/status`
};

// User Roles
const ROLES = {
    CUSTOMER: 0,
    ADMIN: 1
};
