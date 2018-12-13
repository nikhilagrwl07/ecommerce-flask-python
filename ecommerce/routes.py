import os
import secrets
from PIL import Image
from flask import render_template, request
from ecommerce import app
from ecommerce.forms import *
from plotly.offline import plot
import plotly.graph_objs as go
from flask import Markup
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
    categoryData = getCategoryDetails()

    return render_template('home.html', itemData=allProductsMassagedDetails, loggedIn=loggedIn, firstName=firstName,
                           productCountinKartForGivenUser=productCountinKartForGivenUser,
                           categoryData=categoryData)


@app.route("/displayCategory")
def displayCategory():
    loggedIn, firstName, noOfItems = getLoginUserDetails()
    categoryId = request.args.get("categoryId")

    productDetailsByCategoryId = Product.query.join(ProductCategory, Product.productid == ProductCategory.productid) \
        .add_columns(Product.productid, Product.product_name, Product.regular_price, Product.discounted_price,
                     Product.image) \
        .join(Category, Category.categoryid == ProductCategory.categoryid) \
        .filter(Category.categoryid == int(categoryId)) \
        .add_columns(Category.category_name) \
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

        # Using Flask-SQLAlchmy SubQuery
        extractAndPersistKartDetailsUsingSubquery(productId)

        # Using Flask-SQLAlchmy normal query
        # extractAndPersistKartDetailsUsingkwargs(productId)
        flash('Item successfully added to cart !!', 'success')
        return redirect(url_for('root'))
    else:
        return redirect(url_for('loginForm'))


@app.route("/cart")
def cart():
    if isUserLoggedIn():
        loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
        cartdetails, totalsum, tax = getusercartdetails();
        return render_template("cart.html", cartData=cartdetails,
                               productCountinKartForGivenUser=productCountinKartForGivenUser, loggedIn=loggedIn,
                               firstName=firstName, totalsum=totalsum, tax=tax)
    else:
        return redirect(url_for('root'))


@app.route("/admin/categories/new", methods=['GET', 'POST'])
def addCategory():
    form = addCategoryForm()
    if form.validate_on_submit():
        category = Category(category_name=form.category_name.data)
        db.session.add(category)
        db.session.commit()
        flash(f'Category {form.category_name.data}! added successfully', 'success')
        return redirect(url_for('root'))
    return render_template("addCategory.html", form=form)


@app.route("/admin/categories/<int:category_id>/update", methods=['GET', 'POST'])
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = addCategoryForm()
    if form.validate_on_submit():
        category.category_name= form.category_name.data
        db.session.commit()
        flash('This product has been updated!', 'success')
        return redirect(url_for('getCategories'))
    elif request.method == 'GET':
        form.category_name.data = category.category_name
    return render_template('addCategory.html', legend="Update Category", form=form)


@app.route("/admin/categories", methods=['GET'])
def getCategories():
    categories = Category.query.all()
    #Query for number of products on a category: SELECT category.categoryid, category.category_name, COUNT(product_category.productid) FROM category LEFT JOIN product_category ON category.categoryid = product_category.categoryid GROUP BY category.categoryid

    return render_template('adminCategories.html', categories = categories)

#this method is copied from Schafer's tutorials
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/uploads', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/admin/products", methods=['GET'])
def getProducts():
    products = Product.query.all()
    return render_template('adminProducts.html', products=products)

@app.route("/admin/products/new", methods=['GET', 'POST'])
def addProduct():
    form = addProductForm()
    form.category.choices = [(row.categoryid, row.category_name) for row in Category.query.all()]
    product_icon = ""
    if form.validate_on_submit():
        if form.image.data:
            product_icon = save_picture(form.image.data)
        product = Product(sku=form.sku.data, product_name=form.productName.data, description=form.productDescription.data, image=product_icon, quantity=form.productQuantity.data, discounted_price=15, product_rating=0, product_review=" ", regular_price=form.productPrice.data)

        db.session.add(product)
        db.session.commit()
        product_category = ProductCategory(categoryid=form.category.data, productid=product.productid)
        db.session.add(product_category)
        db.session.commit()
        flash(f'Product {form.productName} added successfully', 'success')
        return redirect(url_for('root'))
    return render_template("addProduct.html", form=form, legend="New Product")


