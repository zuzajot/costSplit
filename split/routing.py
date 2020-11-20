from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from . import consumers

websocket_urlpatterns = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("groups/", consumers.CostConsumer),
    ]),
})

# from django.urls import re_path
#
# from . import consumers
#
# websocket_urlpatterns = [
#     re_path(r'ws/cost/(?P<cost_id>\w+)/$', consumers.CostConsumer.as_asgi()),
# ]