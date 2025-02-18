from django.db.models import Q
from django.core.cache import cache

from ninja import NinjaAPI
from ninja.responses import Response

from .models import User, Connection
from app import models, schema, services


api = NinjaAPI()
