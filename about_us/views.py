from accounts.models import User
from django.http import HttpResponse
from django.shortcuts import render

def about_us(request):
    names = User.objects.all()
    context = {'names':names}
    return render(request,'about_us.html',context= context)
