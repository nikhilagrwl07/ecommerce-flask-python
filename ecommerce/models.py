from datetime import datetime
from ecommerce import db, login_manager
from flask_login import UserMixin

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    firstName = db.Column(db.String(20), unique=False, nullable=False)
    lastName = db.Column(db.String(20), unique=False, nullable=False)
    address1 = db.Column(db.String(20), unique=False, nullable=False)
    address2 = db.Column(db.String(20), unique=False, nullable=False)
    zipcode = db.Column(db.String(20), unique=False, nullable=False)
    city = db.Column(db.String(20), unique=False, nullable=False)
    state = db.Column(db.String(20), unique=False, nullable=False)
    country = db.Column(db.String(20), unique=False, nullable=False)
    phone = db.Column(db.String(20), unique=False, nullable=False)

    # posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Category(db.Model):
    __table_args__ = {'extend_existing': True}
    categoryId = db.Column(db.Integer, primary_key=True)
    categoryName = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Category('{self.categoryName}', '{self.date_posted}')"


class Product(db.Model):
    __table_args__ = {'extend_existing': True}
    productId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.DECIMAL, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.categoryId'), nullable=False)

    def __repr__(self):
        return f"Product('{self.productId}', '{self.title}')"


class Cart(db.Model):
    __table_args__ = {'extend_existing': True}
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    productId = db.Column(db.Integer, db.ForeignKey('product.productId'), nullable=False, primary_key=True)

# class Dependent(db.Model):
#     __table__ = db.Model.metadata.tables['dependent']
#
#
# class Department(db.Model):
#     __table__ = db.Model.metadata.tables['department']
#
#
# # used for query_factory
# def getDepartment(columns=None):
#     u = Department.query
#     if columns:
#         u = u.options(orm.load_only(*columns))
#     return u
#
#
# def getDepartmentFactory(columns=None):
#     return partial(getDepartment, columns=columns)


# class Dept_Locations(db.Model):
#     __table__ = db.Model.metadata.tables['dept_locations']


# class Employee(db.Model):
#     __table_args__ = {'extend_existing': True}
#     ssn = db.Column(db.CHAR, primary_key=True)
#     fname = db.Column(db.String(15), nullable=False)
#     super_ssn = db.Column(db.CHAR, db.ForeignKey('employee.ssn'), nullable=False)
#
#
# class Project(db.Model):
#     __table_args__ = {'extend_existing': True}
#     pnumber = db.Column(db.Integer, primary_key=True)
#     pname = db.Column(db.String(15), nullable=False)
#     dnum = db.Column(db.CHAR, db.ForeignKey('department.dnumber'), nullable=False)
