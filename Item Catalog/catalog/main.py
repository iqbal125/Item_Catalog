from time import strftime
import os
import jinja2
import requests
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import User, Category, Item
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
from functools import wraps

engine = create_engine('sqlite:///catalog.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog"

#Helper Functions
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# JSON APIs to view Category Information
@app.route('/category/<int:category_id>/item/JSON')
def CategoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])

@app.route('/category/<int:category_id>/it<int:item_id>/JSON')
def ItemJSON(category_id, item_id):
    Item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=Item.serialize)

@app.route('/categories/JSON')
def CategoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

#Show all categories
@app.route('/')
@app.route('/category/')
def showFront():
    return render_template('frontpage.html')

@app.route('/categories', methods=["GET", 'POST'])
def showCategories():
    categories = session.query(Category).all()
    return render_template('categories.html', categories=categories)

#Create a new category
@app.route('/category/new/', methods=['GET', 'POST'])
@login_required
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showFront'))
    else:
        return render_template('newcategory.html')

#Edit a category
@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
@login_required
def editCategory(category_id):
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if editedCategory.user_id != login_session['user_id']:
        return 'You are not authorized to edit this category.'
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            return redirect(url_for('showFront'))
    else:
        return render_template('editcategory.html', category=editedCategory)

#Delete a category
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_id):
    CategoryToDelete = session.query(Category).filter_by(id=category_id).one()
    if CategoryToDelete.user_id != login_session['user_id']:
        return 'You are not authorized to delete this category.'
    if request.method == 'POST':
        session.delete(CategoryToDelete)
        session.commit()
        return redirect(url_for('showFront', category_id=category_id))
    else:
        return render_template('delcategory.html', category=CategoryToDelete)

#Show a category item
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/item/')
@login_required
def showItem(category_id):
    item = session.query(Item).filter_by(category_id=category_id).first()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('showitem.html', items=items, category_id=category_id, item=item)

#Create a new item
@app.route('/category/<int:category_id>/item/new/', methods=['GET', 'POST'])
@login_required
def newItem(category_id):
    if request.method == 'POST':
        newItem = Item(name=request.form['name'], description=request.form['description'],
                            price=request.form['price'], category_id=category_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id)

#Edit an item
@app.route('/category/<int:category_id>/item/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def editItem(category_id, item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id))
    else:
        return render_template('edititem.html', category_id=category_id, item_id=item_id, item=editedItem)

#Delete an item
@app.route('/category/<int:category_id>/item/<int:item_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(category_id, item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id))
    else:
        return render_template('delitem.html', item=itemToDelete)

#Logout based on provider
@app.route('/logout')
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        return redirect(url_for('showFront'))
    else:
        return redirect(url_for('showFront'))

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    return output

@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # Reset user's session
        login_session.clear()
        resp = jsonify(status='ok', messege="Successfully Disconnected")
    else:    
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

if __name__ == "__main__":
    app.secret_key = "x23bvd"
    app.debug = True
    app.run(host = "0.0.0.0", port = 9000)
