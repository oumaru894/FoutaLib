from datetime import datetime, timedelta
import json
from flask_login import login_user, logout_user, current_user
from app.model import User
#from app.forms import CustomerRegistrationForm, CustomerLoginFrom
from flask import request, session
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required
)
import firebase_admin
from firebase_admin import auth

from app.schema.user import UserSchema
from flask_restful import Resource

from firebase_admin import credentials




private_key = 'foutalib-f623a-firebase-adminsdk-xxkth-90bb923296.json'

# Initialize the Firebase Admin SDK
cred = credentials.Certificate(private_key)
firebase_admin.initialize_app(cred)

user_schema = UserSchema()

class UserRegisterResource(Resource):
    '''handle http request from schema'''
    @classmethod
    def post(cls):
        
        user = user_schema.load(request.get_json())
        
        if user:

            """ if user.find_by_username(user.username):
                return {"message": "A user with that username already exists."}, 400
             """
            if user.find_by_email(user.email):
                return {"message": "A user with that email already exists."}, 400
            
            user.user_name = user.email.split('@')[0]
            print(user.user_name)
            
            user.set_password(user.password)

            user.save_to_db()
            return {"message":"user was created"}

        return {"message": "User not created"}, 500


class UserLogin(Resource):
    #@jwt_required()
    @classmethod
    def post(self):
        # Get the user's ID token from the request
        id_token = request.json.get("idToken")

        try:
            # Verify the ID token
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            email = decoded_token['email']
            display_name = decoded_token.get('name', '')
            #print('token: ', decoded_token)
            
            # Check if user already exists in your database
            user = User.find_by_email(email)
            if not user:
                # Create a new user in your database
                user = User(
                    uid=uid,
                    email=email,
                    username=email.split('@')[0],  # Create a username from email
                    displayed_name=display_name
                )
                login_user(user)
                print(user)
                user.save_to_db()
            else: 
                login_user(user)
                session['user_id'] = user.id
                print("session['user_id']: ", session['user_id'])
                print("Current User:", current_user.is_authenticated)
            return {"message": "User authenticated", "user": 
                    {
                        ""
                    }
                    }, 200
        
        except Exception as e:
            print(e)
            return {"message": str(e)}, 400


class UserProfileResource(Resource):
    @classmethod
    def get(cls, id):
        profile = User.find_by_id(id)
        
        if not profile:
            return {"message": "user not found"}, 404
        return user_schema.dump(profile), 200
     

class UserPasswordUpdateResource(Resource):
    @classmethod
    def put(cls):
        user_data = user_schema.load(request.get_json())

        user = User.find_by_email(user_data.email)

        if user: 
            user.set_password(user_data.password)
            user.save_to_db()
        else:
            return {"message": "user not found"}, 404
        return user_schema.dump(user), 200
    
class VendorRegistrationResource(Resource):
    @classmethod
    def put(cls):
        user_data = user_schema.load(request.get_json())

        user = User.find_by_email(user_data.email)
        print(user_data.user_type)
        if user and user.check_password(user_data.password): 
            user.user_type = "vendor"
            user.contact = user_data.contact
            
            user.save_to_db()
        else:
            return {"message": "user not found"}, 404
        return user_schema.dump(user), 200

class AllUserResource(Resource):
    @classmethod
    def get(cls): 
        users = User.query.with_entities(User.id, User.displayed_name, User.email, User.username, User.uid, User.date_created).all()
        return user_schema.dump(users, many=True), 200



class AdminLoginResource(Resource):
    #@jwt_required()
    @classmethod
    def post(self):
        # Get the user's ID token from the request
        user_data = request.get_json()

        try:
            # Verify the ID token
            #decoded_token = auth.verify_id_token(id_token)
            #uid = decoded_token['uid']
            email = user_data['email']
            password_data = user_data['password']
            #print('token: ', decoded_token)
            
            # Check if user already exists in your database
        
            user = User.find_by_email(email)
            if user and user.check_password(password_data):
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(user.id)
                
                login_user(user)
                
                return{
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "id":user.id,
                    "displayed_name":user.displayed_name,
                    "emial":user.email,
                    "username":user.username,
                    "user_type":user.user_type
                }
                
            return {"message": "User authenticated"}, 200
        
        except Exception as e:
            print(e)
            return {"message": str(e)}, 400
        



class AdminRegisterResource(Resource):
    '''handle http request from schema'''
    @classmethod
    def post(cls):
        
        user = user_schema.load(request.get_json())
        
        if user:

            """ if user.find_by_username(user.username):
                return {"message": "A user with that username already exists."}, 400
             """
            if user.find_by_email(user.email):
                return {"message": "A user with that email already exists."}, 400
            
            user.user_name = user.email.split('@')[0]
            user.user_type = "admin"
            print(user.user_name)
            
            user.set_password(user.password)

            user.save_to_db()
            return {"message":"user was created"}

        return {"message": "User not created"}, 500

