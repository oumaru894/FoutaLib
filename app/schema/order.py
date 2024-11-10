from app import ma
from app.model import Orders, OrderItems, OrderStatus
from marshmallow import fields
from marshmallow_enum import EnumField


class OrderItemSchema(ma.SQLAlchemyAutoSchema):
    price = fields.Decimal(as_string=True)
    class Meta:
        model = OrderItems
        
""" class ShippingAddressSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ShippingAddress
       """
       
        
class OrderSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Nested(OrderItemSchema, many=True)
    #shipping_address = ma.Nested(ShippingAddressSchema)
    total_price = fields.Decimal(as_string=True)
    status = EnumField(OrderStatus, by_value=True)
    
    class Meta:
        model = Orders
        dump_only = ("id",)
        include_fk = True
        load_instance = True
        include_relationship = True
