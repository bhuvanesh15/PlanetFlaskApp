from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager,jwt_required,create_access_token
from flask_mail import Mail, Message

file_path = os.path.abspath(os.getcwd()) + "\database.db"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path  #configs

app.config['JWT_SECRET_KEY'] = 'super-secert'

app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_USERNAME'] = 'fab4a60dfd6dfa'
app.config['MAIL_PASSWORD'] = '455d00c76fc9d7'


db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)



@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("db created bitches")

@app.cli.command('db_dump')
def db_dump():
    db.drop_all()
    print("db dropped!!")


@app.cli.command('db_seeds')
def db_seed():
    mercury = planets(
        planet_name='mercury',
        planet_type='class D',
        home_star='sol',
        mass=3.212,
        radius=45.8,
        distance=35.7979
    )
    venus = planets(
        planet_name='venus',
        planet_type='class E',
        home_star='soil',
        mass=4.212,
        radius=30,
        distance=45.7979
    )

    earth = planets(
        planet_name='earth',
        planet_type='class A',
        home_star='soiler',
        mass=3.212,
        radius=25,
        distance=28.7979
    )

    print('database commited!!')

    test_user = username(
        first_name='justine',
        last_name='biber',
        email='jb@fgfj.com',
        password='password'

    )
    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)
    db.session.add(test_user)
    db.session.commit()
    print('database seeded')


@app.route('/')
def index():
    return jsonify(Helo='index.html', bitches='for the world'), 404


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
    planets_list = planets.query.all()
    result = Planet_schema.dump(planets_list)
    return jsonify(result)


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = username.query.filter_by(email=email).first()
    if test:  #it means none
        return jsonify(message='username already exist'),409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        insert = username(first_name=first_name,last_name=last_name,email=email,
                            password= password)
        db.session.add(insert)
        db.session.commit()
        return jsonify(message='data inserted succesfully'),200

@app.route('/login',methods=['POST'])
def login():
    if request.is_json:    #inputJsonexample
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']   #inputFormexample
        password = request.form['password']

    test = username.query.filter_by(email=email,password=password).first() #remember to auntendicate bothemailid and password
    if test:
        accesss_token1 = create_access_token(identity=email)
        return jsonify(message='Login succeeded',accesss_token =accesss_token1),200
    else:
        return jsonify(message='Sorry entered wrong email_Id or password'),401


@app.route('/retrive_password/<string:email>',methods=['POST'])





#database model:

class username(db.Model):
    __tablename__ = "users"
    id = db.Column(Integer, primary_key=True)
    first_name = db.Column(String)
    last_name = db.Column(String)
    email = db.Column(String, unique=True)
    password = db.Column(String)


class planets(db.Model):
    __tablename__ = "planet"
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(String)
    radius = Column(String)
    distance = Column(String)


class UserSchemes(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


class PlanetSchemes(ma.Schema):
    class Meta:
        fields = ('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')


user_schema = UserSchemes()
users_schema = UserSchemes(many=True)

Planet_schema = PlanetSchemes()
Planet_schema = PlanetSchemes(many=True)

if __name__ == "__main__":
    app.run(debug=True)
