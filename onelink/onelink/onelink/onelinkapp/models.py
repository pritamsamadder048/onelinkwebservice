from django.db import models
from django.core.validators import MaxValueValidator
import random
import hashlib
from datetime import datetime





class Stock(models.Model):
    ticker=models.CharField(max_length=10)
    open=models.FloatField()
    close=models.FloatField()
    volume=models.IntegerField()

    def __str__(self):
        return self.ticker





# UserDetail table

# def profile_picture_upload_location(instance, filename):
#     return "%s/profile_pictures/%s" % (instance.id, filename)







def generate_hash():
    key = str(random.Random().randint(1, 10000))
    m = hashlib.sha1(bytes(key, encoding="UTF-8"))
    digest = m.hexdigest()
    return (key, digest)










class UserDetail(models.Model):

    full_name = models.CharField(max_length=500)

    email = models.EmailField(blank=True,null=True)
    mobile=models.CharField(unique=True,max_length=20)
    pincode=models.CharField(max_length=10)

    country = models.TextField();
    city = models.TextField();
    district = models.TextField(null=True,blank=True);
    building = models.TextField(null=True,blank=True);
    street = models.TextField(null=True,blank=True);
    key = models.CharField(max_length=40)
    password = models.CharField(max_length=200)
    user_type = models.IntegerField(default=0)
    user_image=models.TextField(null=True,blank=True)

    user_createtime = models.DateTimeField(auto_now_add=True)
    # profile_picture = models.ImageField(upload_to=profile_picture_upload_location,
    #                                     null=True,
    #                                     blank=True,
    #                                     height_field="height_field",
    #                                     width_field="width_field")
    # height_field = models.IntegerField(default=0)
    # width_field = models.IntegerField(default=0)
    validemail = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

    def set_password(self, raw_password):
        self.key = str(random.Random().randint(1, 10000))

        m = hashlib.sha1(bytes(self.key, encoding="UTF-8"))
        m.update(bytes(raw_password, encoding="UTF-8"))
        self.password = m.hexdigest()
        # return password

    def check_password(self, raw_password):
        m = hashlib.sha1(bytes(self.key, encoding="UTF-8"))
        m.update(bytes(raw_password, encoding="UTF-8"))
        return m.hexdigest() == self.password


# UserSession Table
class UserSession(models.Model):
    full_name = models.CharField(max_length=500)
    email = models.EmailField(blank=True,null=True)
    mobile = models.CharField(unique=True,max_length=20)
    User_Type=models.IntegerField()
    UserSession_starttime = models.DateTimeField(auto_now_add=True)
    UserSession_lastmodifiedtime = models.DateTimeField(auto_now=True)
    UserDetail_ref = models.OneToOneField(UserDetail, on_delete=models.CASCADE, primary_key=True)  # ,to_field='id')
    UserDetail_id = models.IntegerField(unique=True)
    UserSession_key = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.full_name

    def set_sessionkey(self):
        key = str(random.Random().randint(1, 10000))
        m = hashlib.sha1(bytes(key, encoding="UTF-8"))
        self.UserSession_key = m.hexdigest()

        return self.UserSession_key

    def check_sessionkey(self, clientsessionkey):
        return self.UserSession_key == clientsessionkey


# User verification Session Table
class UserVerificationSession(models.Model):
    full_name = models.CharField(max_length=500)
    session_starttime = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True,null=True)
    mobile = models.CharField(unique=True,max_length=20)
    User_Type = models.IntegerField()
    UserDetail_ref = models.OneToOneField(UserDetail, on_delete=models.CASCADE, primary_key=True)
    UserDetail_id = models.IntegerField(unique=True)
    UserSession_key = models.CharField(max_length=200, unique=True)
    verificationtype = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.full_name

    def set_sessionkey(self):
        key = str(random.Random().randint(1, 10000))
        m = hashlib.sha1(bytes(key, encoding="UTF-8"))
        self.UserSession_key = m.hexdigest()

        return self.UserSession_key

    def check_sessionkey(self, clientsessionkey):
        return self.UserSession_key == clientsessionkey




def service_image_upload_location(instance,filename):
    return "%s/service_image/%s"%(instance.service_name,filename)


class ServiceCategory(models.Model):

    service_name = models.CharField(max_length=500)
    service_detail = models.TextField()


    service_image=models.ImageField(upload_to=service_image_upload_location,
                                      null=True,
                                      blank=True,
                                      height_field="height_field",
                                      width_field="width_field")

    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)


    def __str__(self):
        return self.service_name


