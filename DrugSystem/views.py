from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
import os, json
from django.conf import settings


# Create your views here.

@login_required
def logOut(request):
    print('You are logging out')
    logout(request)
    print('Logged out')
    return redirect('/login')


def home(request):
    # freeUser, created = Group.objects.get_or_create(name='Free Users')
    # paidUser, created = Group.objects.get_or_create(name='Paid User')
    user = request.user
    context_dict = {}



    # if user.is_authenticated: #This means they are logged in
    #     Groups = user.groups.all()
    #     if paidUser in Groups: #Get the paid objects
    #         figType = FileType.objects.get(fileTypeName = 'Fig Files')
    #         speType = FileType.objects.get(fileTypeName= 'SPE Files')
    #         figFiles = NasaFiles.objects.filter(type=figType).order_by('name')
    #         speFiles = NasaFiles.objects.filter(type=speType).order_by('name')

    #         context_dict['figFiles'] = figFiles
    #         context_dict['speFiles'] = speFiles
    #         context_dict['paid'] = True
    #         print("Got paid files")

    #     crossType = FileType.objects.get(fileTypeName = 'Cross Sections')
    #     dataType = FileType.objects.get(fileTypeName='Data Sheets')
    #     crossFiles = NasaFiles.objects.filter(type=crossType).order_by('name')
    #     dataFiles = NasaFiles.objects.filter(type=dataType).order_by('name')
    #     context_dict['crossFiles'] = crossFiles
    #     context_dict['dataFiles'] = dataFiles
    #     print("Got free files")

    return render(request, 'index.html', context=context_dict)