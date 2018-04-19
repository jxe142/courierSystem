from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
import os, json
from django.conf import settings
import pandas as pd
from .models import *
import random

# Create your views here.

@login_required
def logOut(request):
    print('You are logging out')
    logout(request)
    print('Logged out')
    return redirect('home')


def logIn(request):
    if request.POST:
        print("In post")
        userName = request.POST.get('email')
        password = request.POST.get('password')
        currentUser = authenticate(request, username=userName, password=password)
        if currentUser is not None:
            print("We are in")
            login(request, currentUser)
            return redirect('home')
        #Try to login with the email
        else:
            email = request.POST.get('email')
            currentUser = authenticate(request, email=email, password=password)
            if currentUser is not None:
                print("We are in")
                login(request, currentUser)
                return redirect('home')


            #The user doesnt exist
            else:
                return redirect('home')


    return render(request, 'login.html')

@csrf_exempt
def register(request):
    print('Registation')
    #Note the email will be the userName and the email
    #By default they are added to LEVEL 1 there are five levels based off DEA levels for controled substacens

    context = {}
    context['usernameNotAvailable'] = False

    #Get the free user group and add permissions
    userType = ContentType.objects.get_for_model(User)
    c0, created = Group.objects.get_or_create(name='DEA_C0')
    buyC0, created = Permission.objects.get_or_create(name='Buy C0',codename='C0Buyer', content_type=userType)
    c0.permissions.add(buyC0)


    if(request.POST):

        userName = request.POST.get('username')
        print(userName)
        password = request.POST.get('password')
        print(password)
        firstN = request.POST.get('firstN')
        print(firstN)
        lastN = request.POST.get('lastN')
        print(lastN)
        companyN = request.POST.get('companyN')
        print(companyN)
        address = request.POST.get('address')
        print(address)

       

        print(userName)
        if(User.objects.filter(username=userName).exists()):
            context['usernameNotAvailable'] = True
            return render(request, 'index.html', context=context)        
        else:
            #If wer get everything from the request
            if( all((userName, password, firstN, lastN, companyN, address))):
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
                newClient.address = address
                newClient.save()

                print('Made the user')

                #Add them to the free group
                c0.user_set.add(newUser)
                print('Added to Level C0')

                login(user=newUser, request=request)
                return redirect("/home", request=request)
            else:
                return redirect("home", request=request)

    return render(request, 'register.html', context=context) #Note need to TODO: Chagne to the right template


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
def searchNDC(request):
    user = request.user
    data = {}

    NDC = request.POST.get("NDC")


    print(NDC)

    if(request.method == "POST"):
        try:
            if(user.groups.filter(name ='DEA_CV')):
                print("Level 5 Drug")
                Drugs.objects.get(NDC=NDC)
                data['drug'] = NDC
            elif(user.groups.filter(name='DEA_CIV')):
                print("Level 4 Drug")
                drug = Drugs.objects.get(NDC=NDC)
                if(drug.DEALvl == 'CI' or drug.DEALvl == 'CII' or drug.DEALvl == 'CIII' or drug.DEALvl == 'CIV'):
                    data['drug'] = NDC
                else:
                    data['drug'] = "You Do not have high enough cleareance for this"
            elif(user.groups.filter(name='DEA_CIII')):
                print("Level 3 Drug")
                drug = Drugs.objects.get(NDC=NDC)
                if(drug.DEALvl == 'CI' or drug.DEALvl == 'CII' or drug.DEALvl == 'CIII'):
                    data['drug'] = NDC
                else:
                    data['drug'] = "You Do not have high enough cleareance for this"
            elif(user.groups.filter(name='DEA_CII')):
                print("Level 2 Drug")
                drug = Drugs.objects.get(NDC=NDC)
                if(drug.DEALvl == 'CI' or drug.DEALvl == 'CII'):
                    data['drug'] = NDC
                else:
                    data['drug'] = "You Do not have high enough cleareance for this"
            elif(user.groups.filter(name='DEA_CI')):
                print("Level 1 Drug")
                drug = Drugs.objects.get(NDC=NDC)
                if(drug.DEALvl == 'CI'):
                    data['drug'] = NDC
                else:
                    data['drug'] = "You Do not have high enough cleareance for this"
            else:
                data['drug'] = "You Do not have high enough cleareance for this"
        except:
            data['drug'] = "NDC doesn't exist"
    

    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
