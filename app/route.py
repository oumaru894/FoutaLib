from app import api
#from app.resources.brand import BrandResource
from app.resource.category import CategoryResource, AddCategoryResource
#from app.resources.job import AddJobResource
#from app.resources.message import MessageResource
#from app.resources.brand import BrandResource
from app.resource.order import OrderResource
from app.resource.profile import ProffileResource
#from app.resource.transaction import TransactionResource
from app.resource.product import AddProductResource, SingleProductResource,ProductView, SearchProduct, VendoersProductView, \
    CategoryProductView, DeleteProductResource
from app.resource.user import UserRegisterResource, UserLogin, VendorRegistrationResource, AllUserResource, UserProfileResource, AdminLoginResource, AdminRegisterResource
from app.resource.image import Image, AvatarUpload, Avatar, ImageUpload, SpecificImage, ImageByPath, CategoryImage
from app.resource.review import ReviewResources,AddReviewResources,ReviewUpdateResource, ReviewDeleteResource
from app.resource.cart import CartResource, AddCartResource, CartUpdateResource, CartDeleteResource
from app.resource.order import OrderResource, OrderDeleteResource, OrderUpdateResource, OrderAddResource, InvoiceOrderResource
#from app.resource.payment import PaymentResource, GetPaymentResource
from app.resource.favorite import AddFavoriteResourse,FavoriteDeleteResource, FavoriteResource,FavoriteUpdateResource






#product resource routes
api.add_resource(ProductView, '/product') #product route
api.add_resource(SearchProduct, '/search') #search route
api.add_resource(UserRegisterResource, '/add-user') #register user route
api.add_resource(UserLogin,'/login')
api.add_resource(AdminLoginResource, '/admin-login')
api.add_resource(AdminRegisterResource, '/admin-register')
api.add_resource(DeleteProductResource, '/delete-product/<int:id>')


#api.add_resource(BrandResource, '/brand')
api.add_resource(AddProductResource, '/add-product')
api.add_resource(AllUserResource, '/all-user')
api.add_resource(SingleProductResource, '/single-product/<int:id>')
api.add_resource(VendoersProductView, '/vendorsproduct/<int:id>')
api.add_resource(CategoryResource, '/category')

#image
api.add_resource(Image, "/images/<int:product_id>")
api.add_resource(SpecificImage, "/image/<string:filename>/<int:product_id>")
api.add_resource(ImageUpload, "/upload-image/<int:product_id>")
api.add_resource(Avatar,"/avatar/<int:user_id>")
api.add_resource(AvatarUpload,"/avatar-upload/<int:user_id>")
api.add_resource(CategoryImage, "/cat-image/<string:name>/<string:image_uri>")

#api.add_resource(ImageByPath, "/image-path/images/<string:product>/<string:relative_path>")

api.add_resource(ReviewResources, "/review/<int:product_id>")
api.add_resource(AddReviewResources, "/review-add")
api.add_resource(ReviewUpdateResource, "/review-update/<int:_id>")
api.add_resource(ReviewDeleteResource, "/review-delete/<int:_id>")
api.add_resource(AddCartResource, "/cart-add")
api.add_resource(CartResource, "/cart/<int:_id>")
api.add_resource(CartUpdateResource, "/cart-update/<int:_id>")
api.add_resource(CartDeleteResource, "/cart-delete/<int:_id>")


api.add_resource(InvoiceOrderResource, "/invoice/<string:invoice>")
api.add_resource(OrderResource, "/order/<int:_id>")
api.add_resource(OrderAddResource, "/order-add")
api.add_resource(OrderUpdateResource, "/order-update/<int:_id>")
api.add_resource(OrderDeleteResource, "/order-delete/<int:_id>")
""" api.add_resource(PaymentResource, "/add-payment")
api.add_resource(GetPaymentResource,"/payment/<int:_id>")
 """
api.add_resource(UserProfileResource,"/vendor/<int:id>")

api.add_resource(AddFavoriteResourse,"/add-favorite")
api.add_resource(FavoriteResource,"/favorite/<int:_id>")
api.add_resource(FavoriteDeleteResource,"/delete-favorite/<int:_id>")
api.add_resource(FavoriteUpdateResource,"/update-favorite/<int:_id>")

api.add_resource(VendorRegistrationResource,"/vendor-register")



# category routes
api.add_resource(CategoryProductView,"/category-products/<int:id>")
api.add_resource(AddCategoryResource,"/add-category")