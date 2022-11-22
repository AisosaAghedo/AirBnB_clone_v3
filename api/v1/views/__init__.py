#!/usr/bin/python3
""" importing  Blueprint """
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.views.index import *
from api.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import  *