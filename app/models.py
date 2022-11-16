from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Result(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    location = db.column(db.Text())
    temp = db.column(db.Float())

    def to_dict(self):
        return{
            'location': self.location,
            'temp': self.temp,
        }







