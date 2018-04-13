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

@csrf_exempt
def register(request):
    print('Registation')
    #Note the email will be the userName and the email
    #By default they are added to LEVEL 1 there are five levels based off DEA levels for controled substacens

    context = {}
    context['usernameNotAvailable'] = False

    #Get the free user group and add permissions
    userType = ContentType.objects.get_for_model(User)
    cI, created = Group.objects.get_or_create(name='DEA_CI')
    buyCI, created = Permission.objects.get_or_create(name='Buy CI',codename='CIBuyer', content_type=userType)
    cI.permissions.add(buyCI)


    if(request.POST):

        userName = request.POST.get('username')
        password = request.POST.get('password')
        firstN = request.POST.get('firstN')
        lastN = request.POST.get('lastN')
        companyN = request.POST.get('companyN')

       

        print(userName)
        if(User.objects.filter(username=userName).exists()):
            context['usernameNotAvailable'] = True
            return render(request, 'index.html', context=context)        
        else:
            #If wer get everything from the request
            if( all((userName, password, firstN, lastN, companyN))):
                #make the new user
                newUser = User()
                newUser.username = userName
                newUser.email = userName
                newUser.set_password(password)
                newUser.first_name = firstN
                newUser.last_name = lastN
                newUser.save()

                newClient = Client()
                newClient.user = newUser
                newClient.companyName = companyN
                newClient.save()

                print('Made the user')

                #Add them to the free group
                cI.user_set.add(newUser)
                print('Added to Level CI')

                #django.contrib.auth.login(user=newUser, request=request)
                return redirect("/home", request=request)
            else:
                return HttpResponse(400, 'Please include all of the informaiton')

    return render(request, 'index.html', context=context) #Note need to TODO: Chagne to the right template


@csrf_exempt
def checkUserName(request):
    if (request.POST):
        data = {}

        userName = request.POST.get('username')
        if (User.objects.filter(username=userName).exists()):
            data['available'] = False
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data['available'] = True
            return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
@login_required
def updateDEALevel(request):
    context_dict = {}


    # if(not request.user.is_superuser):
    #     print('Not Super')
    #     return redirect("/home", request)
    # else:
    if(request.method == "POST"): #go in and add the users to the groups we specified
        userType = ContentType.objects.get_for_model(User)
        cI, created = Group.objects.get_or_create(name='DEA_CI')
        buyCI, created = Permission.objects.get_or_create(name='Buy CI',codename='CIBuyer', content_type=userType)
        cI.permissions.add(buyCI)

        cII, created = Group.objects.get_or_create(name='DEA_CII')
        buyCII, created = Permission.objects.get_or_create(name='Buy CII',codename='CIIBuyer', content_type=userType)
        cII.permissions.add(buyCI)
        cII.permissions.add(buyCII)

        cIII, created = Group.objects.get_or_create(name='DEA_CIII')
        buyCIII, created = Permission.objects.get_or_create(name='Buy CIII',codename='CIIIBuyer', content_type=userType)
        cIII.permissions.add(buyCI)
        cIII.permissions.add(buyCII)
        cIII.permissions.add(buyCIII)

        cIV, created = Group.objects.get_or_create(name='DEA_CIV')
        buyCIV, created = Permission.objects.get_or_create(name='Buy CIV',codename='CIVBuyer', content_type=userType)
        cIV.permissions.add(buyCI)
        cIV.permissions.add(buyCII)
        cIV.permissions.add(buyCIII)
        cIV.permissions.add(buyCIV)


        cV, created = Group.objects.get_or_create(name='DEA_CV')
        buyCV, created = Permission.objects.get_or_create(name='Buy CV',codename='CVBuyer', content_type=userType)
        cV.permissions.add(buyCI)
        cV.permissions.add(buyCII)
        cV.permissions.add(buyCIII)
        cV.permissions.add(buyCIV)
        cV.permissions.add(buyCV)
        
        user = request.POST.get('user')
        newLevel = request.POST.get('selectedLvl')
        user = User.objects.get(username=user)

        if(newLevel == 'CI'):
            user.groups.clear()
            cI.user_set.add(user)
        elif(newLevel == 'CII'):
            user.groups.clear()
            cII.user_set.add(user)
        elif(newLevel == 'CIII'):
            user.groups.clear()
            cIII.user_set.add(user)
        elif(newLevel == "CIV"):
            user.groups.clear()
            cIV.user_set.add(user)
        elif(newLevel == 'CV'):
            user.groups.clear()
            cV.user_set.add(user)

        print(user)
        print(newLevel)

    print("Not POST")
    usersAndLevels = []
    users = Client.objects.filter().all()
    for u in users:
        for g in u.user.groups.all():
            if(g.name == 'DEA_CV'):
                usersAndLevels.append((u, g.name))
                break
            if(g.name == 'DEA_CIV'):
                usersAndLevels.append((u, g.name))
                break
            if(g.name == 'DEA_CIII'):
                usersAndLevels.append((u, g.name))
                break
            if(g.name == 'DEA_CII'):
                usersAndLevels.append((u, g.name))
                break
            if(g.name == 'DEA_CI'):
                usersAndLevels.append((u, g.name))
                break

    context_dict['users'] = usersAndLevels
    return render(request, 'DEApermissions.html', context=context_dict )

        

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



