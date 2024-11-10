from datetime import datetime, timedelta
import json
import secrets
from app import search
#from flask_login import login_required
from sqlalchemy.orm import joinedload
from app.libs.strings import gettext
from app.libs import image_helper
from app import current_user
from flask_uploads import UploadNotAllowed
from app.model import Product, Brand, Category, Orders as CustomerOrder, User
from flask import request,session,redirect, flash,jsonify, send_file
from flask_jwt_extended import (
    get_jwt,
    get_jwt_identity,
    jwt_required
)
import os

from app.schema.product import ProductSchema
from flask_restful import Resource


product_schema = ProductSchema()

def only_name(path):
    name = str()
    for i in path:
        if i == '\\' or i == '/':
            name = path[i:1]
            return name
            
        else:
            return path


class AddProductResource(Resource):
    '''Handle HTTP request from schema'''
    @classmethod
    def post(cls):
        # Convert form data into a dictionary
        product = request.get_json()
        #print(product['images'])
        if product:
            
            print("product: ", product)
            try:
                print("category: ", product)

                # Create a Product object from the dictionary and save to the database
                new_product = product_schema.load(product)
                
                # Save the product to the database
                product_instance = Product(**new_product)  
                product_instance.save_to_db()
                print("product:", product_instance.id)

                return {"id":product_instance.id}, 201

            except UploadNotAllowed:
                extension = image_helper.get_extension(request.files.get('image_1'))
                return {
                    "message": gettext("image_illegal_extension").format(extension)
                }, 400

        return {"message": "Product not created"}, 400

   
class ProductView(Resource):
    @classmethod
    def get(cls):
        products = Product.query.all() #add additional order by rating later in development
        
        if products:
            product_data = [product_schema.dump(product) for product in products]
            return jsonify(product_data)
        return {"message":"no product available"},400
        


# product of a seller
class VendoersProductView(Resource):
    @classmethod
    def get(cls, id):
        
        products = Product.find_by_seller_id(id) #add additional order by rating later in development
        if products:
            product_data = [product_schema.dump(product) for product in products]
            return jsonify(product_data)
        return {"message":"no product available"}
        
    
class SingleProductResource(Resource):
    @classmethod
    def get(cls,id):
        main_product = Product.find_by_id(id)
        sup_product = Product.query.filter_by(name=main_product.name)
        related_products = Product.query.filter(
        Product.category == main_product.category, 
        Product.id != main_product.id
        ).all()
        product = product_schema.dump(main_product)
        return jsonify(product)

class SearchProduct(Resource):
    @classmethod
    def get(cls):
    #selecting input from search
        searchword = request.args.get("q")
        print(searchword)
        #quarying database for search items
        products = Product.query.msearch(searchword, fields=['product_name','desc'])
        product = [product_schema.dump(product) for product in products]      
        return jsonify(product)
        
#category seach
class CategoryProductView(Resource):
    @classmethod
    def get(cls, id):
        
        products = Product.find_by_category_id(id) #add additional order by rating later in development
        if products:
            product_data = [product_schema.dump(product) for product in products]
            return jsonify(product_data)
        return {"message":"no product available"}
        


#delete  product
class DeleteProductResource(Resource):
    @classmethod
    def delete(cls, id):
        product = Product.find_by_id(id)
        
        if product:
            # Define folder based on product_id
            folder = f"product_{id}"
            
            # Attempt to delete all images associated with the product
            try:
                image_files = image_helper.get_all_files_in_folder(folder)
                
                for image_file in image_files:
                    os.remove(image_helper.get_path(image_file, folder))
                #print(f"Deleted images for product {id} in folder {folder}")
            except Exception as e:
                #print(f"Error deleting images: ")
                return {"message": "Failed to delete product images"}, 500
            
            # Delete the product from the database
            product.delete_from_db()
            return {"message": "Product and associated images deleted successfully"}, 200
        
        return {"message": "Product not found"}, 404


