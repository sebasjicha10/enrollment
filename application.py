import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash



from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///enrollment.db")


@app.route("/")
@login_required
def index():
    """Show list of enrolled courses"""

    # Retrieve user's enrollment history
    history = db.execute("SELECT * FROM history WHERE user_id = :id", id=session["user_id"])

    # Retrieve user's name
    names = db.execute("SELECT name FROM users WHERE user_id = :id", id=session["user_id"])
    name = names[0]["name"].title()

    # Render user´s history with their info
    return render_template("index.html", student_name=name, history=history)


@app.route("/enrollment", methods=["GET", "POST"])
@login_required
def enrollment():
    """Allow user to enroll to a new course"""

    # Get available courses
    courses = db.execute("SELECT * FROM courses WHERE space_available > :space", space=0)

    if request.method == "POST":

        # Define variables
        course = request.form.get("course")
        given_password = request.form.get("password")

        # Ensure course was submitted
        if not course:
            return apology("You must select a course")

        # Ensure password was submitted
        if not given_password:
            return apology("You must provide your password")

        # Ensure password is corrent
        user_list = db.execute("SELECT user_id, password FROM users WHERE user_id = :username",
                               username=session["user_id"])

        # Ensure password is correct
        if len(user_list) != 1 or not check_password_hash(user_list[0]["password"], given_password):
            return apology("Invalid password")

        # Ensure student can´t enroll more than once
        past_enrollment = db.execute("SELECT course_id FROM history WHERE user_id = :username",
                                     username=session["user_id"])

        for i in range(len(past_enrollment)):
            if course == past_enrollment[i]["course_id"]:
                return apology("You are already enrolled in this course")

        # Get selected course info
        selected_course = db.execute("SELECT * FROM courses WHERE course_id =:course", course=course)
        name = selected_course[0]["name"]
        schedule = selected_course[0]["schedule"]
        course_id1 = selected_course[0]["course_id"]


        # Add course to histoy
        db.execute("INSERT INTO history (course_id, name, schedule, user_id) VALUES (:course_id, :name, :schedule, :user_id)",
                   user_id=session["user_id"], course_id=course_id1, name=name, schedule=schedule)

        # Update spaces available
        db.execute("UPDATE courses SET space_available = space_available - :spacetaken WHERE course_id = :course_id",
                   spacetaken=1, course_id=course_id1)

        flash(f'You have successfully enrolled in {course_id1} {name}!')

        return redirect("/")

    else:
        return render_template("enrollment.html", courses=courses)


@app.route("/schedule")
@login_required
def schedule():
    """Show schedule"""

    # Retrieve courses user has enrolled in
    courses = db.execute("SELECT course_id FROM history WHERE user_id = :id", id=session["user_id"])

    return render_template("schedule.html", courses=courses)


