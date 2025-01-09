from django.shortcuts import render
from django.http import HttpResponse
from .models import Person
from django.contrib.auth.models import User
#from django.contrib.auth import User



# def test(request):

#     if request.method == "GET":
#         return HttpResponse("1234")
#     return HttpResponse(request.method)


# def test(request):

#     if request.method == "POST":

#         all_persons = Person.objects.all()


#         print(request.POST)
#         return render(request, "main.html", {"test":request.POST['maininput']})

#     payload = {
#         "test": 2,
#     }
#     return render(request, "main.html", payload)


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
