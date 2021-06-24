from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)


#Use flask_pymongo to set up mongo connections
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    # Store the entire team collection in a list
    mars = mongo.db.mars.find_one()

    # Return the template with the teams list passed in
    return render_template("index.html", mars=mars)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrapper():

    # Run the scrape function
    mars_data = scrape_mars.scrape_all()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect ("/")

# Define Main Behavior
if __name__ == "__main__":
        app.run(debug=True)