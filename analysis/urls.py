
from django.urls import path
from analysis.views import * #mean all you write only name in path
urlpatterns = [
    #url mapping
    path('',index,name='index'), 
    path('user_result',user_result,name='user_result'),
    path('sentimental_analysis',sentimental_analysis,name='sentimental_analysis'),
    path('user_history',user_history,name='user_history'),
]
