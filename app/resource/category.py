from datetime import datetime, timedelta
import json
from flask import request, jsonify
from flask_jwt_extended import (
    get_jwt,
    get_jwt_identity,
    jwt_required
)

from app.model import Category
from app.schema.category import CategorySchema
from flask_restful import Resource
from app.libs import image_helper

category_schema = CategorySchema()

class CategoryResource(Resource):
    '''handle http request from schema'''
    @classmethod
    def get(cls):
        categories = Category.query.all()
        if categories:
            category = [category_schema.dump(category) for category in categories]       
            return jsonify(category) 
        return {"message":"no category avaliable"}, 400
    
class AddCategoryResource(Resource):
    @classmethod
    def post(cls):
        # Access form data directly from the request
        category_name = request.form.get('name')  # Replace 'name' with the actual field name for category
        image_file = request.files.get('image_uri')  # Replace 'image_uri' with the actual file field name
        folder = f"category/{category_name}"

        # Check if category name and image are provided
        if not category_name or not image_file:
            return {"message": "Category name and image are required"}, 400

        # Simulate category existence check (uncomment the actual logic if you have it)
        if Category.find_by_name(category_name):
             return {"message": "Category already exists"}, 400

        # Save the new category (uncomment the actual saving logic if available)
        image_path = image_helper.save_image(image_file,folder=folder, name=f'{category_name}.')
        category = Category(name=category_name, image_uri=image_path.split('/')[2])
        
        category.save_to_db()

        return {"message": "Category added successfully"}, 201
    
    