def product_image_upload_location(instance,filename):
    return "%s/product_image/%s"%(instance.product_name,filename)



class ProductCategory(models.Model):

    product_name = models.CharField(max_length=500)
    product_detail = models.TextField()


    product_image=models.ImageField(upload_to=product_image_upload_location,
                                      null=True,
                                      blank=True,
                                      height_field="height_field",
                                      width_field="width_field")

    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)


    def __str__(self):
        return self.product_name



class ServiceSubCategory(models.Model):

    sub_service_name=models.CharField(max_length=500)
    sub_service_detail = models.TextField();
    service_categorgy_id=models.IntegerField()
    service_categorgy_ref=models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)





    def __str__(self):
        return self.sub_service_name





class ServiceMap(models.Model):


    serviceprovider_id=models.IntegerField()
    service_name=models.CharField(max_length=500,blank=True,null=True)
    license_no = models.CharField(max_length=40,blank=True,null=True)
    under_gov = models.CharField(max_length=40,blank=True,null=True)
    service_details=models.TextField(blank=True,null=True)
    serviceprovider_email=models.EmailField(blank=True,null=True)
    mobile = models.CharField(max_length=20,blank=True,null=True)
    service_category_id=models.IntegerField()
    service_ref=models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    servicemap_image=models.TextField(null=True,blank=True)
    #subservice_id=models.IntegerField()
    areapincode=models.CharField(max_length=10)
    register_time=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    service_type=models.CharField(max_length=40,null=True,blank=True)




    def __str__(self):
        return self.service_name




def item_image_upload_location(instance,filename):
    return "%s/item_image/%s"%(instance.serviceprovider_id,filename)
class ItemMap(models.Model):


    serviceprovider_id = models.IntegerField()
    serviceprovider_email = models.EmailField(blank=True,null=True)
    mobile = models.CharField(max_length=20)
    product_category_id = models.IntegerField()
    product_ref = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    item_name=models.CharField(max_length=500)
    item_details=models.TextField()
    item_features=models.TextField(blank=True,null=True)
    #areapincode = models.PositiveIntegerField()
    # item_image = models.ImageField(upload_to=item_image_upload_location,
    #                                   null=True,
    #                                   blank=True,
    #                                   height_field="height_field",
    #                                   width_field="width_field")
    #
    # height_field = models.IntegerField(default=0)
    # width_field = models.IntegerField(default=0)



    item_MRP=models.FloatField()
    item_SLP=models.FloatField()

    itemmap_image1=models.TextField(null=True,blank=True)
    itemmap_image2=models.TextField(null=True,blank=True)
    itemmap_image3=models.TextField(null=True,blank=True)
    itemmap_image4=models.TextField(null=True,blank=True)
    itemmap_image5=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.item_name


class ServiceRequest(models.Model):

    serviceprovider_id = models.IntegerField()
    serviceprovider_ref=models.ForeignKey(UserDetail,related_name='providerdetail', on_delete=models.CASCADE)
    request_type = models.CharField(default="SERVICE", max_length=40)



    user_id = models.IntegerField()
    user_ref = models.ForeignKey(UserDetail,related_name='userdetail', on_delete=models.CASCADE)

    service_category_id = models.IntegerField()

    service_map_id = models.IntegerField()
    service_map_ref = models.ForeignKey(ServiceMap, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=40, null=True, blank=True)
    read=models.BooleanField(default=False)




    areapincode = models.CharField(max_length=10)
    service_request_address=models.TextField(null=True,blank=True)

    request_time = models.DateTimeField(auto_now_add=True)
    service_time=models.CharField(null=True,blank=True,max_length=200)
    request_detail=models.TextField(blank=True,null=True)
    request_image=models.TextField(blank=True,null=True)

    service_status=models.IntegerField(default=0)
    notification = models.TextField(blank=True, null=True)
    final_budget=models.FloatField(default=0)

    def getMessage(self):
        message = self.user_ref.full_name + " has requested for "+self.serviceprovider_ref.full_name+ "'s service : " + self.service_map_ref.service_name
        return message

    def __str__(self):
        return self.service_map_ref.service_name




