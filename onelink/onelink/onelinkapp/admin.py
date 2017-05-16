from django.contrib import admin

from .models import UserDetail
from .models import UserSession
from .models import UserVerificationSession
from .models import ServiceCategory
from .models import ServiceSubCategory
from .models import ServiceMap
from .models import ItemMap


from .models import Stock
admin.site.register(Stock)


admin.site.register(UserDetail)
admin.site.register(UserSession)
admin.site.register(UserVerificationSession)
admin.site.register(ServiceCategory)
admin.site.register(ServiceSubCategory)
admin.site.register(ServiceMap)
admin.site.register(ItemMap)
