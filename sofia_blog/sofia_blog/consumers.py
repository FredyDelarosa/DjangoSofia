import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.core.serializers.json import DjangoJSONEncoder
from .models.article import Article
from channels.db import database_sync_to_async  

class ArticleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_layer = get_channel_layer()
        await self.channel_layer.group_add("articles", self.channel_name)
        await self.accept()
        
        # Obtener artículos existentes y enviarlos al cliente que se conecta
        articles = await self.get_articles()
        await self.send(text_data=json.dumps({"type": "article_list", "articles": articles}))

    @database_sync_to_async
    def get_articles(self):
        """Consulta la base de datos de forma segura en un contexto asíncrono."""
        return list(Article.objects.values("id", "title", "content"))

    @database_sync_to_async
    def create_article(self, title, content):
        from django.contrib.auth.models import User
        user = User.objects.filter(username="fredy").first()

        if not user:
            return None  # Si no existe el usuario, no se crea el artículo

        article = Article.objects.create(title=title, content=content, author=user)
        return article


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("articles", self.channel_name)

    async def receive(self, text_data):
        print("📩 Mensaje recibido en WebSocket:", text_data)  # <-- Verifica si el servidor recibe el mensaje

        data = json.loads(text_data)

        if data["action"] == "create_article":
            print("✅ Creando artículo:", data)  # <-- Debe aparecer en la terminal si el mensaje llega

            article = await self.create_article(data["title"], data["content"])

            if not article:
                await self.send(text_data=json.dumps({"error": "No se pudo crear el artículo."}))
                return

            response = {
                "type": "new_article",
                "id": article.id,
                "title": article.title,
                "content": article.content,
                "author": article.author.username
            }

            print("📢 Enviando nuevo artículo a todos los clientes:", response)  # <-- Debe aparecer en logs

            await self.channel_layer.group_send(
                "articles",
                {
                    "type": "broadcast_article",
                    "data": response
                }
            )
            
            
    async def broadcast_article(self, event):
        """Enviar un nuevo artículo a todos los clientes conectados."""
        print("📡 Enviando actualización a clientes:", event["data"])

        # Enviar el mensaje a todos los clientes conectados al grupo 'articles'
        await self.channel_layer.group_send(
            "articles",
            {
                "type": "send_article_update",
                "data": event["data"]
            }
        )
        
        await self.send_article_update(event)

    async def send_article_update(self, event):
        """Función encargada de enviar el mensaje a los clientes conectados."""
        print("🚀 Enviando actualización a todos los clientes:", event["data"])
        
        # Enviar el mensaje a cada cliente conectado
        await self.send(text_data=json.dumps(event["data"], cls=DjangoJSONEncoder))


