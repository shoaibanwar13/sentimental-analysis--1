from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class User_Result(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='User_Result',blank=True)
    user_text=models.CharField(null=True,max_length=2000)
    positive=models.DecimalField(max_digits=20,decimal_places=20)
    negative=models.DecimalField(max_digits=20,decimal_places=20)
    neutral=models.DecimalField(max_digits=20,decimal_places=20)
    result=models.CharField(null=True,max_length=30)
    class Meta:
        verbose_name_plural='User Result'
    def __str__(self):
        return f"{self.user.username}-{self.result}"
class Plans(models.Model):
    name=models.CharField(null=True,max_length=100)
    plan_description=models.TextField()
    plan_pricing=models.DecimalField(max_digits=10,decimal_places=2)
    discount=models.CharField(max_length=10)
    benefit1=models.CharField(max_length=20)
    benefit2=models.CharField(max_length=20)
    benefit3=models.CharField(max_length=20)
    benefit4=models.CharField(max_length=20)
    duration=models.IntegerField(null=True)
    created_at=models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name_plural='Plans'
    def __str__(self):
        return self.name


    



