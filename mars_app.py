# import all libraries
from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars
import os

app = Flask(__name__)


client = pymongo.MongoClient()
db = client.Mars_Database
collection = db.Mars_Data

@app.route("/scrape")
def scrape()


