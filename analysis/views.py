from django.shortcuts import render,redirect
import requests
from .models import User_Result
API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest" #API URL 
headers = {"Authorization": "Bearer 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"} #Authentication Token of your account
def query(payload):#this fun use for sending request to api and get response mean result
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json() 
#mape the function with index page 
def index(request):

    return render(request,'index.html')
def user_result(request):
    return render(request,'user_result.html')
def sentimental_analysis(request):
    if request.method=='POST':
        input_text=request.POST.get('text','')
        output=query({"inputs":input_text})
        print(output)
        if isinstance(output,list) and output:
             sentiment_prediction=output[0]
             predict={prediction['label']:prediction['score']for prediction in sentiment_prediction}
             print(predict)
             positive_score=predict.get('positive',0.00)
             negative_score=predict.get('negative',0.00)
             neutral_score=predict.get('neutral',0.00)
             print(positive_score,negative_score,neutral_score)
             if positive_score > negative_score and positive_score > neutral_score:
                        result = 'positive'
             elif negative_score > positive_score and negative_score > neutral_score:
                        result = 'negative'
             else:
                        result = 'neutral'
             data=User_Result(user=request.user,user_text=input_text,positive=positive_score,negative=negative_score,neutral=neutral_score,result=result)
             data.save()   

            
    return render(request,'sentimental_analysis.html')