from django.db import models

class User(models.Model):
    uid=models.AutoField(primary_key=True)
    email = models.EmailField(blank=False,unique=True)
    activation_key=models.CharField(max_length=16,default="nokey")
    password=models.CharField(max_length=8,null=True)

    def __str__(self):
        return self.email

class UserDetail(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    fname=models.CharField(max_length=15)
    lname=models.CharField(max_length=15)
    phno=models.CharField(max_length=10)
    sex=models.CharField(max_length=1)

    def __str__(self):
        return self.fname

class Shop(models.Model):
    MEDICINE = 1
    GROCERY = 2
    DAIRY = 3
    OTHER=4
    categories=(
        (MEDICINE,('Medicines')),
        (GROCERY,('Groceries')),
        (DAIRY,('Dairy')),
        (OTHER,('Other Needs'))
    )
    shopid=models.AutoField(primary_key=True)
    shop_name=models.CharField(max_length=30,default="")
    shop_owner=models.CharField(max_length=30)
    shop_address=models.CharField(max_length=140)
    shop_category=models.PositiveSmallIntegerField(choices=categories,default=OTHER)

class Slots(models.Model):
    
    shopid=models.ForeignKey(Shop,on_delete=models.CASCADE)
    slot_date=models.DateField(auto_now=True)
    slot_time=models.TimeField()
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    user_phno=models.CharField(max_length=10)