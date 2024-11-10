from datetime import datetime, timedelta
import json
from flask import request
from sqlalchemy.orm import joinedload
from sqlalchemy import desc
from flask_jwt_extended import (
    get_jwt,
    get_jwt_identity,
    jwt_required
)
import random
import string
from datetime import datetime

from app.model import Orders, OrderItems
from app.schema.order import OrderSchema
from flask_restful import Resource

order_schema = OrderSchema()
order_list_schema = OrderSchema(many=True)


class OrderAddResource(Resource):
    @classmethod
    def post(cls):
        order_data = request.get_json()
        #print('order:', order_data)
        
        # Extract order details
        client_name = order_data['billingInfo']['name']
        #invoice = order_data['invoice']
        total_amount = order_data['totalAmount']
        items = order_data['cartItems']  # List of item details
        shipping_method = order_data['shippingMethod']  # Shipping address details

        if shipping_method:
            # Create a new Order instance
            new_order = Orders(
            invoice_number=Orders.generate_invoice_number(),
            total_amount=total_amount,
            order_number=Orders.generate_order_number(),
            shipping_name=client_name,
            shipping_address=order_data['billingInfo']['address'],
            shipping_contact=order_data['billingInfo']['contact'],
            shipping_method=order_data['shippingMethod']
            )  
            
            
            # getting individual items
            for item in items:
                new_item = OrderItems(
                product_id=item['product_id'],
                quantity=item['quantity'],
                #vendor_id=item['vendor_id'],
                total_price=item['total_price'],
                price_per_item=item['price'],
                product_name=item['product_name'],
                #image_url=item['image_url'],
                #cart_id=item['cart_id']
            )
                new_order.items.append(new_item)
            
            try:
                new_order.save_to_db()
                return {'Invoice': new_order.invoice_number}, 201
            except Exception as e:
            
                return {'error': print(str(e))}, 500
        return{"message":"no data for items of shipping address"},500
      
class OrderResource(Resource):
    @classmethod
    def get(cls, _id: int):
        order = Orders.find_by_client_id(_id)
        if order:
            # Eagerly load the order items and shipping address
            order_with_items_and_address = Orders.query.options(joinedload(Orders.items), joinedload(Orders.address)).filter_by(client_id=_id).order_by(desc(Orders.order_date)).first()
            #print("check",order_with_items_and_address.items)
            if order_with_items_and_address:
                order_data = order_schema.dump(order_with_items_and_address)
                items_data = order_data["items"]
                for item_data in items_data:
                    item = OrderItems.find_by_id(item_data["id"])
                    item_data["product_id"] = item.product_id
                    item_data["vendor_id"] = item.vendor_id
                return order_data
        return {"message": "no order available"}, 400
    
class OrderUpdateResource(Resource):
    @classmethod
    def put(cls, _id):
        order_json = request.get_json()
        order = Orders.find_by_id(_id)
        if order:
            order.status = order_json["status"]
            order.save_to_db()
            return {"message":"order updated."}
        else:
            return {"message":"order not available."}
    
class OrderDeleteResource(Resource):
    @classmethod
    def delete(cls,_id:int):
        order = Orders.find_by_id(_id)
        if order:
            order.delete_from_db()
            return {"message": "order deleted."}
        return {"message": "order not found."}, 404
    
class InvoiceOrderResource(Resource):
    @classmethod
    def get(cls, invoice: str):
        # Retrieve the order by invoice
        order = Orders.find_by_invoice(invoice)
        
        if order:
            # Load the order along with items and address details
            order_with_items_and_address = (
                Orders.query.options(joinedload(Orders.items))
                .filter_by(invoice_number=invoice)
                .order_by(desc(Orders.order_date))
                .first()
            )
            
            if order_with_items_and_address:
                # Serialize order data with items and address
                order_data = order_schema.dump(order_with_items_and_address)
                
                # Iterate over items to fetch additional details, if needed
                for item_data in order_data.get("items", []):
                    item = OrderItems.find_by_id(item_data["id"])
                    if item:
                        item_data["product_id"] = item.product_id
                        #item_data["vendor_id"] = item.vendor_id
                
                return order_data, 200  # Return serialized order data and 200 OK

        # Return 404 if order is not found
        return {"message": "Order not found"}, 404