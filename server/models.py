from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from marshmallow import Schema, fields

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String)
    title = db.Column(db.String)
    content = db.Column(db.String)
    preview = db.Column(db.String)
    minutes_to_read = db.Column(db.Integer)
    is_member_only = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='articles')

    def __repr__(self):
        return f'Article {self.id} by {self.author}'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    articles = db.relationship('Article', back_populates='user')

    def __repr__(self):
        return f'User {self.name}, ID {self.id}'

class ArticleSchema(Schema):
    id = fields.Int()
    author = fields.String()
    title = fields.String()
    content = fields.String()
    preview = fields.String()
    minutes_to_read = fields.Int()
    is_member_only = fields.Boolean()
    date = fields.DateTime()

    user = fields.Nested(lambda: UserSchema(exclude=("articles",)))

class UserSchema(Schema):
    id = fields.Int()
    name = fields.String()

    articles = fields.Nested(ArticleSchema(exclude=("user",)))