from rest_framework import serializers


from  .models import UserDetail
from .models import UserSession
from .models import Stock
from .models import ServiceCategory
from .models import ServiceSubCategory
from  .models import ServiceMap
from .models import ItemMap


class StockSerializer(serializers.ModelSerializer):


    class Meta:
        model=Stock
        fields='__all__'






#User Detail serializer
class UserDetailSerializer(serializers.ModelSerializer):


    class Meta:
        model=UserDetail
        fields="__all__"



class ServiceCategorySerializer(serializers.ModelSerializer):


    class Meta:
        model=ServiceCategory
        fields=('id','service_name','service_detail','service_image')


class ServiceSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceSubCategory
        fields = ('id', 'sub_service_name', 'sub_service_detail', 'service_categorgy_id')


class ServiceMapSerializer(serializers.ModelSerializer):
    class Meta:
        model=ServiceMap
        fields=('id','serviceprovider_id','service_name',"service_details", 'serviceprovider_email','service_category_id','areapincode')


class ItemMapSerializer(serializers.Serializer):


    class Meta:
        model=ItemMap
        fields=('id','serviceprovider_id','serviceprovider_email','service_category_id','item_name','item_details','item_features','areapincode','item_MRP','item_SLP','iteme_image')