@app.route("/information")
@login_required
def personal_info():
    """Show students personal info"""

    # Retrieve user's current information
    info = db.execute("SELECT * FROM users WHERE user_id = :id", id=session["user_id"])

    name = info[0]["name"].title()

    # Render user´s history with their info
    return render_template("information.html", student_name=name, info=info)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Define variables
        student_id = str(request.form.get("student_id")).capitalize()
        password = request.form.get("password")

        # Ensure student_id was submitted
        if not student_id:
            return apology("You must provide your user id")

        # Ensure student_id was submitted
        if not password:
            return apology("You must provide your password")

        # Query database for user_id
        user_list = db.execute("SELECT user_id, password FROM users WHERE user_id = :username",
                          username=student_id)

        # Ensure user_id exists and password is correct
        if len(user_list) != 1 or not check_password_hash(user_list[0]["password"], password):
            return apology("Invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = user_list[0]["user_id"]

        # Return flashed message
        flash('Welcome back!')

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/check_id", methods=["GET"])
def check_id():
    """Return name if username available, else false, in JSON format"""

    # Retrieve id given by the user
    given_id = (request.args.get("student_id").capitalize())

    # Make sure id is 6 chars
    if len(given_id) != 6:
        return jsonify(False)

    # Find the id
    existing_id = db.execute("SELECT student_id, name FROM students WHERE student_id = :student_id",
                             student_id=given_id)

    if not(existing_id):
        return jsonify(False)

    real_id = existing_id[0]["student_id"]
    student_name = existing_id[0]["name"].title()

    # Checking they haven't registered before
    registrants = db.execute("SELECT user_id FROM users WHERE user_id = :student_id",
                             student_id=given_id)

    if (real_id == given_id) and (not(registrants)):
        return jsonify(student_name)

    else:
        return jsonify(False)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Define variables
        student_id = (request.form.get("student_id").capitalize())
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")
        conf_password = request.form.get("conf_password")

        # Ensure student id was submitted
        if not request.form.get("student_id"):
            return apology("You must provide your Student ID")

        # Ensure phone id was submitted
        elif not phone:
            return apology("You must provide your Phone Number")

        # Ensure email id was submitted
        elif not email:
            return apology("You must provide your Email Address")

        # Ensure password id was submitted
        elif not password:
            return apology("You must provide your Password")

        # Ensure password id was submitted
        elif not conf_password:
            return apology("You must confirm your Password")

        # Ensure phone is valid
        if phone.isdigit() == False or len(phone) != 8:
            return apology("Your Phone Number must be 8 digits, no hashs or spaces")

        # Ensure password is at least 6 chars long
        if len(password) < 6:
            return apology("Password must be at least 6 characters long")

        # Ensure password matches
        elif not (conf_password == password):
            return apology("Passwords must match")

        # Hash password
        final_password = generate_password_hash(password)

        # Find the id
        existing_id = db.execute("SELECT * FROM students WHERE student_id = :student_id",
                                 student_id=student_id)

        real_id = existing_id[0]["student_id"]
        if real_id is None:
            return apology("You must provide a valid Student ID")

        # Checking they haven't registered before
        registrants = db.execute("SELECT user_id FROM users WHERE user_id = :student_id",
                             student_id=student_id)

        if registrants:
            return apology("You must provide a valid Student ID")

        # Add user to data base
        student_name = existing_id[0]["name"]
        major = existing_id[0]["major"]
        result = db.execute("INSERT INTO users (user_id,name,phone,email,password,major) VALUES (:user_id, :name, :phone, :email, :password, :major)",
                            user_id=real_id, name=student_name, phone=phone, email=email, password=final_password, major=major)

        # Remember which user has logged in
        session["user_id"] = real_id

        flash(f'Sign Up was Successful!')

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    """Update info"""

    # Retrieve user's current information
    info = db.execute("SELECT * FROM users WHERE user_id = :id", id=session["user_id"])

    if request.method == "POST":
        # Define variables
        phone = request.form.get("phone")
        email = request.form.get("email")
        given_password = request.form.get("password")

        # Ensure password is given
        if not given_password:
            return apology("You must provide your Password")

        #Retrieve password
        user_password = db.execute("SELECT password FROM users WHERE user_id = :username",
                          username=session["user_id"])

        password = user_password[0]["password"]

        # Check for valid password
        if not check_password_hash(password, given_password):
            return apology("Invalid password")

        # If none changes are given
        if not phone and not email:
            flash("You didn't provide a new phone or email")
            return render_template("update.html", info=info)

        # Ensure we have a phone
        elif not phone:
            phone = info[0]["phone"]

        # Ensure we have a email
        elif not email:
            email = info[0]["email"]

        # Ensure phone is valid
        if phone.isdigit() == False or len(phone) != 8:
            return apology("Your Phone Number must be 8 digits, no hashs or spaces")

        # Update
        db.execute("UPDATE users SET phone = :phone, email = :email WHERE user_id = :user_id",
                   phone=phone, email=email, user_id=session["user_id"])

        flash(f"Your info was successfully updated. Phone: {phone} - Email: {email}")
        return redirect("/")

    else:
        return render_template("update.html", info=info)


@app.route("/password", methods=["GET", "POST"])
@login_required
def passwrod():
    """Change Password"""

    if request.method == "POST":
        # Define variables
        given_password = request.form.get("password")
        new_password = request.form.get("new_password")
        conf_password = request.form.get("conf_password")

        # Ensure password is given
        if not given_password or not new_password or not conf_password:
            return apology("All fields must be filled")

        #Retrieve password
        user_password = db.execute("SELECT password FROM users WHERE user_id = :username",
                          username=session["user_id"])

        password = user_password[0]["password"]

        # Check for valid password
        if not check_password_hash(password, given_password):
            return apology("Current Password was incorrect")

        # Ensure new password is at least 6 chars long
        if len(new_password) < 6:
            return apology("New Password must be at least 6 characters long")

        # Ensure new password and confirmatin match
        if new_password != conf_password:
            return apology("New Password doesn't match")

        # Ensure new password and current one aren't the same
        if given_password == new_password:
            return apology("New Password can't be the same as the Current one")

        # Hash newpassword
        final_password = generate_password_hash(new_password)

        #Update db
        db.execute("UPDATE users SET password = :password WHERE user_id = :user_id",
                   user_id=session["user_id"], password=final_password)

        flash("You password was updated successfully")
        return redirect("/")

    else:
        return render_template("password.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology("Error")

