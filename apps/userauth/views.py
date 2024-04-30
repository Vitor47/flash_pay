# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from ..core.utils import is_email_valid
from .forms import loginForm
from .models import User


def login_user(request: HttpRequest) -> HttpResponse:
    form_login = loginForm()
    context = {"form_login": form_login}
    if request.method == "GET":
        return render(request, "login.html", context=context)

    elif request.method == "POST":
        form = loginForm(request.POST)

        if form.is_valid():
            email: str = form.cleaned_data.get("email", None)
            senha: str = form.cleaned_data.get("password", None)

            try:
                validated_email: bool = is_email_valid(email)
                if not validated_email:
                    messages.error(request, "E-mail inválido!")

                user = User.objects.filter(email=email).first()
                if not user:
                    messages.error(request, "Login inválido!")
                    return render(request, "login.html", context=context)

                if not check_password(senha, user.password):
                    messages.error(request, "Login inválido!")
                    return render(request, "login.html", context=context)

            except Exception:
                messages.error(
                    request, "Erro inesperado, favor tentar novamente!"
                )
                return render(request, "login.html", context=context)

            if user:
                return redirect("/api-swagger/")

        else:
            messages.error(request, "Dados informados inválidos!")
            return render(request, "login.html", context=context)


@login_required
def logout_user(request: HttpRequest) -> HttpResponseRedirect:
    return HttpResponseRedirect("/api-swagger/")
