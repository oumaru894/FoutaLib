
from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
import json
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum



class User(db.Model, UserMixin):
    '''creating database table for user'''
    __tablename__= 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200), unique=False)
    user_type = db.Column(db.String(50), nullable=True, default='client')
    displayed_name = db.Column(db.String(100), unique= False)
    first_name = db.Column(db.String(50), unique= False)
    last_name = db.Column(db.String(50), unique= False)
    country = db.Column(db.String(50), unique= False)
    region = db.Column(db.String(50), unique= False)
    contact = db.Column(db.Integer, unique= False)
    address = db.Column(db.String(50), unique= False)
    profile = db.Column(db.String(200), unique= False, default='profile.jpg')
    cover_pic = db.Column(db.String(50), unique= False,  default='profile.jpg')
    date_created = db.Column(db.DateTime, nullable= False, default=datetime.utcnow)
    uid = db.Column(db.String(200), unique=True)
    
    
    products = relationship('Product', back_populates='vendor')
    order = relationship('Orders', back_populates='user')
    

    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def set_password(self, password: str):
        self.password = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password, password)
    

    
    @classmethod
    def find_by_id(cls, _id: int) -> "User":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_username(cls, username: str) -> "User":
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_email(cls, email: str) -> "User":
        return cls.query.filter_by(email=email).first()
    @classmethod
    def serialize(cls):
        return {
            "id": cls.id,
            "email": cls.email,
            "username": cls.username,
            "displayed_name": cls.displayed_name
           
        }

    
class Product(db.Model):
    '''creating table for user'''
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, ForeignKey('user.id'))
    name =db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text)
    specification = db.Column(db.String(500))
    quantity = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Integer, nullable=True) 
    images = db.Column(db.String(500),)
    category = db.Column(db.Integer, ForeignKey('category.id'))
    brand = db.Column(db.Integer, ForeignKey('brand.id'))
    #review_id = db.column(db.Integer, ForeignKey('review.review_id'))
    status = db.Column(db.Boolean(), nullable=True)
    discount = db.Column(db.Integer)
    colors = db.Column(db.String(300))
    brand = db.Column(db.String(50))
    date_added  = db.Column(db.DateTime, default=datetime.utcnow)
    user_type = db.Column(db.String(50), default="client")
    username = db.Column(db.String(50), unique= True)
    
    review = relationship("Review", back_populates="product")
    vendor = relationship('User', back_populates='products')
    order_items = relationship(
        'OrderItems',
        back_populates='product',
        cascade='all, delete-orphan'
    )
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
        
    def set_main_image(self,image:str):
        self.images = image
        
    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_seller_id(cls, seller_id: int) -> "Product":
        return cls.query.filter(cls.vendor_id==seller_id).all()
    
    
    @classmethod
    def find_by_category_id(cls, seller_id: int) -> "Product":
        return cls.query.filter(cls.category==seller_id).all()
class UserProfile(db.Model):
    '''creating table for user profile'''
    __tablename__ = 'profile'
    profile_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    profile_pic = db.Column(db.String(50))
    bio = db.Column(db.String(500))
    cover_pic = db.Column(db.String(50))
    contact_info = db.Column(db.String(200))
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def find_by_id(cls, _id: int) -> "UserProfile":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_user_id(cls, _id:int) -> "UserProfile":
        return cls.query.filter_by(profile_id=_id).first()
 
   
           
""" 
class Transaction(db.Model):
    '''Creating table for transaction'''
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, ForeignKey('user.id'))
    seller_id = db.Column(db.Integer, ForeignKey('user.id'))
    transaction_type =db.Column(db.Integer, ForeignKey('user.id'))
    transaction_amount = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def find_by_id(cls, _id: int) -> "Transaction":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_seller_id(cls, seller_id: int) -> "Transaction":
        return cls.query.filter_by(seller_id=seller_id).first()
    
    @classmethod
    def find_by_buyer_id(cls, buyer_id: int) -> "Transaction":
        return cls.query.filter_by(buyer_id=buyer_id).first()
    
    
 
    
 
class Message(db.Model):
    '''Creeating table for messages'''
    __tablename__ = 'message'
    message_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, ForeignKey('user.id'))
    content = db.Column(db.String(1000))
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def find_by_id(cls, _id: int) -> "Message":
        return cls.query.filter_by(message_id=_id).first()
    
    @classmethod
    def find_by_sender_id(cls, sender_id: int) -> "Message":
        return cls.query.filter_by(sender_id=sender_id).first()
    
    @classmethod
    def find_by_receiver_id(cls, receiver_id: int) -> "Message":
        return cls.query.filter_by(receiver_id=receiver_id).first()
    """
    
