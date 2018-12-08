import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, session
from ecommerce import app, mysql
from flask_login import login_user, current_user, logout_user, login_required
from ecommerce.forms import *
from ecommerce.models import *


@app.route("/signIn")
def loginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('root'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('root'))


@app.route("/registerationForm")
def registrationForm():
    return render_template("register.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Parse form data
        msg = extractAndPersistUserDataFromForm(request)
        return render_template("login.html", error=msg)


@app.route("/")
@app.route("/home")
def root():
    loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
    allProductDetails = getAllProducts()
    allProductsMassagedDetails = massageItemData(allProductDetails)
    categoryData = getAllCategoryId()

    return render_template('home.html', itemData=allProductsMassagedDetails, loggedIn=loggedIn, firstName=firstName,
                           productCountinKartForGivenUser=productCountinKartForGivenUser,
                           categoryData=categoryData)


@app.route("/displayCategory")
def displayCategory():
    loggedIn, firstName, noOfItems = getLoginUserDetails()
    categoryId = request.args.get("categoryId")

    productDetailsByCategoryId = Product.query.join(ProductCategory, Product.productid == ProductCategory.productid) \
                                    .add_columns(Product.productid, Product.product_name, Product.regular_price, Product.discounted_price, Product.image) \
                                    .join(Category, Category.categoryid == ProductCategory.categoryid)\
                                    .filter(Category.categoryid == int(categoryId))\
                                    .add_columns(Category.category_name)\
                                    .all()

    categoryName = productDetailsByCategoryId[0].category_name
    data = massageItemData(productDetailsByCategoryId)
    return render_template('displayCategory.html', data=data, loggedIn=loggedIn, firstName=firstName,
                           noOfItems=noOfItems, categoryName=categoryName)


@app.route("/productDescription")
def productDescription():
    loggedIn, firstName, noOfItems = getLoginUserDetails()
    productid = request.args.get('productId')
    productDetailsByProductId = getProductDetails(productid)
    return render_template("productDescription.html", data=productDetailsByProductId, loggedIn=loggedIn,
                           firstName=firstName,
                           noOfItems=noOfItems)


@app.route("/addToCart")
def addToCart():
    if isUserLoggedIn():
        productId = int(request.args.get('productId'))
        extractAndPersistKartDetails(productId)
        flash('Item successfully added to cart !!', 'success')
        return redirect(url_for('root'))
    else:
        return redirect(url_for('loginForm'))
