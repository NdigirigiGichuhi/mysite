from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import SignUpForm, LoginForm, UploadForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Order
import os
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html', {})


def create_client(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'User created successfully')
                return redirect('login_client')
            except:
                form.add_error(form, 'username already exists')
                return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'register_client.html', {'form': form})


def login_client(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            client = authenticate(request, username=cd['username'], password=cd['password'])
            

            if client:
                login(request, client)
                # set user-specific data in the session
                request.session['username'] = cd['username']
                request.session.save()
                messages.success(request, 'Login successfull')
                return redirect('dashboard')
            else:
                messages.error(request, 'User does not exist')
                return redirect('login_client')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
    


@login_required
def dashboard(request):
    files = Order.objects.filter(user=request.user)

    #pagination
    paginator = Paginator(files, 5 )
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    username = request.user
    username = str(username).title()
    return render(request, 'dashboard.html', {'files':files, 'username':username, 'page_obj': page_obj})


def logout_client(request):
    logout(request)
    # Clear the user's session data
    Session.objects.filter(session_key=request.session.session_key).delete()
    return redirect('home')


def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False) #save the Order instance to order but do not save to db
            order.user = request.user #add the uploader to the order object
            path = order.file #get the path of the file
            path = str(path) 
            name = os.path.basename(path)
            order.name = name
            form.save() #save
            return redirect('dashboard')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})


def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user}) 


def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'edit_profile.html', {'form': form})
    