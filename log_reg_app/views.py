from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import User
from DojoReadsPlatform_app.models import Review
from django.contrib import messages
import bcrypt


def root(request):
    return redirect ('/login')


def login_page(request):
    return render(request, "login.html")


def registration_page(request):
    return render(request, "register.html")


def user_data(request, user_id):
    this_user_id = request.session.get('user_id')
    if this_user_id:
        context = {
            "user": User.objects.get(id=user_id)
        }
        return render(request, "user_data.html", context)
    else:
        return redirect('/logout')


def registration(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            the_errors = {}
            for key, value in errors.items():
                the_errors[key] = value
            return JsonResponse({'errors' : the_errors})
        else:
            name = request.POST.get('name')
            alias = request.POST.get('alias')
            email = request.POST.get('email')
            pwd = request.POST.get('password')
            pw_hash = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode() 
            user = User.objects.create(name=name, alias=alias, email=email, password=pw_hash)
            request.session['user_id'] = user.id
            request.session['user_name'] = user.alias
            return JsonResponse({'errors' : "success"})
    else:
        return HttpResponse('Method not allowed', status=405)


def loging_in(request):
    if request.method == 'POST':
        errors = User.objects.validator_pwd(request.POST)
        if len(errors) > 0:
            return JsonResponse({'errors' : errors})
        else:
            user = User.objects.filter(email=request.POST['email']).first()
            request.session['user_id'] = user.id
            request.session['user_name'] = user.alias
            return JsonResponse({'errors' : "success"})
    else:
        return HttpResponse('Method not allowed', status=405)


def userProfile(request, user_id):
    this_user_id = request.session.get('user_id')
    if this_user_id:
        reviews = Review.objects.filter(user__id=user_id)
        total_reviews = reviews.count()
        context = {
            "user": User.objects.get(id=user_id),
            "reviews": reviews,
            "total_reviews": total_reviews
        }
        return render(request, "user_data.html", context)
    else:
        return redirect('/logout')


def logout(request):
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name')
    if user_id:
        del request.session['user_id']
    if user_name:
        del request.session['user_name']
    return redirect('/login')