class OrderHistory(models.Model):

    serviceprovider_id = models.IntegerField()
    serviceprovider_ref=models.ForeignKey(UserDetail,related_name='ohproviderdetail', on_delete=models.CASCADE)



    user_id = models.IntegerField()
    user_ref = models.ForeignKey(UserDetail,related_name='ohuserdetail', on_delete=models.CASCADE)

    #service_category_id = models.IntegerField()

    service_map_id = models.IntegerField()
    service_map_ref = models.ForeignKey(ServiceMap,related_name='ohservicemap' ,on_delete=models.CASCADE)

    service_request_id=models.IntegerField()
    service_request_ref=models.ForeignKey(ServiceRequest,related_name='ohservicerequest',on_delete=models.CASCADE)
    confirmation_id=models.CharField(null=True,blank=True,max_length=500)
    models.CharField(blank=True, null=True, default="SERVICE", max_length=10)
    service_status = models.IntegerField(default=1)
    service_type = models.CharField(max_length=40, null=True, blank=True)


    booked_time = models.DateTimeField(auto_now_add=True)
    review_written=models.BooleanField(default=False)


    def __str__(self):
        return self.service_map_ref.service_name



class ServiceNotification(models.Model):

    serviceprovider_id = models.IntegerField()
    serviceprovider_ref = models.ForeignKey(UserDetail, related_name='notiproviderdetail', on_delete=models.CASCADE)
    servicerequest_id = models.IntegerField()
    servicerequest_ref=models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now_add=True)
    request_type=models.CharField(blank=True,null=True,default="SERVICE",max_length=10)
    service_type = models.CharField(max_length=40, null=True, blank=True)

    read=models.BooleanField(default=False)
    notification=models.TextField(blank=True,null=True)

    def getMessage(self):
        message = self.servicerequest_ref.user_ref.full_name + " has requested for your service "#: " + self.servicerequest_ref.service_map_ref.service_name
        return message

    def __str__(self):
        return  self.getMessage()


class FavouriteService(models.Model):
    user_id=models.IntegerField()
    servicemap_id=models.IntegerField()
    servicemap_ref=models.ForeignKey(ServiceMap,on_delete=models.CASCADE)

    def __str__(self):
        return self.servicemap_ref.service_name











class ItemRequest(models.Model):

    serviceprovider_id = models.IntegerField()
    serviceprovider_ref=models.ForeignKey(UserDetail,related_name='itemproviderdetail', on_delete=models.CASCADE)
    request_type=models.CharField(default="PRODUCT",max_length=40)
    # history_id=models.IntegerField(null=True,blank=True)
    # history_ref=models.ForeignKey(ItemOrderHistory,related_name='itemorderhistoryref', on_delete=models.CASCADE,null=True,blank=True)



    user_id = models.IntegerField()
    user_ref = models.ForeignKey(UserDetail,related_name='itemuserdetail', on_delete=models.CASCADE)

    item_category_id = models.IntegerField()

    item_map_id = models.IntegerField()
    item_map_ref = models.ForeignKey(ItemMap, on_delete=models.CASCADE)
    item_quantity=models.IntegerField(default=1)
    read=models.BooleanField(default=False)



    areapincode = models.CharField(null=True,blank=True,max_length=10)
    item_request_address=models.TextField(null=True,blank=True)

    request_time = models.DateTimeField(auto_now_add=True)
    #item_delivery_time=models.CharField(null=True,blank=True)
    request_detail=models.TextField(blank=True,null=True)
    final_budget = models.FloatField(default=0)

    item_status=models.IntegerField(default=0)
    notification = models.TextField(blank=True, null=True)

    paid=models.BooleanField(default=False)
    payment_state=models.CharField(max_length=40,null=True,blank=True)
    payment_id=models.CharField(max_length=500,null=True,blank=True)
    payment_time=models.CharField(max_length=40,null=True,blank=True)

    def getMessage(self):
        message = self.user_ref.full_name + " has requested for " + self.serviceprovider_ref.full_name + "'s Product : " + self.item_map_ref.item_name
        return message

    def __str__(self):
        return self.item_map_ref.item_name





