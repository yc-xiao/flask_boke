from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from app.forms.article import ArticleForm
from app.models.article import Article
from app.models.base import db
from .base import web


@web.route('/admin')
@login_required
def admin():
    size = 5
    page = request.args.get('page', 1, type=int)
    count = Article.query.filter_by(status=True).filter_by(writer_id=current_user.id).count()
    articles = Article.query.filter_by(status=True).filter_by(writer_id=current_user.id).order_by(Article.id.desc()).limit(size).offset((page-1)*size).all()
    next = page + 1 if count > page * size else None
    previous = page - 1 if page-1 > 0 else None
    pages = {'next': next,'previous': previous, 'count': count}
    return render_template('admin.html', articles=articles, pages=pages)


@web.route('/write')
@login_required
def article_write():
    article_status = {'status': 400}
    article_id = request.args.get('id', 0, type=int)
    article = Article.query.get(article_id)
    if article and article.writer_id == current_user.id:
        article_status['status'] = 200
    return render_template('write.html', article=article, article_status=article_status)


@web.route('/article', methods=['POST'])
@login_required
def add_article():
    form = ArticleForm(request.form)
    if form.validate():
        article = Article()
        article.set_attr(form.data)
        article.writer_id = current_user.id
        article.writer_alias = current_user.alias
        db.session.add(article)
        db.session.commit()
        return url_for('web.index')
    else:
        errors = ['_'.join(error) for error in form.errors.values()]
        return '_'.join(errors), 500


@web.route('/article/<int:id>', methods=['GET'])
def get_one_article(id):
    article = Article.query.get(id)
    return render_template('article.html', article=article)


@web.route('/article/<int:id>', methods=['PUT'])
@login_required
def modify_article(id):
    form = ArticleForm(request.form)
    if form.validate():
        article = Article.query.get(id)
        if article and article.writer_id == current_user.id:
            article.set_attr(form.data)
            article.update_time = datetime.now()
            db.session.commit()
            return url_for('web.admin')
        else:
            return '没有权限修改文章', 403
    else:
        errors = ['_'.join(error) for error in form.errors.values()]
        return '_'.join(errors), 500

@web.route('/article/<int:id>', methods=['DELETE'])
@login_required
def delete_article(id):
    article = Article.query.get(id)
    if article and article.writer_id == current_user.id:
        article.update_time = datetime.now()
        article.status = False
        db.session.commit()
        return url_for('web.admin')
    else:
        return '没有权限删除文章', 403
