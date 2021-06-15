from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager,jwt_required,create_access_token
from flask_mail import Mail, Message
from flask_pymongo import PyMongo
from mongoengine import *
from flask_swagger_ui import get_swaggerui_blueprint
from PIL import Image
import base64
from io import BytesIO
import requests



#file_path = os.path.abspath(os.getcwd()) + "\database.db"
app = Flask(__name__)

download_FOLDER = './static/images'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path  #configs
app.config['MONGO_URI'] = 'mongodb://localhost:27017/PlanetList'  #configs
app.config['JWT_SECRET_KEY'] = 'super-secert'

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['download_FOLDER'] = download_FOLDER
#insertmailtrapimptconfigs

mongo = PyMongo(app)
#db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)


SWAGGER_URL = '/api/swag'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
# @app.cli.command('db_create')
# def db_create():
#     db.create_all()
#     print("db created ")
#
# @app.cli.command('db_dump')
# def db_dump():
#     db.drop_all()
#     print("db dropped!!")
#
#
# @app.cli.command('db_seeds')
# def db_seed():
#     mercury = planets(
#         planet_name='mercury',
#         planet_type='class D',
#         home_star='sol',
#         mass=3.212,
#         radius=45.8,
#         distance=35.7979
#     )
#     venus = planets(
#         planet_name='venus',
#         planet_type='class E',
#         home_star='soil',
#         mass=4.212,
#         radius=30,
#         distance=45.7979
#     )
#
#     earth = planets(
#         planet_name='earth',
#         planet_type='class A',
#         home_star='soiler',
#         mass=3.212,
#         radius=25,
#         distance=28.7979
#     )
#
#     print('database commited!!')
#
#     test_user = username(
#         first_name='justine',
#         last_name='biber',
#         email='jb@fgfj.com',
#         password='password'
#
#     )
#     db.session.add(mercury)
#     db.session.add(venus)
#     db.session.add(earth)
#     db.session.add(test_user)
#     db.session.commit()
#     print('database seeded')


@app.route('/')
def index():
    return render_template("index.html")
    #return jsonify(Helo='index.html', wes='for the world'), 404


@app.route("/send-image/<path:url>")
def imageUp(url):
    from datetime import datetime
    datetimeObj = datetime.now()
    file_name_for_base64_data = datetimeObj.strftime("%d-%b-%Y--(%H-%M-%S)")
    file_name_for_regular_data = url[-10:-4]

    try:

        if "data:image/jpeg;base64," in url:
            base_string = url.replace("data:image/jpeg;base64,", "")
            decoded_img = base64.b64decode(base_string)
            img = Image.open(BytesIO(decoded_img))
            #add time stamp
            file_name = download_FOLDER + file_name_for_base64_data + ".jpg"
            img.save(file_name, "jpeg")


        elif "data:image/png;base64," in url:
            base_string = url.replace("data:image/png;base64,", "")
            decoded_img = base64.b64decode(base_string)
            img = Image.open(BytesIO(decoded_img))

            file_name = download_FOLDER + file_name_for_base64_data + ".png"
            img.save(file_name, "png")


        else:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content)).convert("RGB")
            file_name = download_FOLDER+file_name_for_regular_data + ".jpg"
            img.save(file_name, "jpeg")


        status = "Image has been succesfully sent to the server."
    except Exception as e:
        status = "Error! = " + str(e)


    return status,200



@app.route('/getusers')
def userlist():
    getuser_list = mongo.db.username.find()
    result = user_schema.dump(getuser_list)
    return jsonify(result),200


@app.route('/parameterPass')
def params():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message="Sory not your age " + name), 401
    else:
        return jsonify(message="Welcome" + name),200


@app.route('/paramsVariable/<string:name>/<int:age>')  # datatypes holds after #cleaner
def cleanParams(name: str, age: int):  # check dataty holdes before
    if age < 18:
        return jsonify(message="Sory not your age " + name), 401
    else:
        return jsonify(message="Welcome" + name)


@app.route('/planets', methods=['GET'])
def planets():
    planets_list = mongo.db.planets.find()
    result = Planet_schema.dump(planets_list)
    return jsonify(result),200


