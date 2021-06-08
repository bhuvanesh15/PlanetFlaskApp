from mongoengine import connect
from Dbmodel import planets,username

def planet_add (value):
    planeToadd = planets()
    planeToadd.planet_id = value[0]
    planeToadd.planet_type=value[1]
    planeToadd.planet_name = value[2]
    planeToadd.home_star = value[3]
    planeToadd.mass = value[4]
    planeToadd.radius = value[5]
    planeToadd.distance = value[6]
    planeToadd.save()

def user_add (value):
    userToadd = username()
    userToadd.first_name = value[0]
    userToadd.last_name=value[1]
    userToadd.email= value[2]
    userToadd.password = value[3]