@login_required
def makeOrder(request):
    context = {}

    if(request.method == "POST"):
        order = Orders()
        drugNDCs = request.POST.getlist("drugs[]")
        descript = request.POST.get("descript")

        for NDC in drugNDCs:
            try:
                print(NDC)
                current = Drugs.objects.get(NDC=NDC)
                order.drugs = current
            except:
                print("ERROER CANT FIND DRUG")
        
        order.description = descript
        confirmNum = random.uniform(0,1000000000000)
        order.confirmNum = confirmNum
        order.cost = 10000
        client = Client.objects.get(user = request.user)
        order.user = client
        order.save()

        context['conf'] = confirmNum
        context['success'] = confirmNum
        return render(request, 'orderWentThrough.html', context=context)

    return render(request, 'makeOrder.html')

@login_required
def getPastOrders(request):
    context = {}
    client = Client.objects.get(user = request.user)
    orders = Orders.objects.filter(user=client, canceled=False)
    for o in orders:
        print(o)
    context['orders'] = orders

    return render(request, 'pastOrders.html', context=context)



#________________MAKE FUNS FOR CANCELING, TRACKING AND CONFIMING ORDER SHIPP
@csrf_exempt
@login_required
def updateOrderLocation(request):
    data = {}
    if(request.user.is_superuser):
        if(request.method == "POST"):
            confirm = request.POST.get('confirmNum')
            newLocation = request.POST.get('location')
            order = Orders.objects.filter(confirmNum=confirm).first()
            if(order == None):
                data['success'] = "The Order could not be found"
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                order.location = newLocation
                order.save()
                data['success'] = "The Order Location has been updated"
                return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return render(request, 'index.html')
        
    
    return render(request, 'changeOrderLocation.html')

@csrf_exempt
@login_required
def cancelOrder(request):
    data = {}
    if(request.user.is_superuser):
         if(request.method == "POST"):
            confirm = request.POST.get('confirmNum')
            order = Orders.objects.filter(confirmNum=confirm).first()
            print(confirm)
            print(order)
            if(order == None):
                data['success'] = "The Order could not be found"
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                order.canceled = True
                order.save()
                data['success'] = "The Order Location has been Cancled"
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return render(request, 'index.html')

    return render(request, 'cancelOrder.html')
       
@csrf_exempt
@login_required
def confirmOrderDelivery(request):
    data = {}
    if(request.user.is_superuser):
         if(request.method == "POST"):
            confirm = request.POST.get('confirmNum')
            order = Orders.objects.filter(confirmNum=confirm).first()
            if(order == None):
                data['success'] = "The Order could not be found"
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                order.isDelivered = True
                order.save()
                data['success'] = "The Order has been Delivered"
                return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return render(request, 'index.html')

    return render(request, 'confirmDelivery.html', )



@csrf_exempt  
@login_required
def getOrderLocation(request):
    context = data = {}
    if(request.method == "POST"):
        try:
            confirm = request.POST.get('confirmNum')
            order = Orders.objects.filter(confirmNum=confirm).first()
            context['order'] = order
            data['order'] = order.location
        except:
            data['order'] = "Confirmation Number doesn't exist"

        return HttpResponse(json.dumps(data), content_type='application/json')
    return render(request, 'trackOrder.html')
 

@csrf_exempt
@login_required
def updateDEALevel(request):
    context_dict = {}

    if(request.user.is_superuser):
        if(request.method == "POST"): #go in and add the users to the groups we specified
            userType = ContentType.objects.get_for_model(User)
            c0, created = Group.objects.get_or_create(name='DEA_C0')
            buyC0, created = Permission.objects.get_or_create(name='Buy C0',codename='C0Buyer', content_type=userType)
            c0.permissions.add(buyC0)


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


            if(newLevel == 'C0'):
                user.groups.clear()
                c0.user_set.add(user)
            elif(newLevel == 'CI'):
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
                else:
                    usersAndLevels.append((u, g.name))

        context_dict['users'] = usersAndLevels
    else:
        return render(request, 'index.html')
        
    return render(request, 'DEApermissions.html', context=context_dict )

        

def home(request):
    # freeUser, created = Group.objects.get_or_create(name='Free Users')
    # paidUser, created = Group.objects.get_or_create(name='Paid User')
    user = request.user
    context_dict = {}
    print(user)



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
        c0, created = Group.objects.get_or_create(name='DEA_C0')
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
    

def contactUs(request):
    print('contact')

    return render(request, 'contact.html')


