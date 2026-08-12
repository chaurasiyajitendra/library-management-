from django.shortcuts import render,redirect
from django.contrib import messages
from user.models import Book, User, Rental
from django.db.models import Count

# Create your views here.
def dashboard(request):

    context = {
        "total_books": Book.objects.count(),
        "available_books": Book.objects.filter(available=True).count(),
        "active_rentals": Rental.objects.filter(returned=False).count(),
        "total_users": User.objects.count(),
        "books": Book.objects.order_by("-id")[:5],
        "rentals": Rental.objects.select_related("user","book").order_by("-id")[:5],
    }

    return render(
        request,
        "dashboard.html",
        context
    )

def books(request):

    books = Book.objects.all().order_by("-id")

    return render(
        request,
        "books.html",
        {
            "books": books
        }
    )

def add_book(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        author = request.POST.get("author", "").strip()
        description = request.POST.get("description", "").strip()

        if not name or not author or not description:

            return render(
                request,
                "addBook.html",
                {
                    "error": "All fields are required.",
                    "form_title": "Add Book"
                }
            )

        Book.objects.create(
            name=name,
            author=author,
            description=description,
            available=True
        )

        messages.success(
            request,
            "Book added successfully."
        )

        return redirect("/host/books")

    return render(
        request,
        "addBook.html",
        {
            "form_title": "Add Book"
        }
    )


def edit_book(request, id):

    try:
        book = Book.objects.get(id=id)

    except Book.DoesNotExist:

        messages.error(
            request,
            "Book not found."
        )

        return redirect("host_books")


    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        author = request.POST.get("author", "").strip()
        description = request.POST.get("description", "").strip()

        if not name or not author or not description:

            return render(
                request,
                "addBook.html",
                {
                    "book": book,
                    "error": "All fields are required.",
                    "form_title": "Edit Book"
                }
            )

        book.name = name
        book.author = author
        book.description = description

        book.save()

        messages.success(
            request,
            "Book updated successfully."
        )

        return redirect("/host/books")


    return render(
        request,
        "addBook.html",
        {
            "book": book,
            "form_title": "Edit Book"
        }
    )


def delete_book(request, id):

    if request.method != "POST":

        return redirect("host_books")


    try:
        book = Book.objects.get(id=id)

        book.delete()

        messages.success(
            request,
            "Book deleted successfully."
        )

    except Book.DoesNotExist:

        messages.error(
            request,
            "Book not found."
        )


    return redirect("host_books")


def rentals(request):

    rentals = Rental.objects.select_related("user","book").order_by("-id")

    return render(
        request,
        "rentals.html",
        {
            "rentals": rentals,
            "active_rentals": rentals.filter(returned=False).count(),
            "returned_rentals": rentals.filter(returned=True).count(),
        }
    )


def users(request):

    users = User.objects.annotate(rental_count=Count("rentals")).order_by("-id")

    return render(
        request,
        "users.html",
        {
            "users": users
        }
    )

def user_detail(request, id):

    user = User.objects.get(id=id)

    rentals = Rental.objects.filter(
        user=user
    ).select_related("book").order_by("-id")

    return render(
        request,
        "userDetails.html",
        {
            "user": user,
            "rentals": rentals
        }
    )


def delete_user(request, id):

    if request.method == "POST":

        try:
            user = User.objects.get(id=id)

            user.delete()

            messages.success(
                request,
                "User deleted successfully."
            )

        except User.DoesNotExist:

            messages.error(
                request,
                "User not found."
            )

    return redirect("/host/users/")