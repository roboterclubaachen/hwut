from hwut_server.database import db

from sqlalchemy.orm import relationship


class Boards(db.Model):
    __tablename__ = 'boards'
    name = db.Column(db.Text, primary_key=True, unique=True, nullable=False)
    manufacturer = db.Column(db.Text)
    microcontroller = db.Column(db.Text, db.ForeignKey('microcontrollers.name'), nullable=False)
    runners = relationship("Runners")
    jobs = relationship("Jobs")

    def __init__(self, name, microcontroller, manufacturer=None):
        self.name = name
        self.microcontroller = microcontroller
        self.manufacturer = manufacturer

    def __repr__(self):
        return '<board %s>' % self.name

    def to_dict(self, extended=False):
        if extended:
            return {
                'name': self.name,
                'microcontroller': self.microcontroller,
                'manufacturer': self.manufacturer,
                'runners': self.runners,
            }
        else:
            return {
                'name': self.name,
                'microcontroller': self.microcontroller,
            }


class Microcontrollers(db.Model):
    __tablename__ = 'microcontrollers'
    name = db.Column(db.Text, primary_key=True, unique=True, nullable=False)
    manufacturer = db.Column(db.Text)
    board = relationship("Boards")

    def __init__(self, name, manufacturer=None):
        self.name = name
        self.manufacturer = manufacturer

    def __repr__(self):
        return '<microcontroller %s>' % self.name

    def to_dict(self, extended=False):
        if extended:
            return {
                'name': self.name,
                'manufacturer': self.manufacturer,
            }
        else:
            return {
                'name': self.name,
            }
