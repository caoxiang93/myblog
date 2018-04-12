# -*- coding:utf-8 -*-
from . import db   # .表示当前包，实际上指向__init__.py文件
from . import login_manager
from flask_login import  UserMixin,AnonymousUserMixin
from markdown import markdown
from datetime import datetime
from sqlalchemy import Text
class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(1024),nullable=True)
    users = db.relationship('User',backref = 'role')

    @staticmethod
    def seed(self):
        db.session.add_all(map(lambda r:Role(name = r),['Guests','Administrators']))
        db.session.commit()

class User(UserMixin,db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(1024),nullable=True)
    name = db.Column(db.String(1024), nullable=True)
    password = db.Column(db.String(1024),nullable=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    posts = db.relationship('Post',backref='author')
    comments = db.relationship('Comment',backref='author')
    locale = db.Column(db.String(20), default='zh')
    @staticmethod
    def on_created(target,value,oldvalue,initiator):
        target.role = Role.query.filter_by(name='Guests').first()

class AnonymousUser(AnonymousUserMixin):
    @property
    def locale(self):
        return 'zh'

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.event.listen(User.name,'set',User.on_created)

class Post(db.Model):
    __tablename__='posts'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(1024))
    body = db.Column(db.Text)
    body_html=db.Column(db.Text)
    create = db.Column(db.DateTime,index=True,default=datetime.now)

    comments = db.relationship('Comment',backref='post')
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    @staticmethod
    def on_body_change(target,value,oldvalue,initiator):
        if value is None or (value is ''):
            target.body_html=''
        else:
            target.body_html=markdown(value)
db.event.listen(Post.body,'set',Post.on_body_change)

class Comment(db.Model):
    __tablename__ = 'comments'
    id =db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime,index=True,default=datetime.now)
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id')) #posts是表名
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))