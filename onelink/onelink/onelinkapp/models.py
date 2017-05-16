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

    email = models.EmailField(unique=True)
    mobile=models.IntegerField(unique=True)
    pincode=models.PositiveIntegerField();
    address=models.TextField();
    key = models.CharField(max_length=40)
    password = models.CharField(max_length=200)
    user_type = models.IntegerField(default=0)

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
    email = models.EmailField(unique=True)
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
    email = models.EmailField(unique=True)
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



class ServiceSubCategory(models.Model):

    sub_service_name=models.CharField(max_length=500)
    sub_service_detail = models.TextField();
    service_categorgy_id=models.IntegerField()
    service_categorgy_ref=models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)





    def __str__(self):
        return self.sub_service_name





class ServiceMap(models.Model):


    serviceprovider_id=models.IntegerField()
    service_name=models.CharField(max_length=500)
    service_details=models.TextField()
    serviceprovider_email=models.EmailField()
    service_category_id=models.IntegerField()
    service_ref=models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    #subservice_id=models.IntegerField()
    areapincode=models.PositiveIntegerField()


    def __str__(self):
        return self.service_name




def item_image_upload_location(instance,filename):
    return "%s/item_image/%s"%(instance.serviceprovider_id,filename)
class ItemMap(models.Model):


    serviceprovider_id = models.IntegerField()
    serviceprovider_email = models.EmailField()
    service_category_id = models.IntegerField()
    service_ref = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    item_name=models.CharField(max_length=500)
    item_details=models.TextField()
    item_features=models.TextField()
    #areapincode = models.PositiveIntegerField()
    item_image = models.ImageField(upload_to=item_image_upload_location,
                                      null=True,
                                      blank=True,
                                      height_field="height_field",
                                      width_field="width_field")

    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    item_MRP=models.FloatField()
    item_SLP=models.FloatField()





class ServiceRequest(models.Model):

    serviceprovider_full_name = models.CharField(max_length=500)
    serviceprovider_id = models.IntegerField()
    serviceprovider_mobile = models.IntegerField()
    serviceprovider_email = models.EmailField()
    serviceprovider_pincode = models.PositiveIntegerField();
    serviceprovider_address = models.TextField();
    service_category_id = models.IntegerField()
    service_ref = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)

    user_full_name = models.CharField(max_length=500)
    user_email = models.EmailField()
    user_mobile = models.IntegerField()
    user_pincode = models.PositiveIntegerField();
    user_address = models.TextField();


    service_name = models.CharField(max_length=500)
    service_details = models.TextField()




    areapincode = models.PositiveIntegerField()