@app.route("/admin/product/<int:product_id>", methods=['GET', 'POST'])
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('adminViewProduct.html', product=product)
  
@app.route("/admin/product/<int:product_id>/update", methods=['GET', 'POST'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = addProductForm()
    form.category.choices = [(row.categoryid, row.category_name) for row in Category.query.all()]
    if form.validate_on_submit():
        product.product_name = form.productName.data
        product.sku = form.sku.data
        product.productDescription = form.productDescription.data
        product.quantity = form.productQuantity.data
        # product.discounted_price = form.data.discounted_price = 15
        product.regular_price = form.productPrice.data
        db.session.commit()
        product_category = ProductCategory.query.filter_by(productid = product.productid).first()
        print("This is product category")
        print(product_category)
        print("That was product category")
        if form.category.data != product_category.categoryid:
            new_product_category = ProductCategory(categoryid=form.category.data, productid = product.productid)
            db.session.add(new_product_category)
            db.session.commit()
            db.session.delete(product_category)
            db.session.commit()

        flash('This product has been updated!', 'success')
        return redirect(url_for('getProducts'))
    elif request.method == 'GET':
        form.productName.data = product.product_name
        form.sku.data = product.sku
        form.productDescription.data = product.description
        form.productPrice.data = product.regular_price
        form.productQuantity.data = product.quantity
    return render_template('addProduct.html', legend="Update Product", form=form)

@app.route("/admin/users", methods=['GET'])
def getUsers():
    users = User.query.all()
    return render_template('adminUsers.html', users= users)


@app.route("/removeFromCart")
def removeFromCart():
    if isUserLoggedIn():
        productId = int(request.args.get('productId'))
        removeProductFromCart(productId)
        return redirect(url_for('cart'))
    else:
        return redirect(url_for('loginForm'))


@app.route("/checkoutPage")
def checkoutForm():
    if isUserLoggedIn():
        cartdetails, totalsum, tax = getusercartdetails()
        return render_template("checkoutPage.html", cartData=cartdetails, totalsum=totalsum, tax=tax)
    else:
        return redirect(url_for('loginForm'))


@app.route("/createOrder", methods=['GET', 'POST'])
def createOrder():
    totalsum = request.args.get('total')
    email, username, ordernumber, address, fullname, phonenumber, provider = extractOrderdetails(request, totalsum)
    if email:
        sendEmailconfirmation(email, username, ordernumber, phonenumber, provider)

    return render_template("OrderPage.html", email=email, username=username, ordernumber=ordernumber,
                                   address=address, fullname=fullname, phonenumber=phonenumber)


@app.route("/seeTrends", methods=['GET', 'POST'])
def seeTrends():
    trendtype = str(request.args.get('trend'))
    cur = mysql.connection.cursor()
    if(trendtype=="least"):
        cur.execute("SELECT ordered_product.productid, sum(ordered_product.quantity) AS TotalQuantity,product.product_name FROM \
                       ordered_product,product where ordered_product.productid=product.productid GROUP BY productid \
                           ORDER BY TotalQuantity ASC LIMIT 3 ")
    else:
        trendtype="most"
        cur.execute("SELECT ordered_product.productid, sum(ordered_product.quantity) AS TotalQuantity,product.product_name FROM \
                ordered_product,product where ordered_product.productid=product.productid GROUP BY productid \
                    ORDER BY TotalQuantity DESC LIMIT 3 ")

    products = cur.fetchall()
    cur.close()
    x = []
    y = []
    for item in products:
        x.append(item['product_name'])
        y.append(item['TotalQuantity'])

    my_plot_div = plot([go.Bar(x=x, y=y)], output_type='div')

    return render_template('trends.html',
                           div_placeholder=Markup(my_plot_div),trendtype=trendtype
                           )