from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack

from django.urls import path
from split import consumers

websocket_urlPattern=[
    path('ws/polData/', consumers.CostConsumer),
]

application=ProtocolTypeRouter({
    # 'http':
    'websocket': AuthMiddlewareStack(URLRouter(websocket_urlPattern))

})
# import os
#
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# # from django.core.asgi import get_asgi_application
# from split import routing
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'costSplit.settings')
#
# application = ProtocolTypeRouter({
#      "websocket": AuthMiddlewareStack(
#         URLRouter(
#             routing.websocket_urlpatterns
#         )
#     ),
# })
