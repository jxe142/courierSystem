from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
import os, json
from django.conf import settings
import pandas as pd
from .models import *

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


def makeDrugs(request):
    if(Drugs.objects.filter(DEALvl="CI")): #if all files have been made take them home
        return redirect("/home", request)
    if(not request.user.is_superuser):
        return redirect("/home", request)
    else:
        #Make the drug croups based on the DEA SCHEDULE
        cI, created = Group.objects.get_or_create(name='DEA_CI')
        cII, created = Group.objects.get_or_create(name='DEA_CII')
        cIII, created = Group.objects.get_or_create(name='DEA_CIII')
        cIV, created = Group.objects.get_or_create(name='DEA_CIV')
        cV, created = Group.objects.get_or_create(name='DEA_CV')


        rootDir = settings.MEDIA_ROOT
        drugDF = pd.read_excel(os.path.join(rootDir, 'product.xla'))

        drugs = drugDF[ ['PRODUCTNDC','PRODUCTTYPENAME', 'SUBSTANCENAME', 'DEASCHEDULE', 'DOSAGEFORMNAME' ]]
        print(drugs['DEASCHEDULE'].head(10))

        for i, row in enumerate(drugs.itertuples(), 1):
            print(i)
            currentObj = Drugs()
            currentObj.name = row.SUBSTANCENAME
            currentObj.NDC = row.PRODUCTNDC
            currentObj.description = row.PRODUCTTYPENAME
            currentObj.dosageFormName = row.DOSAGEFORMNAME

            if(row.DEASCHEDULE == 'NaN'):
                #Note The groups are for adding the users to them
                #cI.add(currentObj)
                currentObj.DEALvl = 'CI'
            
            if(row.DEASCHEDULE == 'CII'):
                #cII.add(currentObj)
                currentObj.DEALvl = row.DEASCHEDULE
            
            if(row.DEASCHEDULE == 'CIII'):
                #cIII.add(currentObj)
                currentObj.DEALvl = row.DEASCHEDULE

            if(row.DEASCHEDULE == 'CIV'):
                #cIV.add(currentObj)
                currentObj.DEALvl = row.DEASCHEDULE

            if(row.DEASCHEDULE == 'CV'):
                #cV.add(currentObj)
                currentObj.DEALvl = row.DEASCHEDULE
            
            currentObj.save()


    return  HttpResponse(status=200)



