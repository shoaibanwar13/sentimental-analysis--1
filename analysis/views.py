from django.shortcuts import render,redirect,get_object_or_404
import requests
from .models import User_Result,Plans 
from django.contrib.auth.decorators import login_required
API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest" #API URL 
headers = {"Authorization": "Bearer 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"} #Authentication Token of your account
#query func send req to API 
def query(payload):
    #this fun use for sending request to api and get response mean result
	response = requests.post(API_URL, headers=headers, json=payload)
     #data return 
	return response.json()  
def contactus(request):
     user_data=User_Result.objects.filter(user=request.user)
     return render(request,'contact.html',{'user_data':user_data})
def index(request):
    plan=Plans.objects.all()
    print(plan)
    return render(request,'index.html',{'plan':plan})
def user_result(request):
    return render(request,'user_result.html')
@login_required
def sentimental_analysis(request):
    if request.method=='GET': #check if request is GET
        input_text=request.GET.get('text','') #store input_text from form 
        output=query({"inputs":input_text})#call query function to get results
        print(output)
        #check instance if it contain data
        if isinstance(output, list) and output:
            #store output from zero index
            sentiment_predictions = output[0]
             #store result in form of json format
            predict={prediction['label']:prediction['score']for prediction in sentiment_predictions}
            positive_score=predict.get('positive',0.00) #covert from json format to normal form (decimal)
            negative_score=predict.get('negative',0.00)
            neutral_score=predict.get('neutral',0.00)
            print(positive_score,negative_score,neutral_score)
            # comparing condition in result variable
            if positive_score > negative_score and positive_score > neutral_score:
                result = 'positive'
            elif negative_score > positive_score and negative_score > neutral_score:
                result = 'negative'
            else:
               result = 'neutral'
               # store data in db 
            data=User_Result(user=request.user,user_text=input_text,positive=positive_score,negative=negative_score,neutral=neutral_score,result=result)
            data.save()  
            
        
            context={ 
                'positive_score':positive_score,
                'negative_score':negative_score,
                'neutral_score':neutral_score,
                'result':result,
                'input_text':input_text,
            

        
             }
       
      
            return render(request,'result.html',context)
         
        
    return render(request,'result.html')
def user_history(request):
      # get all results of user from database 
        user_data=User_Result.objects.filter(user=request.user)
        return render(request,'history.html',{'user_data':user_data})
def plan_detail(request,id):
     plan_detail=get_object_or_404(Plans,id=id) 
     print(plan_detail)
     return render(request,'plan_detail.html',{'plan_detail':plan_detail})


  
