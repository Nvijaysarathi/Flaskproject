from flask import Flask , request ,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

class_path = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(class_path , "database.sqlite")

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    city = db.Column(db.String(100))

    def __init__(self , name , age , city):
        self.name = name
        self.age = age
        self.city = city

class UserSchema(ma.Schema):
    class Meta:
        fields= ("id" , "name" , "age" , "city")

users_schema = UserSchema(many=True)
user_schema = UserSchema()

@app.route("/")
@app.route("/register")
def index():
    return render_template('register.html')

#Inserting the user details
@app.route("/confirm" , methods=["POST" ,"GET"])
def register():
    if request.method=="POST":
        n = request.form.get('name')
        a = request.form.get('age')
        c = request.form.get('city')
        new_user = User(n , a , c)
        db.session.add(new_user)
        db.session.commit()
        return render_template('confirm.html' ,name=n , age=a , city=c)

@app.route("/view" , methods=["GET"])
def alluser():
    all_user = User.query.all()
    result = users_schema.dump(all_user)
    return render_template('view.html' , users = result)
@app.route('/delete')
def deletpage():
    return render_template('delete.html')

@app.route("/deleteuser" , methods=['POST'])
def Delete():
    D_id = request.form.get("userid")
    user = User.query.get(D_id)
    db.session.delete(user)
    db.session.commit()
    # return user_schema.jsonify(user)
    return render_template('delete_success.html', user_id=D_id)

if __name__ =="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)