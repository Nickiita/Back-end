from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Person, Review
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
import json


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


@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)
        
        User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "User registrated successfully"}, status=201)

    return JsonResponse({'error': 'Invalid request.'}, status=405)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"message": "Login successful"}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
        
    return JsonResponse({'error': 'Invalid request.'}, status=405)
        

@csrf_exempt
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Logout successful"}, status=200)