class Brand(db.Model):
    '''creatig table for breands'''
    __tablename__ ='brand'
    
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String(50), nullable=False)
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def find_by_id(cls, _id: int) -> "Brand":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_brandname(cls, name: str) ->"Brand":
        return cls.query.filter_by(brand_name=name).first()
   

class Review(db.Model):
    '''Creeating table for messages'''
    __tablename__ = 'review'
    review_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, ForeignKey('user.id'))
    product_id = db.Column(db.Integer, ForeignKey('product.id'))
    content = db.Column(db.Text)
    rating= db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    product = relationship("Product", back_populates="review")
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def find_by_id(cls, _id: int) -> "Review":
        return cls.query.filter_by(review_id=_id).first()
    
    @classmethod
    def find_by_sender_id(cls, sender_id: int) -> "Review":
        return cls.query.filter_by(sender_id=sender_id).first()
    
    @classmethod
    def find_by_procduct_id(cls, product_id: int) -> "Review":
        return cls.query.filter(cls.product_id==product_id).all()
    
    
class Category(db.Model):
    '''Creating category table'''
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    image_uri = db.Column(db.Text())
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def find_by_id(cls, _id: int) -> "Category":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_name(cls, name:str) -> "Category":
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_all(cls) -> list["Category"]:
        return cls.query.all()
    
    
class Cart(db.Model):
    '''Creating category table'''
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100) )
    price = db.Column(db.Integer)
    image_url = db.Column(db.String(250))
    quantity = db.Column(db.Integer,default=1)
    vendor_id=db.Column(db.Integer, ForeignKey('user.id'))
    client_id = db.Column(db.Integer, ForeignKey('user.id'))
    product_id = db.Column(db.Integer, ForeignKey('product.id'))
    total_price= db.Column(db.Integer)
    secondary_id= db.Column(db.Integer)
    
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def find_by_id(cls, _id: int) -> "Cart":
        return cls.query.filter_by(cart_id=_id).first()
    
    @classmethod
    def find_by_secondary_id(cls, _id: int) -> "Cart":
        return cls.query.filter_by(secondary_id=_id).first()
    @classmethod
    def find_by_product_id_and_client_id(cls,product_id:int, client_id:int) -> "Cart":
        return cls.query.filter_by(product_id=product_id,client_id=client_id).all()
    @classmethod
    def find_by_vendor_id(cls, sender_id: int) -> "Cart":
        return cls.query.filter_by(vendor_id=sender_id).first()

    @classmethod
    def find_by_client_id(cls, sender_id: int) -> "Cart":
        return cls.query.filter(cls.client_id==sender_id).all()
    
    @classmethod
    def find_by_procduct_id(cls, product_id: int) -> "Cart":
        return cls.query.filter(cls.product_id==product_id).first()


