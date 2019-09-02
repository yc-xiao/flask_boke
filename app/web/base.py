from flask import Blueprint, render_template, request
from app.models import Article
import pdb;

web = Blueprint('web', __name__)


@web.route('/')
def index():
    # article = Article.query.all()
    articles = [{'title':1,'created':'2019-10-7','url':'/'},
    {'title':11111111111111,'created':'2019-10-7','url':'/'},
    {'title':1,'created':'2019-10-7','url':'/'},
    {'title':1,'created':'2019-10-7','url':'/'},
    {'title':1,'created':'2019-10-7','url':'/'},
    {'title':1,'created':'2019-10-7','url':'/'},
    {'title':1,'created':'2019-10-7','url':'/'}]
    pages = {'next':None,'previous':'1', 'count':''}
    return render_template('index.html', articles=articles, pages=pages)

@web.route('/test')
def test():
    return render_template('test.html')

@web.route('/about')
def about():
    return render_template('about.html')

@web.route('/admin')
def admin():
    return render_template('admin.html')

@web.route('/archives')
def archives():
    '''
        {
            times: []
            articles: {"time":"article"}
        }
        {
            years: [2019,2018,2017],
            2019: [article1,articles2,],
            2018: [article1,articles2,],
        }
    '''
    articles = {
        'years': ['2019','2018','2017','2020'],
        '2019': [{'title':1,'created':'2019-10-7','url':'/'},
        {'title':11111111111111,'created':'2019-10-7','url':'/'},
        {'title':1,'created':'2019-10-7','url':'/'}],
        '2018': [{'title':1,'created':'2019-10-7','url':'/'},
        {'title':1111111131111,'created':'2019-10-7','url':'/'},
        {'title':1,'created':'2019-10-7','url':'/'}],
        '2020': [{'title':1,'created':'2019-10-7','url':'/'},
        {'title':11111111122211,'created':'2019-10-7','url':'/'},
        {'title':1,'created':'2019-10-7','url':'/'}],
    }
    return render_template('archives.html', articles=articles)
