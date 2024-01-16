#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article

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

    return {'message': '200: Successfully cleared session data'}, 200

@app.route('/articles')
def index_articles():
    articles = [article.to_dict() for article in Article.query.all()]
    return make_response(jsonify(articles), 200)
    

#When a user makes a GET request below, the following should happen:
# -If this is first request a user has made, set session['page_views'] to initial value of 0
# -For every request, increment the value of session['page_views] by 1
@app.route('/articles/<int:id>')
def show_article(id):
    #sets initial page views to either current number of views or 0 by default
    session['page_views'] = session.get('page_views') or 0
    #increases the page views by 1 regardless of what route
    session['page_views'] += 1

    #If sessions page views less than or = to 3, return the article page at this route.
    if session['page_views'] <= 3:
        return Article.query.filter(Article.id == id).first().to_dict(), 200
    #Displays an error message if over 3 page views.
    return {'message': 'Maximum pageview limit reached'}, 401
    

if __name__ == '__main__':
    app.run(port=5555)
