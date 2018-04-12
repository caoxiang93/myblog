# -*- coding:utf-8 -*-
from flask import render_template,request,url_for,redirect, flash
from . import auth
from forms import RegistrationForm,LoginForm
from .. import db
from ..models import User
from flask_login import login_user,logout_user,current_user,login_manager
@auth.route('/login',methods=['GET','POST'])
def login():
        # from app.auth.forms import LoginForm
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name = form.username.data,password=form.password.data).first()
        if user is not None:
            login_user(user)
            return redirect(url_for('main.index'))

    return render_template('login.html', title=u'登陆',form = form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    name = form.username.data,
                    password=form.password.data
                    )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html',
                           title=u'注册',
                           form = form)


