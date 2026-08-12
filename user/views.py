from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password ,check_password
from .models import User,Rental,Book
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone


# Create your views here.
def index(request):
    
    books = Book.objects.all()

    return render(
        request,
        "index.html",
        {
            "books": books
        }
    )

def register(request):

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email","").strip().lower()
        username = request.POST.get("username","").strip().lower()
        password = make_password(request.POST.get("password","").strip())

        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            return render(request,"register.html",{"error":"User Alreday exist"})


        user = User.objects.create(
            name=name,
            email=email,
            username=username,
            password=password
        )

        request.session["user_id"] = user.id
        request.session["username"] = user.username

        return redirect("/");

    return render(request,"register.html")

def login(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "").strip()

        user = User.objects.filter(email=email).first()

        if user:
            if check_password(password, user.password):

                request.session["user_id"] = user.id
                request.session["username"] = user.username

                if user.email == "admin@me.com":
                    return redirect("/host")

                return redirect("/")

            else:
                return render(
                    request,
                    "login.html",
                    {"error": "Invalid password"}
                )

        else:
            return render(
                request,
                "login.html",
                {"error": "Email not registered"}
            )


    return render(request, "login.html")

def logout(request):

    request.session.flush()

    return redirect("/")

def profile(request):

    if "user_id" not in request.session:
        return redirect("/login/")

    user = User.objects.get(id=request.session["user_id"])

    rentals = Rental.objects.filter(user=user).select_related("book")
    active = rentals.filter(returned=False).count()

    return render(
        request,
        "profile.html",
        {
            "user": user,
            "rentals": rentals,
            "active": active
        }
    )

def search_books(request):

    query = request.GET.get("q", "").strip()

    books = Book.objects.filter(
        name__icontains=query
    )

    html = render_to_string(
        "book_list.html",
        {"books": books},
        request=request
    )

    return JsonResponse({
        "success": True,
        "html": html
    })

def rent_book(request, id):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Invalid request."
        })

    if "user_id" not in request.session:
        return JsonResponse({
            "success": False,
            "login": True,
            "message": "Please login first."
        })

    try:
        book = Book.objects.get(id=id)

    except Book.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Book not found."
        })

    if not book.available:
        return JsonResponse({
            "success": False,
            "message": "This book is already rented."
        })

    user = User.objects.get(
        id=request.session["user_id"]
    )

    Rental.objects.create(
        user=user,
        book=book
    )

    book.available = False
    book.save()

    return JsonResponse({
        "success": True,
        "message": f"{book.name} rented successfully!"
    })

def return_book(request, id):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Invalid request."
        })

    if "user_id" not in request.session:
        return JsonResponse({
            "success": False,
            "message": "Please login first."
        })

    try:
        rental = Rental.objects.select_related(
            "book", "user"
        ).get(
            id=id,
            user_id=request.session["user_id"]
        )

    except Rental.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Rental not found."
        })

    if rental.returned:
        return JsonResponse({
            "success": False,
            "message": "This book is already returned."
        })

    rental.returned = True
    rental.return_date = timezone.now()
    rental.save()

    rental.book.available = True
    rental.book.save()

    return JsonResponse({
        "success": True,
        "message": f"{rental.book.name} returned successfully!"
    })