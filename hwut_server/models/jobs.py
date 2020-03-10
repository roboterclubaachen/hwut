from enum import Enum

from hwut_server.database import db


class JobStatus(Enum):
    WAITING = 10
    RUNNING = 20
    FINISHED = 30


class Jobs(db.Model):
    __tablename__ = 'jobs'
    id = db.Column('id', db.BigInteger, db.Sequence('jobs_id_seq'), primary_key=True, index=True, unique=True,
                   autoincrement=True)
    created = db.Column(db.TIMESTAMP, nullable=False)
    uploaded = db.Column(db.TIMESTAMP, nullable=False)
    status = db.Column(db.Enum(JobStatus))
    name = db.Column(db.Text)
    filename_executable = db.Column(db.Text, nullable=False)
    filename_log = db.Column(db.Text)
    filename_other = db.Column(db.Text)
    owner = db.Column(db.Text, db.ForeignKey('users.name'), nullable=False)

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
