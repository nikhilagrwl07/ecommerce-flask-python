from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, \
    SelectField, HiddenField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ecommerce import db
from ecommerce.models import *
from wtforms.fields.html5 import DateField
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from ecommerce.models import *
from sqlalchemy import select, func, Integer, Table, Column, MetaData
from flask import session, request
import hashlib, os


def getAllProducts():
    itemData = Product.query.with_entities(Product.productid, Product.product_name, Product.regular_price,
                                           Product.description, Product.image, Product.quantity).all()
    return itemData


def getAllCategoryId():
    return Category.query.with_entities(Category.categoryid, Category.category_name).all()


def massageItemData(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(6):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans


def is_valid(email, password):
    data = User.query.with_entities(User.email, User.password).all()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False


def getLoginUserDetails():
    productCountinCartForGivenUser = 0

    if 'email' not in session:
        loggedIn = False
        firstName = ''
    else:
        loggedIn = True
        userid, firstName = User.query.with_entities(User.userid, User.fname).filter(
            User.email == session['email']).first()

        productCountinCart = []

        # for Cart in Cart.query.filter(Cart.userId == userId).distinct(Products.productId):
        for cart in Cart.query.filter(Cart.userid == userid).all():
            productCountinCart.append(cart.productid)
            productCountinCartForGivenUser = len(productCountinCart)

    return (loggedIn, firstName, productCountinCartForGivenUser)


def getProductDetails(productId):
    productDetailsById = Product.query.filter(Product.productid == productId).first()
    return productDetailsById


def extractAndPersistUserDataFromForm(request):
    password = request.form['password']
    email = request.form['email']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    address1 = request.form['address1']
    address2 = request.form['address2']
    zipcode = request.form['zipcode']
    city = request.form['city']
    state = request.form['state']
    country = request.form['country']
    phone = request.form['phone']

    user = User(fname=firstName, lname=lastName, password=hashlib.md5(password.encode()).hexdigest(), address1=address1,
                address2=address2,
                city=city, state=state, country=country, zipcode=zipcode, email=email, phone=phone)
    db.session.add(user)
    db.session.flush()
    db.session.commit()
    return "Registered Successfully"

def isUserLoggedIn():
    if 'email' not in session:
        return False
    else:
        return True

def extractAndPersistKartDetails(productId):
    userId = User.query.with_entities(User.userid).filter(User.email == session['email']).first()
    userId = userId[0]
    kwargs = {'userid': userId, 'productid': productId}
    quantity = Cart.query.with_entities(Cart.quantity).filter_by(**kwargs).first()

    if quantity is not None:
        cart = Cart(userid=userId, productid=productId, quantity=quantity[0]+1)
    else:
        cart = Cart(userid=userId, productid=productId, quantity=1)

    db.session.merge(cart)
    db.session.flush()
    db.session.commit()


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
