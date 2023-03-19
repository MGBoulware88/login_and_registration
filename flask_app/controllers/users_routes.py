from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/users/register", methods=['POST'])
def register():
    # validate inputs
    if not User.validate_reg(request.form):
        print("Returning to reg page")
        return redirect("/")
    #if pass, hash pw then instantiate the user
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # override pw input with hashed pw
    data = {
        **request.form,
        'password':pw_hash
    }
    # store the id to pass into redirect
    user_id = User.create_user(data)
    print("Logging in!")
    return redirect(f"/users/{user_id}/dashboard")

@app.route("/users/<int:id>/dashboard")
def dashboard(id):
    # check for login first
    if 'user_id' not in session:
        return redirect("/") #return to login/reg page

    # grab the user and instantiate
    user = User.read_one_user_by_id(id)
    #pass in the first name
    return render_template("dashboard.html", first_name=user.first_name)


@app.route("/users/login", methods=['POST'])
def login_user():
    #check email by trying to instantiate a user
    existing_user = User.read_one_user_by_email(request.form['email'])
    if not existing_user:
        flash("Invalid credentials", 'login')
        return redirect("/")
    #check pw
    if not bcrypt.check_password_hash(existing_user.password, request.form['password']):
        flash("Invalid credentials", 'login')
        return redirect("/")
    
    #if everything checks out, put the user's id into session
    session['user_id'] = existing_user.id
    return redirect(f"/users/{session['user_id']}/dashboard")


@app.route("/users/logout")
def logout_user():
    session.clear()
    return redirect("/")