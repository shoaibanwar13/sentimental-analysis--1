
from django.urls import path
from analysis.views import * #mean all you write only name in path
from django.contrib.auth import views

urlpatterns = [
    #url mapping
    path('',index,name='index'), 
     
    path('sentimental_analysis/',sentimental_analysis,name='sentimental_analysis'),
    path('user_history/',user_history,name='user_history'),
    path('features/',features,name='features'),
    path('chat_form/',chat_form,name='chat_form'),
    path('plan_detail/<str:id>',plan_detail,name='plan_detail'),
    path('start_order/', start_order, name='start_order'),
    path('payment_success/',payment_success,name='payment_success'),
    path('payment_cancel/',payment_cancel,name='payment_cancel'),
    path('limit_reached/',limit_reached,name='limit_reached'),
    path('pricing/',pricing,name='pricing'),
    path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),

    path('logout/',  logoutfunction, name='logout'),
]
