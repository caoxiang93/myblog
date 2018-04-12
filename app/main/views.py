# -*- coding:utf-8 -*-
from flask import render_template,request,url_for,redirect, flash
from os import path
from werkzeug.utils import secure_filename
from ..models import Post,Comment
from forms import PostForm,CommentForm
from ..models import db
from . import main
from flask_login import login_required,current_user

from flask_babel import gettext as _
# @main.template_test('current_link')
# def is_current_link(link):
#     return link==request.path

@main.route('/services')
def services():
    return 'services'

@main.route('/about')
def about():
    return 'About'

@main.route('/user/<regex("[a-z]{3}"):user_id>')
def user(user_id):
    return 'User %s' % user_id

@main.route('/projects/')
@main.route('/our-workers/')
def projects():
    return 'the project page'



@main.route('/upload',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        f=request.files['file']
        basepath = path.abspath(path.dirname(__file__))
        upload_path=path.join(basepath,'static','uploads',secure_filename(f.filename))
        f.save(upload_path)
        return redirect(url_for('upload'))
    return render_template('upload.html')

@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@main.route('/')  # route 装饰器函数
def index():
    page_index = request.args.get('page',1,type=int)
    query = Post.query.order_by(Post.create.desc())

    pagination = query.paginate(page_index,per_page=20,error_out=False)
    posts = pagination.items
    return render_template('index.html',
                           title=_(u'欢迎来到曹湘的博客'),
                           posts = posts,
                           pagination = pagination)

# @main.template_filter('md')
# def markdown_to_html(txt):
#     from markdown import markdown
#     return markdown(txt)

def read_md(filename):
    with open(filename) as md_file:
        content = reduce(lambda x, y: x + y, md_file.readlines())
    return content.decode('utf-8')

@main.context_processor
def inject_methods():
    return dict(read_md=read_md)

@main.route('/posts/<int:id>',methods=['GET','POST'])
def post(id):
    post = Post.query.get_or_404(id)
    #detail详情页
    #评论窗体
    form = CommentForm()

    #保存评论
    if form.validate_on_submit():
        comment =Comment(author=current_user,body=form.body.data,post=post)
        db.session.add(comment)
        db.session.commit()

    return render_template('posts/detail.html',
                           title=post.title,
                           form=form,
                           post=post)

@main.route('/edit',methods=['GET','POST'])
@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id=0):
    form = PostForm()

    if id ==0:
        post = Post(author = current_user)
    else:
        #修改
        post  = Post.query.get_or_404(id)

    if form.validate_on_submit():
        post.body = form.body.data
        post.title = form.title.data

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.post', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    title = _(u'添加新文章')
    if id > 0:
        title = _(u'编辑 - %(title)',title=post.title)
    return render_template('posts/edit.html',
                           title=title,
                           form = form,
                           post=post)