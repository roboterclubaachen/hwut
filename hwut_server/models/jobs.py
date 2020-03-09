from sqlalchemy.orm import relationship

from hwut_server.database import db


class Jobs(db.Model):
    __tablename__ = 'jobs'
    id = db.Column('id', db.BigInteger, db.Sequence('jobs_id_seq'), primary_key=True, index=True, unique=True,
                   autoincrement=True)
    created = db.Column(db.TIMESTAMP, nullable=False)
    uploaded = db.Column(db.TIMESTAMP, nullable=False)
    name = db.Column(db.Text)
    #executable_file = relationship("ExecutableFile", cascade="all,delete", backref="parent")

    def __init__(self, created, uploaded, name):
        # 'id' auto increment
        self.created = created
        self.uploaded = uploaded
        self.name = name

    def __repr__(self):
        return '<job %i>' % self.id

    def to_dict_short(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def to_dict_long(self):
        return {
            'id': self.id,
            'name': self.name,
            'created': self.created,
        }
