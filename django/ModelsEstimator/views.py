from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.shortcuts import render
from ModelsEstimator.models import User


def redirect(request):
    if "id" in request.session:
        return HttpResponseRedirect("/panel")
    return HttpResponseRedirect("/auth")


def logout(request):
    if "id" in request.session:
        del request.session["id"]
    return HttpResponseRedirect("/auth")


def auth(request):
    if request.method == "GET":
        return render(request, "Auth.html", {
            "domain": settings.DOMAIN,
            "scheme": settings.SCHEME,
        })
    
    login = request.POST["login"]
    password = request.POST["password"]

    user = User.objects.filter(login=login)
    if user.count() == 1:
        user = user[0]
        if user.password == password:
            request.session["id"] = user.id
            return JsonResponse({"ok": True})
    
    return JsonResponse({"ok": False, "error": "Неправильный логин или пароль"}) 