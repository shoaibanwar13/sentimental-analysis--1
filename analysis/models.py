from django.db import models
from django.contrib.auth.models import User
class User_Result(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='User_Result',blank=True)
    user_text=models.CharField(null=True,max_length=2000)
    positive=models.DecimalField(max_digits=20,decimal_places=20)
    negative=models.DecimalField(max_digits=20,decimal_places=20)
    neutral=models.DecimalField(max_digits=20,decimal_places=20)
    result=models.CharField(null=True,max_length=30)
    def __str__(self):
        return f"{self.user.username}-{self.result}"

