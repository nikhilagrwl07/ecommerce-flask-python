import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from __init__ import  app

@app.route("/")
@app.route("/home")
def home():
	return "Working"
    # return render_template('index.html', title='Home')
