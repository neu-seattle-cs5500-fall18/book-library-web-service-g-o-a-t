from flask import Flask
from flask_restplus import Api, Resource


class Book:
    def __init__(title, name, ID):
    	Book.title = title
        Book.name = name
        Book.ID = ID
