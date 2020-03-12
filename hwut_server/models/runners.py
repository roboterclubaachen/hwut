from sqlalchemy.orm import relationship
from secrets import token_urlsafe
from datetime import datetime

from hwut_server.database import db


class Runners(db.Model):
    __tablename__ = 'runners'
    id = db.Column('id', db.BigInteger, db.Sequence('runners_id_seq'), primary_key=True, index=True, unique=True,
                   autoincrement=True)
    token = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    enabled = db.Column(db.Boolean, nullable=False)
    last_seen = db.Column(db.DateTime)
    ping_counter = db.Column(db.BigInteger, nullable=False)
    job_counter = db.Column(db.BigInteger, nullable=False)
    busy = db.Column(db.Boolean, nullable=False)
    owner = db.Column(db.Text, db.ForeignKey('users.name'), nullable=False)
    target_board = db.Column(db.Text, db.ForeignKey('boards.name'), nullable=False)
    target_microcontroller = db.Column(db.Text, db.ForeignKey('microcontrollers.name'), nullable=False)
    jobs = relationship("Jobs")

    def __init__(self, owner, board, microcontroller, enabled=True):
        self.token = token_urlsafe(32)
        self.enabled = enabled
        self.last_seen = None
        self.ping_counter = 0
        self.job_counter = 0
        self.busy = False
        self.owner = owner
        self.target_board = board
        self.target_microcontroller = microcontroller

    def __repr__(self):
        return '<runner %d>' % self.id

    def to_dict(self, extended=False):
        if extended:
            return {
                'id': self.id,
                'token': self.token,
                'created': self.created,
                'enabled': self.enabled,
                'last_seen': self.last_seen,
                'ping_counter': self.ping_counter,
                'job_counter': self.job_counter,
                'busy': self.busy,
            }
        else:
            return {
                'id': self.id,
            }

    def ping(self):
        self.ping_counter = Runners.ping_counter + 1
        self.last_seen = datetime.now()
        # FIXME: Maybe do a commit here?

    def acquire(self):
        self.busy = True
        self.job_counter = Runners.job_counter + 1
        # FIXME: Maybe do a commit here?

    def release(self):
        self.busy = False
        # FIXME: Maybe do a commit here?
