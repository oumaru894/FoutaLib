from datetime import datetime, timedelta
import json
from flask import request, jsonify
from flask import session
#from flask_session import Session
from flask_jwt_extended import (
    get_jwt,
    get_jwt_identity,
    jwt_required
)

from flask_login import login_user, current_user, logout_user, login_required

from app.model import Cart
from app.schema.cart import CartSchema
from flask_restful import Resource

cart_schema = CartSchema()
cart_list_schema = CartSchema(many=True)



    
class CartResource(Resource):
    #@login_required
    @classmethod

    def get(cls,_id:int):
        carts = Cart.find_by_client_id(_id)
        if carts:
            #cart = [cart_schema.dump(cart) for cart in carts]       
            return cart_list_schema.dump(carts) 
        return {"message":"no cart avaliable"}, 400
    
class CartUpdateResource(Resource):
    @classmethod
    def put(cls, _id):
        
        cart_json = request.get_json()
        cart = Cart.find_by_id(_id)
        print(cart_json)
        if cart:
            #print(exist.cart_id)
            cart.quantity = cart_json["quantity"]
            print("new",cart.quantity)
            cart.save_to_db()
            return {"message":"cart updated."}
        else:
            return {"message":"cart not available."}
    
class CartDeleteResource(Resource):
    @classmethod
    def delete(cls,_id:int):
        print(_id,'id')
        cart = Cart.find_by_id(_id)
        
        if cart:
            cart.delete_from_db()
            
            return {"message": "cart deleted."}
        return {"message": "cart not found."}, 404


class AddCartResource(Resource):
    @classmethod
    def post(cls):
        cart_data = request.get_json()
        cart = cart_schema.load(cart_data)
        
        if not cart:
            return {"message": "Invalid cart data"}, 400

        product_id = cart_data["product_id"]
        
        #if current_user.is_authenticated:
        #cart.client_id = current_user.id
        # Check if the cart item already exists for the user and product
        existing_cart = Cart.find_by_product_id_and_client_id(product_id, cart_data["client_id"])
        if existing_cart:
            # Update quantity or return a message about its existence
            return {"message": "Item already in cart"}, 204
        #else:
        # Store in session if the user is not logged in
        """ session["cart"] = session.get("cart", []) + [cart_data]
        return {"message": "Cart saved to session for guest"}, 201 """

        # Save to DB if authenticated and unique
        cart.save_to_db()
        return {"message": "Cart item added successfully"}, 201
     
    

