#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from flask.views import MethodView

from models import db, Article, User, ArticleSchema, UserSchema

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = [ArticleSchema().dump(a) for a in Article.query.all()]
    return make_response(articles)

@app.route('/articles/<int:id>')
def show_article(id):
    if 'page_views' not in session:
        session['page_views'] = 0

    session['page_views'] += 1

    if session['page_views'] > 3:
        return {'message': 'Maximum pageview limit reached'}, 401

    article = Article.query.get(id)

    if article is None:
        return {'message': 'Article not found'}, 404

    return make_response(ArticleSchema().dump(article))


class MemberOnlyIndex(MethodView):
    def get(self):
        if not session.get('user_id'):
            return {'message': 'Unauthorized'}, 401

        articles = Article.query.filter_by(is_member_only=True).all()
        return make_response([ArticleSchema().dump(article) for article in articles])


class MemberOnlyArticle(MethodView):
    def get(self, id):
        if not session.get('user_id'):
            return {'message': 'Unauthorized'}, 401

        article = Article.query.filter_by(id=id, is_member_only=True).first()

        if article is None:
            return {'message': 'Article not found'}, 404

        return make_response(ArticleSchema().dump(article))


member_only_index = MemberOnlyIndex.as_view('member_only_index')
app.add_url_rule('/member_only_articles', view_func=member_only_index, methods=['GET'])

member_only_article = MemberOnlyArticle.as_view('member_only_article')
app.add_url_rule('/member_only_articles/<int:id>', view_func=member_only_article, methods=['GET'])


if __name__ == '__main__':
    app.run(port=5555)
