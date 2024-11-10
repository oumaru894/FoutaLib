from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import send_file, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback
import os

from app.libs import image_helper
from app.libs.strings import gettext
from app.schema.image import ImageSchema
from app.schema.product import ProductSchema
from app.model import Product

product_shema = ProductSchema

image_schema = ImageSchema()



class ImageUpload(Resource):
    @classmethod
    def post(cls, product_id: int):
        # Get the files from the request
        data = request.files

        # Define folder based on product_id
        folder = f"product_{product_id}"

        try:
            # Check if any files exist in the request
            if 'images' in data:
                # Loop through each file under the 'images' key
                for index, file in enumerate(data.getlist('images')):
                    # Save each image with a unique name
                    image_path = image_helper.save_image(
                        file, 
                        folder=folder, 
                        name=f"{product_id}_{index}"+"."
                    )
                        
                        
                    print(f"Saved image: {image_path}")
                
                return {"message": gettext("image_uploaded")}, 201
            else:
                return {"message": "No images found in the request"}, 400

        except UploadNotAllowed:
            # Handle illegal extension
            extension = image_helper.get_extension(data['images'])
            return {
                "message": gettext("image_illegal_extension").format(extension)
            }, 400

class Image(Resource):
    @classmethod
    def get(cls, product_id: int):
        # Get all images for a specific product
        folder = f"product_{product_id}"

        # Check if the folder exists and get a list of all images in the folder
        image_files = image_helper.get_all_files_in_folder(folder)

        if not image_files:
            return {"message": gettext("no_images_found_for_product").format(product_id)}, 404

        # Generate URLs for each image
        image_urls = [image_helper.get_url_for_image(file, folder) for file in image_files]
        print('imageuls: ', image_urls)

        return {"images": image_files}, 200


    @classmethod
    def delete(cls, filename: str, user_id: int):
        # Delete an image for a user or product
        folder = f"user_{user_id}"
        if not image_helper.is_filename_safe(filename):
            return {"message": gettext("image_illegal_file_name").format(filename)}, 400
        try:
            os.remove(image_helper.get_path(filename, folder=folder))
            return {"message": gettext("image_deleted").format(filename)}, 200
        except FileNotFoundError:
            return {"message": gettext("image_not_found").format(filename)}, 404
        except:
            traceback.print_exc()
            return {"message": gettext("image_delete_failed")}, 500

class SpecificImage(Resource):
    @classmethod
    def get(cls, filename: str, product_id: int):
        folder = f"product_{product_id}"

        
        # find image path in any format
        image = image_helper.find_image_any_format(filename, folder)
        if not image:
            image = image_helper.get_path(filename, folder)
        
        #print("image: ",image)
        
        # Check if the filename is safe
        try:
            if image:
                """ file_path = image_helper.get_path(image, folder=folder) """
                return send_file(
                "../" + image,
                mimetype="image/jpeg",
                as_attachment=True,
                #achment_filename=filename,
          
            )
                print("image: ",image)
            else:
                return {"message": "Image not found"}, 400

        except FileNotFoundError:
            return {"message": gettext("image_not_found").format(filename)}, 404
        
        
        
class ImageByPath(Resource):
    @classmethod
    def get(cls, relative_path: str, product:str):
        """
        Takes a relative path and returns the image file using Flask's send_file.
        Example relative path: /images/product_1/1_0.jpeg
        """
        # Base directory for your images (adjust this as needed based on your setup)
        base_directory = '../static/images'

        # combining the with path
        combined_path = os.path.join(product, relative_path)

        # Clean up the relative path to avoid directory traversal attacks
        safe_relative_path = combined_path.lstrip('/')

        # Create the absolute path for the file
        absolute_path = os.path.join(base_directory, safe_relative_path)

        # Check if the file exists
        if not os.path.isfile(absolute_path):
            abort(404, description="Image not found")

        # Use Flask's send_file to return the image file
        return send_file(absolute_path, mimetype='image/jpeg', as_attachment=False)


class AvatarUpload(Resource):
    # @jwt_required()
    def put(cls, user_id: int):
        # endpoint used to upload user avaters; named after user's ID.
        # new one overrides old one
        print(request.files)
        data = image_schema.load(request.files)
        filename = f"user_{user_id}"
        folder = "avatar"
        
        avatar_path = image_helper.find_image_any_format(filename, folder)
        if avatar_path:
            try:
                os.remove(avatar_path)
            except:
                return {"message": gettext("avatar_delete_failed")}, 500
        try:
            ext = image_helper.get_extension(data["image"].filename)
            avatar = filename + ext
            avatar_path = image_helper.save_image(
                data["image"], folder=folder, name=avatar
            )
            basename = image_helper.get_basename(avatar_path)
            return {"message": gettext("avatar_uploaded").format(basename)}, 200
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {
                "message": gettext("image_illegal_extension").format(extension)
            }, 400


class Avatar(Resource):
    @classmethod
    def get(cls, user_id: int):
        folder = "avatar"
        filename = f"user_{user_id}"
        avatar = image_helper.find_image_any_format(filename, folder)
        if avatar:
            print(send_file(
                "../" + avatar,
                mimetype="image/jpeg",
                #as_attachment=True,
                ))
            return send_file(
                "../" + avatar,
                mimetype="image/jpeg",
                as_attachment=True,
                #achment_filename=filename,
          
            )
        default = image_helper.find_image_any_format("default", "defaultUser")
        return send_file(
                "../" + default,
                mimetype="image/jpeg",
                as_attachment=True,
                #achment_filename=filename,
        )
        


class CategoryImage(Resource):
    @classmethod
    def get(cls, name: str, image_uri: str):
        folder = f"category/{name}"

        
        # find image path in any format
        image = image_helper.find_image_any_format(name, folder)
        if not image:
            image = image_helper.get_path(name, folder)
        
        print("image: ",image)
        
        # Check if the filename is safe
        #try:
        if image:
            """ file_path = image_helper.get_path(image, folder=folder) """
            return send_file(
            "../" + image,
            mimetype="image/jpeg",
            as_attachment=True,
            #achment_filename=filename,
        
        )
            print("image: ",image)
        else:
            return {"message": "Image not found"}, 400

        #except FileNotFoundError:
        return {"message": gettext("image_not_found").format(name)}, 404
        
   