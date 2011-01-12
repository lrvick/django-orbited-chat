import json,stomp,datetime,time
from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import Message
from django.conf import settings

conn = stomp.Connection()
conn.start()
conn.connect()
conn.subscribe(destination='/messages', ack='auto')

def index(request):
    """
    handle the index request
    """
    messages = Message.objects.all()
    return render_to_response("index.html", {
        "messages":messages, 
        "orbited_server":settings.ORBITED_SERVER,
        "orbited_port":settings.ORBITED_PORT,
        "orbited_stomp_port":settings.ORBITED_STOMP_PORT,
    })

def addMessage(request):
    user = request.POST.get("user", "nobody")
    message = request.POST.get("message", "")
    time = datetime.datetime.now()
    msg = Message(user=user, body=message, time=time)
    msg.save()
    msg_to_send = json.dumps({"user":user,"message":message, "time":time.strftime("%H:%S-%d/%m/%Y")})
    conn.send(msg_to_send, destination='/messages')
    return HttpResponse("ok")
