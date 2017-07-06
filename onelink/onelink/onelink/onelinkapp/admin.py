from django.contrib import admin

from .models import UserDetail
from .models import UserSession
from .models import UserVerificationSession
from .models import ServiceCategory
from .models import ServiceSubCategory
from .models import ServiceMap
from .models import ItemMap
from .models import ServiceRequest
from .models import ServiceNotification
from .models import ItemNotification
from .models import FavouriteService
from .models import ProductCategory
from .models import OrderHistory
from .models import ItemOrderHistory
from .models import ItemRequest
from .models import RequestMessage
from .models import Review



from .models import Stock
admin.site.register(Stock)


admin.site.register(UserDetail)
admin.site.register(UserSession)
admin.site.register(UserVerificationSession)
admin.site.register(ServiceCategory)
admin.site.register(ServiceSubCategory)
admin.site.register(ServiceMap)
admin.site.register(ItemMap)
admin.site.register(ServiceRequest)
admin.site.register(ItemRequest)
admin.site.register(ServiceNotification)
admin.site.register(ItemNotification)
admin.site.register(FavouriteService)
admin.site.register(ProductCategory)
admin.site.register(OrderHistory)
admin.site.register(ItemOrderHistory)
admin.site.register(RequestMessage)
admin.site.register(Review)
