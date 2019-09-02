from flask import render_template, request, flash
from app.forms.article import ArctileForm
from .base import web
import pdb

'''
    文章详情页
        增删改查
    首页
        返回文章梳理
'''

@web.route('/articles', methods=['GET'])
def get_all_article():
    return 'get all article'

@web.route('/article', methods=['POST'])
def add_article():
    form = ArctileForm(request.form)
    if form.validate():
        title = form.title.data.strip()
        content = form.content.data
        pdb.set_trace()
    else:
        for errors in form.errors.values():
            flash('_'.join(errors))
    return render_template('add_article.html')

@web.route('/article/<int:id>', methods=['GET'])
def get_one_article(id):
    return 'get one article'

@web.route('/article/<int:id>', methods=['DELETE'])
def delete_article(id):
    return 'delete'

@web.route('/article/<int:id>', methods=['PUT'])
def modify_article(id):
    return 'put'
