from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'

    def serialize(self):
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_at": self.created_at.isoformat()  # Formato ISO para fechas
        }


class Article(db.Model):
    __tablename__ = 'articles'
    
    article_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(255), nullable=False)
    published_date = db.Column(db.DateTime, nullable=False)
    source = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    image_url = db.Column(db.String(255))

    category = db.relationship('Category', backref='articles')

    def __repr__(self):
        return f'<Article {self.title}>'

    def serialize(self):
        return {
            "article_id": self.article_id,
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "published_date": self.published_date.isoformat(),
            "source": self.source,
            "category_id": self.category_id,
            "image_url": self.image_url
        }


class Category(db.Model):
    __tablename__ = 'categories'
    
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Category {self.name}>'

    def serialize(self):
        return {
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description
        }


class Tag(db.Model):
    __tablename__ = 'tags'
    
    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(50))

    def __repr__(self):
        return f'<Tag {self.name}>'

    def serialize(self):
        return {
            "tag_id": self.tag_id,
            "name": self.name,
            "color": self.color
        }


class ArticleTag(db.Model):
    __tablename__ = 'articles_tags'
    
    article_id = db.Column(db.Integer, db.ForeignKey('articles.article_id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True)

    article = db.relationship('Article', backref='article_tags')
    tag = db.relationship('Tag', backref='article_tags')

    def serialize(self):
        return {
            "article_id": self.article_id,
            "tag_id": self.tag_id
        }


class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.article_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='favorites')
    article = db.relationship('Article', backref='favorites')

    def serialize(self):
        return {
            "favorite_id": self.favorite_id,
            "user_id": self.user_id,
            "article_id": self.article_id,
            "created_at": self.created_at.isoformat()
        }


class Comment(db.Model):
    __tablename__ = 'comments'
    
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.article_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    article = db.relationship('Article', backref='comments')
    user = db.relationship('User', backref='comments')

    def serialize(self):
        return {
            "comment_id": self.comment_id,
            "article_id": self.article_id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at.isoformat()
        }
