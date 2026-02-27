from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# ---------------- CONFIG ----------------

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fallback-secret")

app.config["MONGO_URI"] = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://ethicaladmin:sbup@clusterpractice.suczpoe.mongodb.net/ethicaldb?retryWrites=true&w=majority"
)

mongo = PyMongo(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

bcrypt = Bcrypt(app)

# ---------------- USER CLASS ----------------

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.username = user_data["username"]
        self.password = user_data["password"]

@login_manager.user_loader
def load_user(user_id):
    try:
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(user_data)
    except:
        return None
    return None

# ---------------- CREATE ADMIN IF NOT EXISTS ----------------

with app.app_context():
    if mongo.db.users.count_documents({"username": "pruthvirajpatil"}) == 0:
        hashed_password = bcrypt.generate_password_hash("sbup").decode("utf-8")
        mongo.db.users.insert_one({
            "username": "pruthvirajpatil",
            "password": hashed_password
        })

# ---------------- TRUST SCORE ----------------

def calculate_trust_score(amount, address, description):
    score = 100

    if amount > 100000:
        score -= 30

    if not address or len(address) < 10:
        score -= 20

    suspicious_words = ["urgent", "double money", "guaranteed return"]

    for word in suspicious_words:
        if word in description.lower():
            score -= 15

    return max(score, 0)

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    description = request.form["description"]
    amount = int(request.form["amount"])
    address = request.form["address"]

    trust_score = calculate_trust_score(amount, address, description)

    mongo.db.campaigns.insert_one({
        "name": name,
        "description": description,
        "amount": amount,
        "address": address,
        "trust_score": trust_score,
        "status": "Pending"
    })

    return redirect(url_for("home"))


@app.route("/admin")
@login_required
def admin():
    search = request.args.get("search", "")
    status_filter = request.args.get("status", "")

    query = {}

    if search:
        query["name"] = {"$regex": search, "$options": "i"}

    if status_filter:
        query["status"] = status_filter

    campaigns = list(mongo.db.campaigns.find(query))

    total = mongo.db.campaigns.count_documents({})
    approved = mongo.db.campaigns.count_documents({"status": "Approved"})
    rejected = mongo.db.campaigns.count_documents({"status": "Rejected"})
    pending = mongo.db.campaigns.count_documents({"status": "Pending"})

    avg_score = 0
    all_campaigns = list(mongo.db.campaigns.find())
    if len(all_campaigns) > 0:
        avg_score = sum(c["trust_score"] for c in all_campaigns) / len(all_campaigns)

    return render_template(
        "admin.html",
        campaigns=campaigns,
        total=total,
        approved=approved,
        rejected=rejected,
        pending=pending,
        avg_score=round(avg_score, 2),
        search=search,
        status_filter=status_filter
    )


@app.route("/approve/<id>")
@login_required
def approve(id):
    try:
        mongo.db.campaigns.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"status": "Approved"}}
        )
    except:
        pass
    return redirect(url_for("admin"))


@app.route("/reject/<id>")
@login_required
def reject(id):
    try:
        mongo.db.campaigns.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"status": "Rejected"}}
        )
    except:
        pass
    return redirect(url_for("admin"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_data = mongo.db.users.find_one({"username": username})

        if user_data and bcrypt.check_password_hash(user_data["password"], password):
            user = User(user_data)
            login_user(user)
            return redirect(url_for("admin"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run()