
from django.shortcuts import render, redirect, HttpResponse
from manil_app.models import *
from manil_app import views
from customer_app import views
from chaipoint_app import views
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
import re
from django.http import JsonResponse
from django.utils.dateparse import parse_date