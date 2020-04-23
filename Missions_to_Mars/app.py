from flask import Flask, render_template, redirect
import pymongo
from bson import json_util
import json
from scrape_mars import scrape

app = Flask(__name__)


recent_mars_info={}
recent_mars_info['Latest_News'] = {'Title':'', 'Teaser': '', 'URL': '', 'Image': ''}
recent_mars_info['JPL_Featured_Image'] = ''
recent_mars_info['Current_Mars_Weather'] = ''
recent_mars_info['Hemisphere_images'] = ''
# recent_mars_info['Mars_Facts'] = {}

print('Connecting to MongoDB....')
# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.mars_db
client.drop_database(db)
collection = db.mars_info

db.collection.update({}, {"$set": {'mars_info':recent_mars_info}}, upsert=True)

@app.route('/')
def home():

    print('A request for the home page…')

    mars_dict = db.collection.find()

    return render_template('index.html', dict=mars_dict[0])

@app.route('/scrape')
def scrape_page():
    
    print('A request for the scrape page…')

    print('Scraping websites for Mars informaiton....')
    post = scrape()

    print('Writing to database....')
    db.collection.update({}, {"$set": {'mars_info':post}}, upsert=True)
    
    print('Redirecting....')
    return redirect('/', code=302)

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