from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, JsonResponse
from .models import Person, Review
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def handle_review(request):
    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Review.objects.create(content=content)
            return redirect("review_success")
        
        else: 
            return HttpResponseBadRequest("Отзыв не может быть пустым")

    elif request.method == "GET":
        reviews = Review.objects.all()
        return render(request, "handle_review.html", {"reviews": reviews})
    

def review_success(request):
    return render(request, "review_success.html")

#CREATE
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
    

#CREATE
@csrf_exempt
def create_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"error": "Username and password are required"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "User created", "user_id": user.id}, status=201)
    
    except:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)


    

#READ
@csrf_exempt
def read_user(request, user_id):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)
    try:
        user = User.objects.get(id=user_id)
        user_data = {
            "id": user.id,
            "username": user.username,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "last_login": user.last_login,
            "date_joined": user.date_joined,
        }

        return JsonResponse(user_data, status=200)
        
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    

#UPDATE
@csrf_exempt
def update_user(request, user_id):
    if request.method != "PUT":
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)
    try:
        data = json.loads(request.body)
        user = User.objects.get(id=user_id)

        new_username = data.get("username")
        if new_username:
            if User.objects.filter(username=new_username).exclude(id=user_id).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)
            user.username = new_username

        if "password" in data:
            user.set_password(data["password"])

        user.save()
        return JsonResponse({"message": "User updated"}, status=200)

    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    except:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)


#DELETE
@csrf_exempt
def delete_user(request, user_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({"message": "User deleted successfully"}, status=200)
        
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    


