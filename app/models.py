from app import db

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable=False)

class pokemon(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pokemon = db.Column(db.String, unique = True, nullable = False)
    nivel = db.Column(db.Integer, nullable = False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 