from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
import requests
from .models import User_Result,Plans,Plan_purchase
from django.http import JsonResponse
from django.contrib.auth import  logout
import stripe
import json
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib import messages
 
from django.utils import timezone
# send email to expire  plan user
def send_mail(email,user,plan_name):
    email_subject2 = "Plan Expire Date Is Approaching "
    message2 = render_to_string('expire_plan.html', {
                'user':user,
                'plan_name':plan_name
                 
        })
    email_message2 = EmailMessage(email_subject2, message2, settings.EMAIL_HOST_USER, [email])
    email_message2.send()
# Function to start a scheduler for sending emails
def start_scheduler(email,user,plan_name):
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mail, 'interval',hours=0,minutes=0,seconds=0,args=[email,user,plan_name])  # Change as needed
    scheduler.start()
#Function to Detect expire plan to  email when plan expire to start schedular
def sendemail():
     
    plans = Plan_purchase.objects.filter(paid=True)
    for plan in plans:
        expiredate=plan.expiration_date
        days_until_expiration = (expiredate - timezone.now()).days
        print(days_until_expiration)
        if 0 < days_until_expiration <= 1:
            user=plan.user
            email=plan.user.email
            plan_name=plan.plan_name
            plan.delete()
            start_scheduler(email,user,plan_name)
#calling sending mail function


 #API URL 
API_URL = "https://api-inference.huggingface.co/models/Remicm/sentiment-analysis-model-for-socialmedia"

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
    return render(request,'index2.html',{'plan':plan})


@login_required
def sentimental_analysis(request):
    try:
        free_trial=User_Result.objects.filter(user=request.user).count()
        print(free_trial)
        user=request.user 
        plan_check=Plan_purchase.objects.filter(user=request.user)

        if free_trial==2 and not plan_check:
           messages.warning(request,"Free trial Limit reached please purchase a plan now")
           return redirect ('limit_reached')
         
    except:
         pass 
    
    
    
    if request.method=='POST': #check if request is GET
        input_text=request.POST.get('text','') #store input_text from form 
        output=query({"inputs":input_text})#call query function to get results
        print(output)
        #check instance if it contain data
        if isinstance(output, list) and output:
            #store output from zero index
            sentiment_predictions = output[0]
             #collect result 
            predict={prediction['label']:prediction['score']for prediction in sentiment_predictions}
            #covert 2D arry Result into jason format
            sentiment_data_json = json.dumps(predict)
            print(sentiment_data_json)
            sentiment_data_dict = json.loads(sentiment_data_json)
            negative_score = sentiment_data_dict["LABEL_0"]
            positive_score=sentiment_data_dict["LABEL_1"]
            print(negative_score,positive_score)

            # comparing condition in result variable
            if positive_score > negative_score:
                result = 'positive'
            else:
               result = 'negative'
            
               # store data in db 
            data=User_Result(user=request.user,user_text=input_text,positive=positive_score,negative=negative_score, result=result)
            data.save()  
           
            
        
            context={ 
                'positive_score':positive_score,
                'negative_score':negative_score,
                 
                'result':result,
                'input_text':input_text,
                'sentiment_scores':sentiment_data_json
            

        
             }
            
       
      
            return render(request,'result.html',context)
         
        
    return render(request,'result.html')
@login_required
def user_history(request):
      # get all results of user from database 
        user_data=User_Result.objects.filter(user=request.user)
        return render(request,'history.html',{'user_data':user_data})
@login_required
def plan_detail(request,id):
     plan_detail=get_object_or_404(Plans,id=id) 
     print(plan_detail)
     pub_key = settings.STRIPE_PUBLIC_KEY
     check=Plan_purchase.objects.filter(user=request.user).exists()
     return render(request,'plan_detail.html',{'plan_detail':plan_detail,'pub_key':pub_key,'check':check})

def pricing(request):
    plan=Plans.objects.all()
    if request.htmx:
        return render(request,'components/pricing.html',{'plan':plan})
    else:
        return render(request,'pricing.html',{'plan':plan})
        
def chat_form(request):
    return render(request,'chat_form.html')

def start_order(request):
    # Extract data from request body
    data = json.loads(request.body)
    # get plan name and paid amount
    name = data.get('name', '')
    raw_paid_amount = data.get('paid_amount', '0.00')
    
    # Convert paid_amount to Decimal
    paid_amount = Decimal(raw_paid_amount)
    
    # Multiply by 100 and format the result
    result = int(paid_amount * Decimal('100.00'))
    
    items = []
    price = result
    
    # Construct line items for Stripe checkout
    items.append({
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': name,
            },
            'unit_amount': price,
        },
        'quantity': 1
    })

    # Create a Stripe checkout session
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
         # pass stripe session values and these value store in stripe account 
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url=request.build_absolute_uri('/payment_success/'),
        cancel_url=request.build_absolute_uri('/payment_cancel/'),
    )
    # data in session stored in this var
    payment_intent = session.payment_intent

    # Create a SitePurchase object to represent the order
    order = Plan_purchase.objects.create(
        user=request.user, 
        plan_name=data['name'], 
        plan_price=data['paid_amount'],
        plan_expired=data['duration'],
        paid=False
    )
    order.save()

    return JsonResponse({'session': session, 'order': payment_intent})
def payment_success(request):
    try:
        # Retrieve the order that needs to be marked as paid
        order = get_object_or_404(Plan_purchase, user=request.user, paid=False)
        order.paid = True
        order.save()
        
        # Extract necessary data from the order
        Plan_name = order.plan_name
        price = order.plan_price
        purchaseid = order.id
        
        # Send a success email to the user
        email_subject = "Thank You for Your Purchase on Sentimental Analysis Tool"
        message = render_to_string('SendEmail.html', {
            'plan_name': Plan_name,
            'user':request.user,
            'plan_price': price,
            'purchaseid': purchaseid
        })
        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [request.user.email])
        email_message.send()

        return render(request, 'success.html')
    except Exception as e:
        print(f"Error: {str(e)}")
        return HttpResponse(status=400)
    
     
def payment_cancel(request):
     return render(request,'cancel.html')

def limit_reached(request):
     return render(request,'limit.html')
def logoutfunction(request):
    logout(request)
    return redirect('/')
def features(request):
    if request.htmx:
        return render(request,'components/features_component.html')
    else:
        return render(request,'features.html')

    