class ItemOrderHistory(models.Model):

    serviceprovider_id = models.IntegerField()
    serviceprovider_ref=models.ForeignKey(UserDetail,related_name='iohproviderdetail', on_delete=models.CASCADE)



    user_id = models.IntegerField()
    user_ref = models.ForeignKey(UserDetail,related_name='iohuserdetail', on_delete=models.CASCADE)

    #service_category_id = models.IntegerField()

    item_map_id = models.IntegerField()
    item_map_ref = models.ForeignKey(ItemMap,related_name='iohservicemap' ,on_delete=models.CASCADE)

    item_request_id=models.IntegerField()
    item_request_ref=models.ForeignKey(ItemRequest,related_name='iohsitemrequest',on_delete=models.CASCADE)
    confirmation_id = models.CharField(null=True, blank=True, max_length=500)
    request_type=models.CharField(blank=True, null=True, default="PRODUCT",max_length=10)
    review_written = models.BooleanField(default=False)
    item_status = models.IntegerField(default=1)

    paid = models.BooleanField(default=False)
    payment_state = models.CharField(max_length=40, null=True, blank=True)
    payment_id = models.CharField(max_length=500, null=True, blank=True)
    payment_time = models.CharField(max_length=40, null=True, blank=True)


    booked_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.item_map_ref.item_name


class ItemNotification(models.Model):

    serviceprovider_id = models.IntegerField()
    serviceprovider_ref = models.ForeignKey(UserDetail, related_name='inotiproviderdetail', on_delete=models.CASCADE)
    itemrequest_id = models.IntegerField()
    itemrequest_ref=models.ForeignKey(ItemRequest, on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now_add=True)
    request_type = models.CharField(blank=True, null=True, default="PRODUCT",max_length=10)

    read=models.BooleanField(default=False)
    notification=models.TextField(blank=True,null=True)

    def getMessage(self):
        message = self.itemrequest_ref.user_ref.full_name + " has requested for your product "#: " + self.itemrequest_ref.item_map_ref.item_name
        return message

    def __str__(self):
        return  self.getMessage()

class FavouriteItem(models.Model):
    user_id=models.IntegerField()
    itemmap_id=models.IntegerField()
    itemmap_ref=models.ForeignKey(ItemMap,on_delete=models.CASCADE)

    def __str__(self):
        return self.itemmap_ref.item_name


class RequestMessage(models.Model):
    request_id=models.IntegerField()
    servicerequest_ref= models.ForeignKey(ServiceRequest, related_name='msgsservicerequest', on_delete=models.CASCADE,null=True,blank=True)
    itemrequest_ref= models.ForeignKey(ItemRequest, related_name='msgsservicerequest', on_delete=models.CASCADE,null=True,blank=True)
    sender_id=models.IntegerField()
    sender_ref= models.ForeignKey(UserDetail, related_name='msgsender', on_delete=models.CASCADE)
    receiver_id=models.IntegerField()
    receiver_ref= models.ForeignKey(UserDetail, related_name='msgreceiver', on_delete=models.CASCADE)
    sending_time=models.DateTimeField(auto_now_add=True)
    message_text=models.TextField()
    request_type=models.CharField(max_length=10)
    read=models.BooleanField(default=False)

    def __str__(self):
        return "Sender : "+self.sender_ref.full_name+"   Receiver : "+self.receiver_ref.full_name







class Review(models.Model):
    service_star=models.IntegerField()
    quality_star=models.IntegerField()
    value_star=models.IntegerField()
    title=models.TextField()
    comment=models.TextField()
    user_id=models.IntegerField()
    user_ref=models.ForeignKey(UserDetail, related_name='reviewuserdetail', on_delete=models.CASCADE)
    user_name=models.CharField(max_length=500)
    provider_id=models.IntegerField()
    provider_ref=models.ForeignKey(UserDetail, related_name='reviewproviderdetail', on_delete=models.CASCADE)
    map_id=models.IntegerField(null=True,blank=True)
    servicemap_ref = models.ForeignKey(ServiceMap, related_name='reviewservicemap', on_delete=models.CASCADE,null=True, blank=True)
    itemmap_ref = models.ForeignKey(ItemMap, related_name='reviewitemmap', on_delete=models.CASCADE,null=True, blank=True)
    history_id = models.IntegerField(null=True, blank=True)
    servicehistory_ref = models.ForeignKey(OrderHistory, related_name='reviewservicehistory',on_delete=models.CASCADE, null=True, blank=True)
    itemhistory_ref = models.ForeignKey(ItemOrderHistory, related_name='reviewitemhistory', on_delete=models.CASCADE,null=True, blank=True)
    review_type=models.CharField(max_length=40)#,null=True,blank=True)
    review_time=models.DateTimeField(auto_now_add=True)
