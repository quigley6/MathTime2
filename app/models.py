from app import db, login
from base64 import b64encode
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return Player.query.get(int(id))

class Player(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    streak = db.Column(db.Integer)
    settings = db.Column(db.JSON)

# class Material(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     description = db.Column(db.String(120))
#     cost = db.Column(db.Float)
#     purchase_date = db.Column(db.DateTime)
#     item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
#     item_used = db.relationship('Item', back_populates='materials')

#     def __repr__(self):
#         return '<Material {}, {}, {}>'.format(self.id, self.description, self.cost)

#     def json(self):
#         return {
#             'id' : self.id,
#             'description' : self.description,
#             'cost' : self.cost,
#             'purchase_date' : self.purchase_date,
#             'item_id' : self.item_id
#         }

# class Item(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120))
#     materials = db.relationship('Material', back_populates='item_used')
#     create_date = db.Column(db.DateTime)
#     listings = db.relationship('Listing', back_populates='item')
#     picture = db.Column(db.LargeBinary)

#     def __repr__(self):
#         return '<Item {} {}>'.format(self.id, self.name)

#     def json(self):
#         return {
#             'id' : self.id,
#             'name' : self.name,
#             'materials' : [x.id for x in self.materials],
#             'listings' : [x.id for x in self.listings],
#             'picture' : b64encode(self.picture).decode('ascii')
#         }

# class Listing(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(256))
#     item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
#     item = db.relationship('Item', back_populates='listings')
#     list_cost = db.Column(db.Float)
#     list_price = db.Column(db.Float)
#     sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'))
#     expiration = db.Column(db.DateTime)
#     expired = db.Column(db.Boolean)

#     def __repr__(self):
#         return '<Listing {} {} {} {} {} {} {}>'.format(self.id, self.title, self.item.id, self.list_cost, self.list_price, self.expiration, self.expired)

#     def json(self):
#         return {
#             'id' : self.id,
#             'title' : self.title,
#             'item' : self.item_id,
#             'list_cost' : self.list_cost,
#             'list_price' : self.list_price,
#             'sale' : self.sale_id,
#             'expiration' : self.expiration,
#             'expired' : self.expired
#         }

# class Sale(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     listing = db.relationship('Listing')
#     sale_date = db.Column(db.DateTime)
#     shipping_info = db.Column(db.String(256))
#     shipping_cost = db.Column(db.Float)

#     def __repr__(self):
#         return '<Sale {} {} {} {} {}>'.format(self.id, self.listing, self.sale_date, self.shipping_info, self.shipping_cost)

#     def json(self):
#         return {
#             'id' : self.id,
#             'listing' : self.listing.id,
#             'sale_date' : self.sale_date,
#             'shipping_info' : self.shipping_info,
#             'shipping_cost' : self.shipping_cost
#         }




    