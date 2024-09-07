from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
    session,
)

from urllib.parse import quote
from flask import session


from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)

# Set a secret key for flash messages
app.secret_key = "your_secure_random_string"  # Replace with a secure secret key

password = "sahil@123"
quoted_password = quote(password, safe="")
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://root:{quoted_password}@localhost/pet_adoption"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column("user_id", db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    living_situation = db.Column(db.String(50))
    family_composition = db.Column("family_compostion", db.Integer)
    lifestyle = db.Column(db.String(50))
    contact = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)


# Define a route to handle form submission
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        # Get form data
        username = request.form["inputName"]
        email = request.form["inputEmail"]
        living_situation = request.form["inputLivingSituation"]
        family_composition = request.form["inputFamilyComposition"]
        lifestyle = request.form["inputLifestyle"]
        contact = request.form["inputMobileNumber"]
        password = request.form["inputPassword"]

        # Create a new User object
        new_user = User(
            username=username,
            email=email,
            living_situation=living_situation,
            family_composition=family_composition,
            lifestyle=lifestyle,
            contact=contact,
            password=password,  # Store the password as plain text
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)

        # Render the account_created.html template
        return render_template(
            "account_created.html", message="User successfully registered!"
        )

    return render_template("create.html")


# Define a route for the account created page
@app.route("/account_created")
def account_created():
    message = request.args.get("message", None)
    return render_template("account_created.html", message=message)


@app.route("/")
def welcome():
    return render_template("wel.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/start")
def start():
    return render_template("start.html")


@app.route("/index")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Your existing logic for the index page goes here
    return render_template("index.html")


@app.route("/logout")
def logout():
    # Clear the user session
    session.clear()

    # Redirect to the login page after logout
    return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        print(f"Received login request for Email: {email}, Password: {password}")

        user = User.query.filter(User.email == email).first()

        if user and user.password == password:
            print("Login successful")
            flash("Login successful", "success")

            # Set user_id in session upon successful login
            session["user_id"] = user.user_id

            return render_template(
                "index.html",
                flashed_messages=get_flashed_messages(with_categories=True),
            )
        else:
            print("Invalid email or password")
            flash("Invalid email or password", "error")
            return render_template(
                "wel.html", flashed_messages=get_flashed_messages(with_categories=True)
            )

    return render_template(
        "index.html", flashed_messages=get_flashed_messages(with_categories=True)
    )


if __name__ == "__main__":
    app.run(debug=True)
