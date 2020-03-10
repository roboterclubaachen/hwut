from hwut_server.database import db

from sqlalchemy.orm import relationship


class Boards(db.Model):
    __tablename__ = 'boards'
    name = db.Column(db.Text, primary_key=True, unique=True, nullable=False)
    manufacturer = db.Column(db.Text)
    runners = relationship("Runners")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<board %s>' % self.name

    def to_dict_short(self):
        return {
            'name': self.name,
        }

    def to_dict_long(self):
        return {
            'name': self.name,
            'manufacturer': self.manufacturer,
            'runners': self.runners,
        }


class Microcontrollers(db.Model):
    __tablename__ = 'microcontrollers'
    name = db.Column(db.Text, primary_key=True, unique=True, nullable=False)
    manufacturer = db.Column(db.Text)
    runners = relationship("Runners")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<microcontroller %s>' % self.name

    def to_dict_short(self):
        return {
            'name': self.name,
        }

    def to_dict_long(self):
        return {
            'name': self.name,
            'manufacturer': self.manufacturer,
            'runners': self.runners,
        }
