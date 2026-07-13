# Bookstore Frontend

A clean, responsive vanilla JavaScript frontend for the Flask Bookstore API with a warm, cozy bookstore aesthetic.

## 🎨 Design Theme

- **Color Palette**: Warm browns, cream, and gold accents
- **Typography**: Playfair Display (headings) + Lato (body)
- **Style**: Modern bookstore aesthetic with card-based layout

## 🚀 Quick Start

### Prerequisites

- Flask API running at `http://localhost:5000`
- Modern web browser
- No build tools required!

### Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Open with Live Server** (Recommended):
   - Install VS Code extension: "Live Server"
   - Right-click `index.html` → "Open with Live Server"
   - Or open `index.html` directly in your browser

3. **Alternative - Python HTTP Server**:
   ```bash
   python -m http.server 8000
   ```
   Then visit: `http://localhost:8000`

## 📁 Project Structure

```
frontend/
├── index.html              # Landing page
├── books.html              # Browse books with filters
├── book-detail.html        # Single book view
├── cart.html               # Shopping cart
├── checkout.html           # Checkout form
├── orders.html             # User orders history
├── login.html              # Login page
├── register.html           # Registration page
├── assets/
│   ├── css/
│   │   └── style.css       # All custom styles
│   ├── js/
│   │   ├── config.js       # API configuration
│   │   ├── api.js          # API service layer
│   │   ├── auth.js         # Authentication logic
│   │   └── utils.js        # Helper functions
│   └── images/
│       └── placeholder-book.jpg
└── README.md
```

## 🔧 Configuration

Edit `assets/js/config.js` to change API settings:

```javascript
const CONFIG = {
    API_BASE_URL: 'http://localhost:5000/api/v1',  // Change if needed
    // ...
};
```

## ✨ Features

### User Features
- ✅ User registration and login
- ✅ Browse books with filters (category, author, price)
- ✅ View book details with reviews
- ✅ Shopping cart management
- ✅ Checkout with shipping information
- ✅ Order history and tracking
- ✅ JWT authentication with token refresh

### UI/UX
- ✅ Fully responsive design (mobile, tablet, desktop)
- ✅ Toast notifications for user feedback
- ✅ Loading states and error handling
- ✅ Star rating system
- ✅ Cart badge with item count
- ✅ Clean, bookstore-themed aesthetics

## 📦 Pages Overview

| Page | Description | Auth Required |
|------|-------------|---------------|
| `index.html` | Landing page with featured books | No |
| `books.html` | Browse all books with filters | No |
| `book-detail.html` | Single book details & reviews | No |
| `cart.html` | Shopping cart | Yes |
| `checkout.html` | Checkout form | Yes |
| `orders.html` | Order history | Yes |
| `login.html` | User login | No |
| `register.html` | User registration | No |

## 🔐 Authentication Flow

1. User registers or logs in
2. JWT tokens stored in localStorage
3. Access token attached to protected API calls
4. Automatic token refresh on expiry
5. Logout clears all stored data

## 🎯 API Integration

All API calls go through `assets/js/api.js`:

```javascript
// Example: Get books with filters
const books = await getBooks({
    category_id: 'uuid',
    min_price: 10,
    max_price: 50
});

// Example: Add to cart
await addToCart(bookId, quantity);
```

## 🌐 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 📝 Development Notes

### Adding New Features

1. **Add API endpoint** in `config.js`:
   ```javascript
   ENDPOINTS: {
       NEW_FEATURE: '/new-feature'
   }
   ```

2. **Create API function** in `api.js`:
   ```javascript
   async function getNewFeature() {
       return await apiGet(ENDPOINTS.NEW_FEATURE);
   }
   ```

3. **Use in HTML pages** with inline `<script>` tags

### Styling Guidelines

- Colors defined in CSS variables (`:root`)
- Bootstrap 5 classes for layout
- Custom classes in `style.css` for theme
- Responsive breakpoints: 768px (tablet), 992px (desktop)

## 🐛 Troubleshooting

### CORS Issues
Ensure Flask API has CORS enabled:
```python
from flask_cors import CORS
CORS(app)
```

### API Connection Failed
Check `config.js` - ensure `API_BASE_URL` matches your Flask server.

### Cart Not Updating
Clear browser localStorage and refresh:
```javascript
localStorage.clear();
```

## 📚 Libraries Used (CDN)

- **Bootstrap 5.3** - UI framework
- **Font Awesome 6.4** - Icons
- **Google Fonts** - Typography (Playfair Display, Lato)

No npm packages or build tools required!

## 🚀 Deployment

### Option 1: Static Hosting
Deploy to Netlify, Vercel, or GitHub Pages. Update `API_BASE_URL` in `config.js` to production API.

### Option 2: Serve with Flask
Place frontend in Flask's `static` folder and serve index.html.

## 📄 License

Part of the Flask Bookstore API project.

## 🎉 Enjoy Your Bookstore!

Happy reading! 📚✨
