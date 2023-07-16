from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import Book, Review, Author
from log_reg_app.models import User


def books(request):
    user_id = request.session.get('user_id')
    if user_id:
        all_reviews = Review.objects.order_by('-created_at')
        context = {
            "user": User.objects.get(id=user_id),
            "last_three_reviews": all_reviews[:3],
            "all_reviews_except_last_three": all_reviews[:len(all_reviews)-3][::-1]
        }
        return render(request, "books.html", context)
    else:
        return redirect('/logout')


def add(request):
    user_id = request.session.get('user_id')
    if user_id:
        context = {
            "user": User.objects.get(id=user_id),
            "authors": Author.objects.all()
        }
        return render(request, "adding_book.html", context)
    else:
        return redirect('/logout')


def viewBook(request, book_id):
    user_id = request.session.get('user_id')
    if user_id:
        context = {
            "user": User.objects.get(id=user_id),
            "book": Book.objects.get(id=book_id),
            "reviews": Review.objects.filter(book__id=book_id).order_by('-created_at')
        }
        return render(request, "added_book.html", context)
    else:
        return redirect('/logout')


def addingBook(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if user_id:
            errors_title = Book.objects.validator(request.POST)
            author_old = request.POST.get('author_old')
            if not (author_old.isnumeric()):
                errors_author_new = Author.objects.validator(request.POST)
            errors_review = Review.objects.validator(request.POST)
            if (len(errors_title) > 0) or ((not (author_old.isnumeric())) and (len(errors_author_new) > 0)) or (len(errors_review) > 0):
                the_errors = {}
                if len(errors_title) > 0:
                    for key, value in errors_title.items():
                        the_errors[key] = value
                if len(errors_review) > 0:
                    for key, value in errors_review.items():
                        the_errors[key] = value
                if len(errors_author_new) > 0:
                    for key, value in errors_author_new.items():
                        the_errors[key] = value
                return JsonResponse({'errors' : the_errors})
            else:
                title = request.POST.get('title')
                author_old = request.POST.get('author_old')
                author_new = request.POST.get('author_new')
                content = request.POST.get('content')
                rate = request.POST.get('rate')
                
                if (author_old.isnumeric()):
                    author = Author.objects.get(id=int(author_old))
                elif len(author_new) >= 2:
                    author = Author.objects.create(
                        name = author_new
                    )
                
                book = Book.objects.create(
                    title = title,
                    author = author
                )
                
                Review.objects.create(
                    content = content,
                    rate = rate,
                    user = User.objects.get(id=user_id),
                    book = book
                )
                
                return JsonResponse({'errors' : "success"})
        return redirect('/')
    else:
        return HttpResponse('Method not allowed', status=405)


def addingReview(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if user_id:
            errors_review = Review.objects.validator(request.POST)
            if (len(errors_review) > 0):
                the_errors = {}
                for key, value in errors_review.items():
                    the_errors[key] = value
                return JsonResponse({'errors' : the_errors})
            else:
                content = request.POST.get('content')
                rate = request.POST.get('rate')
                book_id = request.POST.get('book_id')
                
                Review.objects.create(
                    content = content,
                    rate = rate,
                    user = User.objects.get(id=user_id),
                    book = Book.objects.get(id=book_id)
                )
                
                return JsonResponse({'errors' : "success", 'book_id' : book_id})
        return redirect('/')
    else:
        return HttpResponse('Method not allowed', status=405)


def removeReview(request, review_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if user_id:
            review = Review.objects.get(id=review_id)
            book_id = review.book.id
            review.delete()
            return redirect('/books/book/' + str(book_id))
        return redirect('/')
    else:
        return HttpResponse('Method not allowed', status=405)