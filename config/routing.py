from channels.routing import route, include
from gglobal.cms.consumers import phone_numbers_connect, phone_numbers_recive, phone_numbers_disconnect
from gglobal.crm.consumers import ws_add, ws_disconnect


onlinestatus_channel_routing = [
    route("websocket.connect", ws_add),
    route("websocket.disconnect", ws_disconnect),
]

phonenumbers_channel_routing = [
    route("websocket.connect", phone_numbers_connect),
    route("websocket.receive", phone_numbers_recive),
    route("websocket.disconnect", phone_numbers_disconnect)
]

channel_routing = [
    include(phonenumbers_channel_routing, path=r'^/phonenumbers/'),
    include(onlinestatus_channel_routing, path=r'^/onlinestatus/'),
]


