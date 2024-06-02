from django.shortcuts import render,redirect

from .forms import SignUpForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utlis import generate_token
from django.core.mail import EmailMessage
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
            return redirect('emailverification')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
       
def emailverification(request):
    return render(request, 'verification.html')

def profile_edit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('/')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile_edit.html',context)
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
   


def User_profile(request):
    if request.htmx:
        return render(request,'components/User_profile.html')
    else:
        return render(request,'User_profile.html')
    