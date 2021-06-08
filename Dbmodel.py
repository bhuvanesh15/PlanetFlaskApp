from mongoengine import *

connect(db='PlanetList', host='127.0.0.1', port=27017)


class username(Document):
    #__tablename__ = "users"
    id = StringField(required=True)
    first_name = StringField(max_length=10, required=True)
    last_name = StringField(max_length=5, required=True)
    email = StringField(max_length=10, required=True)
    password = StringField(max_length=20, required=True)


class planets(Document):
   # __tablename__ = "planet"
    planet_id = StringField( required=True)
    planet_name = StringField( required=True)
    planet_type = StringField(required=True)
    home_star = StringField(required=True)
    mass = StringField(required=True)
    radius = StringField(required=True)
    distance = StringField(required=True)