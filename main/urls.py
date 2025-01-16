from django.urls import path

#from .views import 
from . import views


urlpatterns = [
    path("", views.test),
    path("review/", views.handle_review, name="handle_review"),
    path("review_success/", views.review_success, name="review_success"),
]
