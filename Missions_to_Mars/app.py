from flask import Flask, jsonify
from scrape_mars import scrape
import pymongo

app = Flask(__name__)

@app.route('/')
def home():
    print('A request for the home page…')
    return 'Go to /scrape'

@app.route('/scrape')
def scrape_page():

    return 'Scraping websites for Mars informaiton....'
    post = (scrape())
    return 'Done.'

    return 'Connecting to MongoDB....'
    # Initialize PyMongo to work with MongoDBs
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    # Define database and collection
    db = client.mars_db
    collection = db.mars_info
    return 'Done.'

    return 'Writing to database....'
    collection.insert_one(post)
    return 'Done.'

    return 'Displaying DB....'
    listings = db.mars_info.find()

    for listing in listings:
        print(listing)

if __name__ == "__main__":
    app.run(debug=True)
    


'''Step 2 - MongoDB and Flask Application
Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

Start by converting your Jupyter notebook into a Python script called scrape_mars.py 
with a function called scrape that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.

Next, create a route called /scrape that will import your scrape_mars.py script and call your scrape function.

Store the return value in Mongo as a Python dictionary. Create a root route / that will query your Mongo 
database and pass the mars data into an HTML template to display the data.

Create a template HTML file called index.html that will take the mars data dictionary and display all of the data in the appropriate HTML elements. 
Use the following as a guide for what the final product should look like, but feel free to create your own design.'''