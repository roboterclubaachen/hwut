from enum import Enum

from hwut_server.database import db


class JobStatus(Enum):
    WAITING = 10
    QUEUED = 15
    RUNNING = 20
    FINISHED = 30
    CANCELED = 40
    ERROR = 50


class Jobs(db.Model):
    __tablename__ = 'jobs'
    id = db.Column('id', db.BigInteger, db.Sequence('jobs_id_seq'), primary_key=True, index=True, unique=True,
                   autoincrement=True)
    created = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(JobStatus), nullable=False)
    comment = db.Column(db.Text)
    duration_limit_seconds = db.Column(db.Integer, nullable=False)
    filename_executable = db.Column(db.Text, nullable=False)
    filename_log = db.Column(db.Text)
    filename_other = db.Column(db.Text)
    owner = db.Column(db.Text, db.ForeignKey('users.name'), nullable=False)
    board = db.Column(db.Text, db.ForeignKey('boards.name'), nullable=False)
    runner = db.Column(db.BigInteger, db.ForeignKey('runners.id'))

    def __init__(self, created, status, duration_limit_seconds, filename_executable, owner, board):
        # 'id' auto increment
        self.created = created
        self.status = status
        self.duration_limit_seconds = duration_limit_seconds
        self.filename_executable = filename_executable
        self.owner = owner
        self.board = board

    def __repr__(self):
        return '<job %i>' % self.id

    def to_dict(self, extended=True):
        if extended:
            return {
                'id': self.id,
                'created': self.created,
                'status': self.status.name,
                'comment': self.comment,
                'duration_limit_seconds': self.duration_limit_seconds,
                'filename_executable': self.filename_executable,
                'filename_log': self.filename_log,
                'filename_other': self.filename_other,
                'owner': self.owner,
                'board': self.board,
            }
        else:
            return {
                'id': self.id,
                'created': self.created,
                'status': self.status.name,
                'owner': self.owner,
            }