@app.route('/register', methods=['POST'])
def register():

    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    password = request.form['password']
    db_emails = mongo.db.username.find({"email": f"{email}"})#verify email
    #check = []
    # for ddb_e in db_emails:
    #     check.append(ddb_e)
    # if len(check)>0:
    if db_emails.count()>0:
        return 'already exist', 409
    else:
        update_this = mongo.db.username.insert_one({'email':email,'first_name':first_name,'last_name':last_name,'password':password})
        ref= update_this.inserted_id
        return f'db updated as { ref }', 200
    # print(email)
    # user = username(first_name=first_name,last_name=last_name,email=email,
    #                         password= password)
    # print(user)
    # user.save()
    # test = mongo.db.username.find({"email":email})
    # print('-----test---')
    # print(test)
    # if test:  #it means none
    #     return jsonify(message='username already exist'),409
    # else:
    #
    #     insert = username(first_name=first_name,last_name=last_name,email=email,
    #                         password= password)
    #     insert.save()
    #     return jsonify(message='data inserted succesfully'),200

@app.route('/login',methods=['POST'])
def login():
    if request.is_json:    #inputJsonexample
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']   #inputFormexample
        password = request.form['password']
    db_emails = mongo.db.username.find({"email": f"{email}"})
    if db_emails.count() > 0:
        accesss_token1 = create_access_token(identity=email)
        return jsonify(message='Login succeeded', accesss_token=accesss_token1), 200
    else:
        return jsonify(message='Sorry entered wrong email_Id or password'), 401



    # #remember to auntendicate bothemailid and passwordd
    # check = []
    # for ddb_e in db_emails:
    #     check.append(ddb_e)
    # if len(check) > 0:
    #     check[0].get('email')
    #
    #
    # if db_emails:
    #     accesss_token1 = create_access_token(identity=email)


#
# @app.route('/retrive_password/<string:email>',methods=['POST'])
# def forgotpass(email: String):
#     USser = username.query.filter_by(email=email).first()
#     if USser:
#         msg = Message("Your planet API password is " + USser.password,
#                      sender="admin@god.com",
#                      recipients=[email])
#         mail.send(msg)
#         return jsonify(message="Forgetten password send to "+ email)
#     else:
#         return jsonify(message="the emailid does not exist")


@app.route('/remove_planet/<string:planetis>',methods=['DELETE'])
@jwt_required()
def rm(planetis:String):
    #planet = planets.query.filter_by(planet_id=planetis).first() #firstfunction is important
    planetcheck = mongo.db.planets.find({"planet_name": f"{planetis}"})
    if planetcheck.count():
        planettodelete = mongo.db.planets.delete_one({"planet_name": f"{planetis}"})
        return jsonify(message="planet deleted wowowo"),200
    else:
        return jsonify(message="this planet not exist in the universe"),404



@app.route('/godaddsplanet',methods=['POST'])
def godsWish():
    distance = request.form['distance']
    home_star = request.form['home_star']
    mass = request.form['mass']
    #planet_id = request.form['planet_id']
    planet_name = request.form['planet_name']
    planet_type = request.form['planet_type']
    radius = request.form['radius']
    planet_id = mongo.db.planets.find().count()+1 ##uuid
    plane_check= mongo.db.planets.find({"planet_name": f"{planet_name}"})  # verify email
    # check = []
    # for ddb_e in db_emails:
    #     check.append(ddb_e)
    # if len(check)>0:
    if plane_check.count() > 0:
        return 'God has already created the planet ', 409
    else:
        update_this = mongo.db.planets.insert_one(
            {'distance': distance, 'home_star': home_star, 'mass': mass, 'planet_id': planet_id, 'planet_name':planet_name,
             'planet_type':planet_type,'radius':radius})
        ref = update_this.inserted_id
        return f'God created the planet {planet_name} as {ref}', 200








# database model:

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


class UserSchemes(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


class PlanetSchemes(ma.Schema):
    class Meta:
        fields = ('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')


user_schema = UserSchemes()
user_schema = UserSchemes(many=True)

Planet_schema = PlanetSchemes()
Planet_schema = PlanetSchemes(many=True)

if __name__ == "__main__":
    app.run(debug=True)
