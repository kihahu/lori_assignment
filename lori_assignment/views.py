from django.shortcuts import render


def index(request):
    return render(request, "index.html", {})


def home(request):
    if request.user.is_authenticated:
        return render(request, "home.html", {"user":request.user, "id":request.user.id})
    else:
        return render(request, "index.html", {})
    

def balance(request):
    if request.user.is_authenticated:
        return render(request, "balance.html", {"user":request.user, "id":request.user.id})
    else:
        return render(request, "index.html", {})