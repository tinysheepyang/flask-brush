# project/models.py

from datetime import datetime
from sqlalchemy import DateTime
from project import db, bcrypt


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, paid=False, admin=False):
        self.email = email
        #self.password = bcrypt.generate_password_hash(password)
        self.password = password
        self.registered_on = datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<email {}'.format(self.email)

class Case(db.Model):
    __tablename__ = "Cases"
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(100), nullable=True)
    url = db.Column(db.String(100), nullable=True)
    created_time = db.Column(db.DateTime(), default=datetime.now())
    comment = db.Column(db.String(100))

    def __init__(self, info, url, create_time=False, comment=False):
        self.info = info
        self.url = url
        self.created_time = create_time
        self.comment = comment

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return "<Case('%s','%s','%s','%s','%s')>" % (self.id, self.info, self.url, self.created_time, self.comment)

class IP_log(db.Model):
    __tablename__ = 'ip_log'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(32), nullable=False)
    address = db.Column(db.String(64), nullable=True)
    keyword = db.Column(db.String(64), nullable=True)
    url = db.Column(db.String(256), nullable=True)
    click = db.Column(db.Integer, default=0, nullable=True)
    error = db.Column(db.String(64), nullable=True)
    page = db.Column(db.Integer, default=-1, nullable=True)
    rank = db.Column(db.Integer, default=-1, nullable=True)
    created_at = db.Column(db.TIMESTAMP,default=datetime.now())

    def __init__(self, ip, address, keyword,url, click, error, page, rank, created_at):
        self.ip = ip
        self.address = address
        self.keyword = keyword
        self.url = url
        self.click = click
        self.error = error
        self.page = page
        self.rank = rank
        self.created_at = created_at