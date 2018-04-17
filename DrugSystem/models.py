from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Client(models.Model): #Note this is for a clients taht want to join the site
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    companyName = models.TextField()


#Letting Djnago build Admin and Agents
# class Agents(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#Admin is a super users 

class Drugs(models.Model):
    NDC =  models.CharField(max_length=500, blank=False, db_index=True)
    name = models.TextField()
    description = models.TextField()
    productTypeName = models.TextField()
    quanity =  models.IntegerField(default=100)
    dosageFormName = models.TextField()
    DEALvl = models.CharField(max_length=10, default="CI")




class Orders(models.Model):
    timeStamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000)
    cost = models.IntegerField()
    drugs = models.ManyToManyField(Drugs)
    user = models.ForeignKey(Client, on_delete=models.CASCADE, default=2)
    confirmNum = models.TextField(blank=False)
    isDelivered = models.BooleanField(default=False)
    location = models.TextField()
    canceled = models.BooleanField(default=False)






