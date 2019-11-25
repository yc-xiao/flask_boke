from flask import render_template, request, url_for
from flask_login import current_user, login_required
from flasgger.utils import swag_from
from collections import namedtuple

from app.models.base import db
from app.models.article import Article
from .base import web

# @web.route('/test1')
# @swag_from('api_doc.test1.yml')
# def test1():
#     return render_template('test.html')

@web.route('/helloc')
def helloc():
    num1 = request.args.get('num1')
    num2 = request.args.get('num2')
    return num1 + num2

@web.route('/test')
def test():
    return render_template('test.html')

@web.route('/')
def index():
    size = 5
    page = request.args.get('page', 1, type=int)
    count = Article.query.filter_by(status=True).count()
    articles = Article.query.filter_by(status=True).order_by(Article.id.desc()).limit(size).offset((page-1)*size).all()

    next = page + 1 if count > page * size else None
    previous = page - 1 if page-1 > 0 else None
    pages = {'next': next,'previous': previous, 'count': count}
    return render_template('index.html', articles=articles, pages=pages)

@web.route('/about')
def about():
    return render_template('about.html')

@web.route('/archives')
@login_required
def archives():
    articles = {}
    sql = "select id, title, create_time from article where writer_id={} order by id desc;".format(current_user.id)
    results = db.session.execute(sql).fetchall()
    _Article = namedtuple('Article', ['id', 'title', 'create_time'])
    for article in results:
        article = _Article._make(article)
        article_time = article.create_time
        year = str(article_time.year)
        article = article._asdict()
        article['timestamp'] = article_time.timestamp()
        if year not in articles:
            articles[year] = [article]
        else:
            articles[year].append(article)
    articles['years'] = sorted(articles.keys(), reverse=True)
    for each in articles['years']:
        articles[each].sort(key=lambda x:x['timestamp'], reverse=True)
    return render_template('archives.html', articles=articles)
