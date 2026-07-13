from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models
from app.models.BaseModel import BaseModel
from app.models.User import User
from app.models.Author import Author
from app.models.Category import Category
from app.models.Book import Book
from app.models.CartItem import CartItem
from app.models.CartHistory import CartHistory
from app.models.OrderItem import OrderItem
from app.models.OrderDetails import OrderDetails
from app.models.Review import Review

__all__ = ['db', 'BaseModel', 'User', 'Author', 'Category', 'Book', 'CartItem', 'CartHistory', 'OrderItem', 'OrderDetails', 'Review']
