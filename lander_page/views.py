from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from lander_page.models import Contact
from datetime import datetime
from pytz import timezone
import telegram
from django.conf import settings
import requests as external_request


# Create your views here.
def index(request):
    return render(request,"index.html")


    # return render(,"thankyou.html")

class ContactFormView:
    def __init__(self):
        # self.bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID

    def submit(self,request):
        if request.method == 'POST':
            name = request.POST.get("name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            msg = request.POST.get("message")
            contact_obj = Contact(name=name,email=email,phone=phone,message=msg,contact_time=datetime.now(timezone('Asia/Kolkata')))
            contact_obj.save()
            response = self.send_telegram_message(contact_obj)
            if response['ok']:
                message = "Thank you! Your submission has been received![Via Telegram]"
            else:
                message = "Thank you! Your submission has been received!"
                print(response)
            messages.success(request, message)
        return redirect("/")
    
    def send_telegram_message(self, submission):
        message = f"New contact form submission:\n\n DateTime : {submission.contact_time}\n\nName: {submission.name}\nPhone Number: {submission.phone}\nEmail: {submission.email}\nMessage: {submission.message}"
        # await self.bot.send_message(chat_id=self.chat_id, text=message)
        send_text = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + self.chat_id + '&parse_mode=Markdown&text=' + message
        response = external_request.get(send_text)
        return response.json()
