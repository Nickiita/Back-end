from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Person, Review
from django.contrib.auth.models import User

#from django.contrib.auth import User


def test(request):
    if request.method == "GET":
        all_persons = User.objects.all()

        print(all_persons[0].username)

        data = {
            "persons": all_persons[0].username,
            "title": request.method,
        }

        return render(request, "main.html", data)
    
    if request.method == "POST":
        data = {
            "title": request,
        }

        return render(request, "main.html", data)


def handle_review(request):
    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Review.objects.create(content=content)
            return redirect("review_success")

    elif request.method == "GET":
        reviews = Review.objects.all()
        return render(request, "handle_review.html", {"reviews": reviews})
    

def review_success(request):
    return render(request, "review_success.html")