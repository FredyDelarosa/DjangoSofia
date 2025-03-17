import json
import asyncio
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

        # Iniciar la tarea en segundo plano para verificar nuevos artículos
        self.check_articles_task = asyncio.create_task(self.check_for_new_articles())

    @database_sync_to_async
    def get_articles(self):
        """Consulta la base de datos de forma segura en un contexto asíncrono."""
        return list(Article.objects.values("id", "title", "content"))

    @database_sync_to_async
    def get_latest_article(self):
        """Obtiene el artículo más reciente de la base de datos."""
        latest_article = Article.objects.order_by('-id').first()
        return {
            "id": latest_article.id,
            "title": latest_article.title,
            "content": latest_article.content,
            "author": latest_article.author.username
        } if latest_article else None

    async def check_for_new_articles(self):
        """Revisa cada 3 segundos si hay un nuevo artículo en la base de datos."""
        last_article_id = None  # Guardamos el ID del último artículo enviado

        while True:
            await asyncio.sleep(3)  # Espera 3 segundos antes de verificar nuevamente

            latest_article = await self.get_latest_article()

            if latest_article and latest_article["id"] != last_article_id:
                last_article_id = latest_article["id"]

                print("🆕 Nuevo artículo detectado en la base de datos:", latest_article)

                await self.channel_layer.group_send(
                    "articles",
                    {
                        "type": "send_article_update",
                        "data": {"type": "new_article", **latest_article}
                    }
                )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("articles", self.channel_name)
        if hasattr(self, "check_articles_task"):
            self.check_articles_task.cancel()  # Cancelamos la tarea al desconectar

    async def receive(self, text_data):
        print("📩 Mensaje recibido en WebSocket:", text_data)  

        data = json.loads(text_data)

        if data["action"] == "create_article":
            print("✅ Creando artículo:", data)  

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

            print("📢 Enviando nuevo artículo a todos los clientes:", response)

            await self.channel_layer.group_send(
                "articles",
                {
                    "type": "send_article_update",
                    "data": response
                }
            )
    
    async def send_article_update(self, event):
        """Enviar el articulo al websocket del cliente"""
        print("📡 Enviando actualización a cliente:", event["data"])
        await self.send(text_data=json.dumps(event["data"]))

    @database_sync_to_async
    def create_article(self, title, content):
        from django.contrib.auth.models import User
        user = User.objects.filter(username="fredy").first()

        if not user:
            return None  

        article = Article.objects.create(title=title, content=content, author=user)
        return article
