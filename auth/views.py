from django.shortcuts import render,redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utlis import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
#function base view
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            instance=form.save()
            user=User.objects.get(id=instance.id)
            user.is_active=False
            user.save()
            email_subject="Activate Your Account"
            message=render_to_string('activate.html',{
            'user':user,
            'domain':'https://sentimentalanalysis-uhvm.onrender.com',            #https://sentimentalanalysis-uhvm.onrender.com
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)

        })
            email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[request.POST.get('email')])
            email_message.send()
        return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
 #class base view   
class ActtivateAccountView(View):
     def get(self,request,uidb64,token):
            try:
                uid=force_str(urlsafe_base64_decode(uidb64))
                user=User.objects.get(pk=uid)
            except Exception as identifier:
                 user=None
            if user is not None and generate_token.check_token(user,token):
               user.is_active=True
               user.save()
               return redirect('emailconfirm')
            else:
                return redirect('activate_fail')

 
def emailconfirm(request):
    return render(request,'activated.html')
def activate_fail(request):
    return render(request,'activatefail.html')
   
def logoutfunction(request):
    logout(request)
    return redirect('/')

