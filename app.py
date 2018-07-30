# Dependencies
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)    

@app.route("/")
def dashboard():
    mars_db = mongo.db.mars_db.find_one()
    return render_template("index.html", mars_db=mars_db)

@app.route("/scrape")
def scrape():
    mars_db = mongo.db.mars_db
    mars_data = scrape_mars.scrape()
    mars_db.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)