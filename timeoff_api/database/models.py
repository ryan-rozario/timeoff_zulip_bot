from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash


class Leave(db.Document):
    sender = db.EmailField(required=True)
    leave_type = db.StringField(required=True)
    start_time = db.DateTimeField(required=True)
    end_time = db.DateTimeField(required=True)
    manager = db.EmailField(required=True)
    details = db.StringField(required=True)
    accepted = db.BooleanField(default=False)
    added_by = db.ReferenceField('User')

class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    leaves = db.ListField(db.ReferenceField('Leave', reverse_delete_rule=db.PULL))

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

User.register_delete_rule(Leave, 'added_by', db.CASCADE)