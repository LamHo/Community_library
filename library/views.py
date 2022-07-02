from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import User, Book, Time_obj

# Create your views here.


def index(request):
    
    all_books = Book.objects.all().order_by("-last_updated_time")

    paginator = Paginator(all_books, 5) # Show 5 books per page.

    page_number = request.GET.get('page')
   
    page_obj = paginator.get_page(page_number)
    
    return render(request, "library/index.html", {'page_obj': page_obj})
    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "library/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "library/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "library/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "library/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "library/register.html")

@login_required
def donate(request):
    if request.method == 'POST' and request.FILES['file']:
        in_title = request.POST['title']
        in_author = request.POST['author']
        in_cover = request.FILES['cover']
        in_file = request.FILES['file']

        donator = User.objects.get(pk = request.user.id)
       
        new_book = Book(title = in_title, author = in_author, donator = donator, cover_image = in_cover, file = in_file)
        new_book.save()
                
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "library/donate.html")

def search(request):
    if (request.method == "POST"):
        content = request.POST['q']
        found_books = []
        for book in Book.objects.all():
            if (content.lower() in book.title.lower()):
                found_books += [book]
        return render(request,"library/search.html",{
            "found_books": found_books,
            "content": content,
        })

@login_required
def profile(request):
    books = request.user.books_donated.all().order_by("-last_updated_time")

    paginator = Paginator(books, 5) # Show 5 books per page.
    page_number = request.GET.get('page')   
    page_obj = paginator.get_page(page_number)   
   
    return render(request, "library/profile.html",{
        'page_obj': page_obj,
        
    })

@csrf_exempt
@login_required
def edit(request, id):
    try:
        book = Book.objects.get(pk = id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found."}, status=404)
    if (book not in request.user.books_donated.all()):
        return JsonResponse({"error": "This is not your book!"})
    
    if (request.method == 'POST' and request.FILES['file']):
        in_title = request.POST['title']
        in_author = request.POST['author']
        in_cover = request.FILES['cover']
        in_file = request.FILES['file']

        book.title = in_title
        book.author = in_author
        book.cover_image = in_cover
        book.file = in_file
        time_obj = Time_obj()
        time_obj.save()
        book.last_updated_time = time_obj.time
        time_obj.delete()
        book.save()

        return HttpResponseRedirect('/profile')    
    else:
        
        return render(request,"library/edit.html",{
            "book": book,
        })


#APIs:

def book(request, id):
    if (request.method == "GET"):
        book = Book.objects.get(pk = id)
        return JsonResponse(book.serialize(), safe=False)
    elif (request.method == "PUT"):
        pass
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@csrf_exempt
@login_required        
def delete(request):
    if (request.method == "POST"):
        data = json.loads(request.body)
        print(data.get("id"))
        book = Book.objects.get(pk = data.get("id"))
        donator = book.donator.username
        book.delete()
        return JsonResponse({"message": "Book deleted successfully."}, status=201)
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=400)