class OrderStatus(PyEnum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELED = "Canceled"


class Orders(db.Model):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    order_number = Column(String(50), unique=True, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_amount = Column(Float, nullable=False)
    invoice_number = Column(String(255), nullable=False, unique=True)
    
    # Relationships
    user = relationship("User", back_populates="order")
    items = relationship("OrderItems", back_populates="order", cascade="all, delete-orphan")
    #address = relationship("ShippingAddress", back_populates="order")
    
    # Shipping Information
    shipping_name = Column(String(100), nullable=False)
    shipping_address = Column(String(255), nullable=False)
    shipping_contact = Column(String(15), nullable=False)
    shipping_method = Column(String(50), nullable=True)
    shipping_cost = Column(Float, default=0.0)

    # Payment Information
    payment_method = Column(String(50), nullable=True)
    payment_status = Column(String(50), default="Pending")
    payment_date = Column(DateTime, nullable=True)
    
    # Timestamps for real-time tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    
    @classmethod
    def generate_order_number(cls):
        # Get today's date in YYYYMMDD format
        date_part = datetime.utcnow().strftime("%Y%m%d")
        prefix = "ORD"
        
        # Query the database for the highest order number of the day
        last_order = cls.query.filter(
            cls.order_date >= datetime.utcnow().date()
        ).order_by(cls.order_number.desc()).first()
        
        if last_order and last_order.order_number.startswith(f"{prefix}-{date_part}"):
            # Extract the sequential part of the last order number and increment it
            last_sequence = int(last_order.order_number.split("-")[-1])
            new_sequence = last_sequence + 1
        else:
            # Start at 1 if there are no orders for today
            new_sequence = 1

        # Format the order number as `ORD-YYYYMMDD-XXXX`
        order_number = f"{prefix}-{date_part}-{new_sequence:04}"
        return order_number 
    
    
    
    # generate invoice number
    @classmethod
    def generate_invoice_number(cls):
        # Get today's date in YYYYMMDD format
        date_part = datetime.utcnow().strftime("%Y%m%d")
        prefix = "INV"
        
        # Query the database for the highest invoice number for today
        last_order = cls.query.filter(
            cls.order_date >= datetime.utcnow().date()
        ).order_by(cls.invoice_number.desc()).first()
        
        if last_order and last_order.invoice_number.startswith(f"{prefix}-{date_part}"):
            # Extract the sequential part of the last invoice number and increment it
            last_sequence = int(last_order.invoice_number.split("-")[-1])
            new_sequence = last_sequence + 1
        else:
            # Start at 1 if there are no orders for today
            new_sequence = 1

        # Format the invoice number as `INV-YYYYMMDD-XXX`
        invoice_number = f"{prefix}-{date_part}-{new_sequence:03}"
        return invoice_number

    @classmethod
    def find_by_invoice(cls, invoice)->'Orders':
        return cls.query.filter(cls.invoice_number==invoice).order_by(cls.invoice_number.desc()).first()
        
    def save_to_db(self) -> None:  
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
    

    def __repr__(self):
        return f"<Order {self.order_number} - {self.status}>"


class OrderItems(db.Model):
    __tablename__ = 'order_items'
    
    id = Column(db.Integer, primary_key=True)
    order_id = Column(db.Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(db.Integer, ForeignKey('product.id'), nullable=False)
    product_name = Column(db.String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_item = Column(db.Float, nullable=False)
    total_price = Column(db.Float, nullable=False)

    # Relationships
    order = relationship("Orders", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    
    
    @classmethod
    def find_by_id(cls, _id: int) -> "OrderItems":
        return cls.query.filter_by(id=_id).first()
    

    def __repr__(self):
        return f"<OrderItem {self.product_name} x {self.quantity}>"

    

""" class ShippingAddress(db.Model):
    __tablename__ = 'shipping_addresses'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, ForeignKey('orders.id'))
    address = db.Column(db.String)

    country = db.Column(db.String)
    product_name = db.Column(db.String)
   

    order = relationship("Orders", back_populates="address")
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_id(cls, _id: int) -> "ShippingAddress":
        return cls.query.filter_by(id=_id).first()
 """

class Favorite(db.Model):
    '''Creating favorite table'''
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100) )
    price = db.Column(db.Integer)
    image_1 = db.Column(db.String(250))
    vendor_id=db.Column(db.Integer, ForeignKey('user.id'))
    client_id = db.Column(db.Integer, ForeignKey('user.id'))
    product_id = db.Column(db.Integer, ForeignKey('product.id'))
    

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def find_by_id(cls, _id: int) -> "Favorite":
        return cls.query.filter_by(cart_id=_id).first()
    
    @classmethod
    def find_by_sender_id(cls, sender_id: int) -> "Favorite":
        return cls.query.filter_by(vendor_id=sender_id).first()
    @classmethod
    def find_by_client_id(cls, sender_id: int) -> "Favorite":
        return cls.query.filter_by(client_id=sender_id).first()
    
    @classmethod
    def find_by_procduct_id(cls, product_id: int) -> "Favorite":
        return cls.query.filter(cls.product_id==product_id).all()


""" class Payment(db.Model):
    '''Creating table for transaction'''
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, ForeignKey('user.id'))
    vendor_id = db.Column(db.Integer, ForeignKey('user.id'))
    product_id = db.Column(db.Integer, ForeignKey('product.id'))
    amount = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    client_phone = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    product_name = db.Column(db.String, nullable=False)
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def find_by_id(cls, _id: int) -> "Payment":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_product_id(cls, product_id: int) -> "Payment":
        return cls.query.filter_by(product_id=product_id).first()
    
    @classmethod
    def find_by_seller_id(cls, seller_id: int) -> "Payment":
        return cls.query.filter_by(vendor_id=seller_id).first()
    
    @classmethod
    def find_by_buyer_id(cls, buyer_id: int) -> "Payment":
        return cls.query.filter_by(client_id=buyer_id).first()
    
 """

