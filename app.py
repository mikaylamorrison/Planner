# This document represents all the CRUD functions that we will use for our websiote
    # CRUD = Create, Read, Update, Delete

# importing the framework we need from flask
# imports functionality for our project so we don't have to write a system for routing info from front end to back end
from flask import Flask, render_template, request, redirect

# A route associates a URL with a view function to complete a certain function
# Flask matches the URL to a route; routes are defined with the @app.route decorator in Flask 
    # A decorator adds additional features to a function
    # A view function is a Python function that takes a web request and returns a web response. Information can be passed into the view function.

import sqlite3 # will be used to create the back end of our database 

# initializing flask application; creates the flask object to be used later
app = Flask(__name__)
items = [] #empty list, will eventually store our data

# Adding a database connection 
db_path = 'checklist.db' #creating a table by specifying the path 

def create_table(): # whenever we create a new table function (call this function), a new databse will occur.
    conn = sqlite3.connect(db_path) # establishes the connection with the database
    c = conn.cursor() # instantiates cursor for the database; how we read and write information 
    c.execute('''CREATE TABLE IF NOT EXISTS checklist
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT)''')
    # ^ the way in which the data is stored and formatted; two different variables for each data entry (Integer ID and text)
        # There will be unique integers for every day element, and they will incremet
        # the item is the text value
    conn.commit() # commits changes to the database
    conn.close() # closing connection to databse when finished modifying

# Revising CRUD Operations to work with the Database
def get_items(): # function that selects item from the database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute ("SELECT * FROM checklist")
        # asterix indicates to include all the data
    items = c.fetchall()
    conn.close() # not making any changes here, so we don't have to commit
    return items

def add_item(item):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute ("INSERT INTO checklist (item) VALUES (?)", (item,)) 
        # takes in a database item, and the value associated with that item; inserts it into database
    conn.commit()
    conn.close()

def update_item(item_id, new_item): #updates item based on the value and location provided
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute ("UPDATE checklist SET item = ? WHERE id = ?", (new_item, item_id)) 
    conn.commit()
    conn.close()

def delete_item(item_id): 
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute ("DELETE FROM checklist WHERE id = ?", (item_id,)) # delete according to the ID
    conn.commit()
    conn.close()

# Reading = takes place at the home path; associates user front-end (URL) with the backend 
    # Route uses get method by default; only lets user receive data, not send it
@app.route('/')
def checklist():
    create_table() # makes sure that the table exists when the list is first created
    items = get_items()
    return render_template('checklist.html', items=items) # passes items list into the template; allows for customization of template file
    # item variable contains item ID and the name of the item

# Creating endpoint = associating path to a view function
    # Post is an HTTP method that allows the user to send and recive date; goes from back-end to front-end
@app.route('/add', methods = ['POST']) # decorator; serves as the route for our flask app
    # posts item into the database
def add():
    item = request.form['item'] #gets data that the user inputted into the request form
    add_item(item) # adds the new item to the list; connects to database and adds item with function
    return redirect('/') # returns us to home page/directoy/route

# Updating functionality and endpoint
@app.route('/edit/<int:item_id>', methods=['GET', 'POST']) # create a unique path ()data specifier for each item 
def edit(item_id):
    if request.method == 'POST': #if the requst item does not exist in the item database
        new_item = request.form['item'] # a new item that we get from the user using the request form
        update_item(item_id, new_item)
        return redirect('/')
    
    else: #this will  help us understand which one to delete in case of a duplicate; searches for the item id rather than the item name
        items = get_items() # get full list of items
        item = next((x[1] for x in items if x[0] == item_id), None) # search for item according to it's ID
        return render_template('edit.html', item=item, item_id=item_id)

# Delete
@app.route('/delete/<int:item_id>') # deleting an item according to its ID
def delete(item_id):
    delete_item(item_id) # deleting an item from the list of items  
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

