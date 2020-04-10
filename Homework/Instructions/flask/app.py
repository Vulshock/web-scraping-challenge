from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app= Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/marsdata"
mongo = PyMongo(app, "mongodb://localhost:27017/marsdata")

#app route

@app.route("/")
def index():
        mars = mongo.db.mars.find_one()
        return render_template("index.html", mars=mars)

# Scrape route for scrape_mars
@app.route("/scrape")
def scrape():
    mars= mongo.db.mars
    mars_info= scrape_mars.scrape_all()
    mars.update({}, mars_info, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)