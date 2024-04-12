from flask import Flask
from pymongo import MongoClient
from flask_pymongo import PyMongo

client = MongoClient('localhost', 27017)

db = client.actions
git_db = db.git
