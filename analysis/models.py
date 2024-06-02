from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
class User_Result(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='User_Result',blank=True)
    user_text=models.CharField(null=True,max_length=2000)
    positive=models.DecimalField(max_digits=20,decimal_places=20)
    negative=models.DecimalField(max_digits=20,decimal_places=20)
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
    duration=models.IntegerField(null=True)
    plan_image=models.ImageField(upload_to="plan_images/",null=True)
    created_at=models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name_plural='Plans'
    def __str__(self):
        return self.name 
class Plan_purchase(models.Model): 
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='PlanBuy')
    plan_name=models.CharField(max_length=50)
    plan_price=models.DecimalField(max_digits=10,decimal_places=2)
    paid=models.BooleanField(default=False)
    plan_expired=models.IntegerField(default=32)
    created_at=models.DateTimeField(default=timezone.now)
    def save(self,*args,**kwargs):
        if self.paid and not self.plan_expired:
            self.expired_date=self.created_at+timedelta(days=self.plan_expired)
        super().save(*args,**kwargs)
    @property 
    def expiration_date(self):
        if self.paid:
            return self.created_at+timedelta(days=self.plan_expired)
        else:
            None
    class Meta:
        verbose_name_plural='Purchase Plans'
    def __str__(self):
        return self.plan_name
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    user_image=models.ImageField(upload_to="profile_images/",null=True,default="media/user.jpg")
    cover_image=models.ImageField(upload_to="profile_images/",null=True,default="media/user.jpg")
    phone_number=models.CharField(max_length=15)
    user_bio=models.TextField()
    def __str__(self):
        return self.user.username
    





    


