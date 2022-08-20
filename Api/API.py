from flask import Flask, request, render_template
from flask_restful import Api, Resource, reqparse
from flask_restful import fields, marshal_with, marshal, inputs, abort
from flask_sqlalchemy import SQLAlchemy
import datetime, requests, json, os
import logging


app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
BASE_URL = "https://127.0.0.1:5000"


def loggingSetup(path):
    log_format = '%(asctime)s %(message)s'
    logging.basicConfig(filename = path,
                        format = log_format,
                        filemode = "w",
                        level = logging.INFO)

loggingSetup("master.log")

class BirthdayModel(db.Model):
    fname = db.Column(db.String(30), primary_key = True)
    lname = db.Column(db.String(30), primary_key = True)
    birthday = db.Column(db.String(8), nullable = False)
    BirthdayLocation = db.Column(db.String(50))
    relationship = db.Column(db.String(50))
    customMessage = db.Column(db.String(100))
    Day30Notification = db.Column(db.Integer)
    Day7Notification = db.Column(db.Integer)
    BirthdayNotification = db.Column(db.Integer)
    created = db.Column(db.DateTime, nullable = False)
    updated = db.Column(db.DateTime)
    
    columns = {
                "fname": fields.String,
                "lname": fields.String,
                "birthday": fields.String,
                "BirthdayLocation": fields.String,
                "relationship": fields.String,
                "customMessage": fields.String,
                "Day30Notification": fields.Integer,
                "Day7Notification": fields.Integer,
                "BirthdayNotification": fields.Integer,
                "created": fields.DateTime,
                "updated": fields.DateTime
            }

parser = reqparse.RequestParser()
parser.add_argument("fname", type = str)
parser.add_argument("lname", type = str)
parser.add_argument("birthday", type = str)
parser.add_argument("relationship", type = str)
parser.add_argument("customMessage", type = str)
parser.add_argument("Day30Notification", type = bool)
parser.add_argument("Day7Notification", type = bool)
parser.add_argument("BirthdayNotification", type = bool)

class Birthday(Resource):
    
    def checkName(self, fname, lname):
        name = f"{fname} {lname}"
        match = BirthdayModel.query.filter_by(fname = fname, lname = lname).first()
        if match:
            logging.info("Name {} already exist".format(name))
            return match
        else:
            return None
        
    def checkModel(self, model):
        return self.checkName(model.fname, model.lname)
    
    # TODO check to see if there are updates. If no updates then send a message.
    def updateModel(self, old_model, new_model):
        logging.info(f"Updating info for {old_model.fname} {old_model.lname}")
        old_model.birthday = new_model.birthday
        old_model.relationship = new_model.relationship
        old_model.customMessage = new_model.customMessage
        old_model.Day30Notification = new_model.Day30Notification
        old_model.Day7Notification = new_model.Day7Notification
        old_model.BirthdayNotification = new_model.BirthdayNotification
        old_model.updated = datetime.datetime.now()
        return old_model

    @marshal_with(BirthdayModel.columns)
    def get(self):
        return BirthdayModel.query.all(), 200    

    def post(self):
        args = parser.parse_args()
        birthday = BirthdayModel(created = datetime.datetime.now(), **args)
        match = self.checkModel(birthday)
        if not match:
            resp = marshal(birthday, BirthdayModel.columns)
            db.session.add(birthday)
            logging.info(f"New Entry {birthday.fname} {birthday.lname} added to database")
            db.session.commit()
            return resp, 201
        else:
            updated = marshal(self.updateModel(match, birthday), BirthdayModel.columns)
            db.session.commit()
            return {"Entry Updated": updated}, 202
    
    def delete(self):
        args = parser.parse_args()
        match = self.checkName(args["fname"], args["lname"])
        if match:
            resp = {"Entry Deleted": dict(marshal(match, BirthdayModel.columns)), "Timestamp": datetime.datetime.now()}
            logging.info(resp)
            db.session.delete(match)
            db.session.commit()
            return resp, 200
        else:
            resp = {"Error": f'{args["fname"]} {args["lname"]} was not found in the database'}
            logging.warning(resp)
            return resp, 400

 # TODO add user endpoint with user specific actions


api.add_resource(Birthday, "/birthdays")
db.create_all()

if __name__ == "__main__":
    app.run(debug = True)