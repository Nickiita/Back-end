from django.urls import path

#from .views import 
from . import views


urlpatterns = [
    path("", views.test),
    path("review/", views.handle_review, name="handle_review"),
    path("review_success/", views.review_success, name="review_success"),
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),   
]
