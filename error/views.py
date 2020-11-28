from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class ErrorView(View, LoginRequiredMixin):
    def get(self, request):
        return render(request, 'error/error_page.html')


def error404(request):
    type = "404"
    args = {
        'type': type,
    }
    return render(request, 'error/error404and500.html',args)


def error500(request):
    type = "500"
    args={
        'type':type,
    }
    return render(request,'error/error404and505.html',args)