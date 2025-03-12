from django.shortcuts import render

def websocket_view(request):
    return render(request, "articles/websocket_view.html", {"websocket_url": "wss://ebef-187-188-26-191.ngrok-free.app/ws/articles/"})
