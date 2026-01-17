from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate 
def signup(request):
    print("Signup view accessed")
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('posts_list')  # Redirect to posts list after signup
        else:
            print(form.errors)
    
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})