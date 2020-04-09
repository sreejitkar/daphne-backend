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
