from flask import Flask
from flask_restplus import Api, Resource

class Person:
    def __init__(person, name, ID, comments):
        Person.name = name
        Person.ID = ID
        Person.comments = comments

