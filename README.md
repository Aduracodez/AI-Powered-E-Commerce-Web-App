# 👑 The Queens

A full-stack e-commerce web application with a Python Flask backend and React frontend.

## Features

- **User Authentication**: Register and login functionality
- **Product Catalog**: Browse products by category and search
- **Shopping Cart**: Add, update, and remove items from cart
- **Order Management**: Place orders and view order history
- **Responsive Design**: Modern, mobile-friendly UI

## Tech Stack

### Backend
- Python 3
- Flask
- SQLAlchemy (Database ORM)
- Flask-JWT-Extended (Authentication)
- Flask-Bcrypt (Password hashing)
- Flask-CORS (Cross-origin requests)

### Frontend
- React
- React Router (Routing)
- Axios (HTTP client)
- CSS3 (Styling)

## Project Structure

```
E_commerce_website/
├── backend/
│   ├── app.py                 # Flask application
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Page components
│   │   ├── context/          # React context (Auth)
│   │   ├── App.js
│   │   └── index.js
│   └── package.json          # Node dependencies
└── README.md
```

## Installation & Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/register` - Register a new user
- `POST /api/login` - Login user

### Products
- `GET /api/products` - Get all products (supports `?category=` and `?search=` query params)
- `GET /api/products/<id>` - Get product by ID

### Cart (Requires Authentication)
- `GET /api/cart` - Get user's cart items
- `POST /api/cart` - Add item to cart
- `PUT /api/cart/<id>` - Update cart item quantity
- `DELETE /api/cart/<id>` - Remove item from cart

### Orders (Requires Authentication)
- `GET /api/orders` - Get user's orders
- `POST /api/orders` - Create a new order

## Database

The application uses SQLite by default (stored as `ecommerce.db` in the backend directory). The database will be automatically created on first run and seeded with sample products.

### Models
- **User**: User accounts with authentication
- **Product**: Product catalog
- **CartItem**: Shopping cart items
- **Order**: Customer orders
- **OrderItem**: Items in each order

## Default Sample Products

The application comes with 6 sample products:
- Wireless Headphones (Electronics)
- Smart Watch (Electronics)
- Running Shoes (Fashion)
- Laptop Backpack (Accessories)
- Coffee Maker (Home)
- Yoga Mat (Fitness)

## Usage

1. Start both backend and frontend servers
2. Visit `http://localhost:3000` in your browser
3. Register a new account or use existing credentials
4. Browse products, add them to cart, and place orders

## Environment Variables (Optional)

Create a `.env` file in the backend directory for production:

```
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///ecommerce.db
JWT_SECRET_KEY=your-jwt-secret-key
```

## Notes

- For production deployment, change the secret keys and use a production-grade database (PostgreSQL, MySQL, etc.)
- The CORS is configured to allow requests from `http://localhost:3000`
- JWT tokens expire after 24 hours

## License

MIT

