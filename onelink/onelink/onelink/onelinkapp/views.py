from django.shortcuts import render


from django.http import HttpResponse



import datetime
import urllib
from urllib.request import urlopen




from  django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import  Response
from  rest_framework import  status
from rest_framework import generics
from rest_framework import views



import json
import sys,os
import datetime
from datetime import date


from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
from django.core.mail import EmailMessage

import math

from onelink.settings import GMAIL_DETAIL
from .models import generate_hash
from onelink import settings






from .models import Stock
from .serializers import StockSerializer








'''
status_code                                          Meaning

  0----------------------------------------------------not confirmed
  1----------------------------------------------------confirmed
  2----------------------------------------------------paid
  3----------------------------------------------------rejected
  4----------------------------------------------------work started[service] /shipped[product]
  5----------------------------------------------------ongoing[service]
  6----------------------------------------------------on hold[service]
  7----------------------------------------------------work completed[service]
  8----------------------------------------------------payment received[service]
  

'''
class StockList(APIView):

     def get(self,request):

         # stocks=Stock.objects.get(ticker=ticker)
         stocks = Stock.objects.all()
         ss=StockSerializer(stocks,many=True)
         print(type(ss.data))
         return  Response(ss.data)#,headers={'Access-Control-Allow-Origin': '*'})



     # def post(self):
     #     pass
    # def get(self,request):
    #
    #     queryset = Stock.objects.all()
    #     serializer_class = StockSerializer
    # def post(self):
    #     pass


def GetConfirmationId(rtype,rid):
    td=date.today().isoformat().replace("-","")
    tid="OL-"+rtype.upper()+td+str(rid)
    return  tid


def send_gmail(subject="",body="",to_mail=""):
    try:
        GMAIL_CONNECTION = get_connection(host=GMAIL_DETAIL["EMAIL_HOST"],
                            port=GMAIL_DETAIL["EMAIL_PORT"],
                            username=GMAIL_DETAIL["EMAIL_HOST_USER"],
                            password=GMAIL_DETAIL["EMAIL_HOST_PASSWORD"],
                            use_tls=GMAIL_DETAIL["EMAIL_USE_TLS"])
        email = EmailMessage(subject, body, to=[to_mail],connection=GMAIL_CONNECTION)
        email.send(fail_silently=False)
        try:
            GMAIL_CONNECTION.close()
        except:
            pass
        return 0
    except Exception as e:
        print(e)
        try:
            GMAIL_CONNECTION.close()
        except:
            pass
        return 1







from .models import  UserDetail
from .serializers import UserDetailSerializer

from .models import UserSession

from  .models import UserVerificationSession

from .models import ServiceCategory
from .serializers import ServiceCategorySerializer

from .models import ServiceSubCategory
from .serializers import ServiceSubCategorySerializer

from .models import ServiceMap
from .serializers import ServiceMapSerializer


from .models import ItemMap
from .serializers import ItemMapSerializer

# from .models import ServiceRequestChat
# from .serializers import ServiceRequestChatSerializer

from .models import FavouriteService
from .serializers import FavouriteServiceSerializer

# register the user
class RegisterUser(APIView):

    def post(self,request):

        signup_data = {}
        responsedata={}

        try:

            print("trying to register",request.POST)

            for key in request.POST:

                signup_data[key] = request.POST[key].strip()
            print("sign up data : ",signup_data)

            try:
                if ( (not signup_data['mobile']) or (not signup_data['name'])  or (not signup_data['password']) or (not signup_data['pincode']) or (not signup_data['country'])    or (not signup_data['city']) or (not signup_data['user_type'])):

                    #print("not all data",responsedata)

                    print(signup_data)

                    responsedata={"successstatus":"error","message":"please provide all the details necessary"}
                    print(responsedata)

                    return Response(responsedata)
            except:

                #print("not all data except ","   ", responsedata)

                print(signup_data)

                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                return Response(responsedata)


            try:
                ud = UserDetail.objects.get(mobile=signup_data['mobile'])
                if (ud):
                    responsedata={"successstatus":"error","message":"the mobile number is already registered.Please login ."}
                    return Response(responsedata)

            except UserDetail.DoesNotExist:

                pass


            try:


                print("in block")

                ud = UserDetail()
                print("init")
                ud.full_name = signup_data['name']

                if signup_data.get('email',None) is not None:

                    ud.email = signup_data["email"]
                if signup_data.get('user_image',None) is not None:
                    ud.user_image=signup_data['user_image']
                ud.mobile = signup_data['mobile']
                ud.pincode=signup_data["pincode"]
                ud.country=signup_data["country"]
                ud.city=signup_data["city"]
                if(signup_data.get('district',None) is not None):
                    ud.district=signup_data["district"]
                if (signup_data.get('street', None) is not None):
                    ud.street=signup_data["street"]
                if (signup_data.get('building', None) is not None):
                    ud.building=signup_data["building"]

                ud.user_type = signup_data['user_type']

                ud.set_password(signup_data['password'])

                print("trying to save data")

                ud.save()
                print("user details : ",ud)

                #s=sendverificationlink_fun(ud.id)

                #print("sending email...")


                #if (s==0):


                 #   print("success fully sent email")


                responsedata={"successstatus":"ok","message":"you have successfully registered. now login to continue"}
                print(responsedata)
                return Response(responsedata)
                #else:


                #    print("error occured trying to send email")

                #    responsedata = {"successstatus": "error", "message": "error occured.could not send the email."}
                #    return Response(responsedata)

            except Exception as e:

                print("in inner except : ",e)
                responsedata = {"successstatus": "error", "message": "unknown error. Please try again"}
                return Response(responsedata)



        except:


            print("in outer except")
            responsedata = {"successstatus": "error", "message": "unknown error. Please try again"}
            return Response(responsedata)






class UpdateUser(APIView):
    def post(self,request):
        signup_data = {}
        responsedata = {}

        try:

            print("trying to register", request.POST)

            for key in request.POST:
                signup_data[key] = request.POST[key].strip()
            print("update user data : ", signup_data)

            try:
                if ((not signup_data['id']) or (not signup_data['user_session_key'])  or (not signup_data['name']) or (not signup_data['pincode']) or (not signup_data['country']) or (not signup_data['district']) or (not signup_data['city']) or (not signup_data['street']) or (not signup_data['building']) ):
                    # print("not all data",responsedata)

                    print(signup_data)

                    responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                    print(responsedata)

                    return Response(responsedata)
            except:

                # print("not all data except ","   ", responsedata)

                print(signup_data)

                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            try:
                us = UserSession.objects.get(UserSession_key=signup_data['user_session_key'])


                ud = UserDetail.objects.get(id=signup_data['id'])
                if (ud):

                    ud.full_name = signup_data['name']

                    if signup_data.get('email', None) is not None:
                        ud.email = signup_data["email"]
                    if signup_data.get('user_image', None) is not None:
                        ud.user_image = signup_data["user_image"]
                    #ud.mobile = signup_data['mobile']
                    ud.pincode = signup_data["pincode"]
                    ud.country = signup_data["country"]
                    ud.city = signup_data["city"]
                    ud.district = signup_data["district"]
                    ud.street = signup_data["street"]
                    ud.building = signup_data["building"]
                    #ud.user_type = signup_data['user_type']

                    #ud.set_password(signup_data['password'])


                    print("trying to save data")

                    ud.save()
                    sud=UserDetailSerializer(ud)
                    print("user details : ", ud)
                    responsedata = {"successstatus": "ok","message": "Profile Updated Successfully","userdetail":sud.data}
                    print(responsedata)
                    return Response(responsedata)

            except UserSession.DoesNotExist:
                responsedata = {"successstatus": "error", "message": "Please Login First."}
                print(responsedata)
                return Response(responsedata)
            except UserDetail.DoesNotExist:

                responsedata={"successstatus":"error","message":"User Does Not Exists."}
                print(responsedata)
                return Response(responsedata)





        except:

            print("in outer except")
            responsedata = {"successstatus": "error", "message": "unknown error. Please try again"}
            return Response(responsedata)


# generate and send verification link
def sendverificationlink_fun(userid):

    userid = int(userid)
    responsedata={}

    try:
        ud = UserDetail.objects.get(id=userid)
        if (ud):
            if ud.validemail:
                responsedata={"successstatus":"error","message":"your email is already verified"}
                return Response(responsedata)

            try:
                # uvs=UserVerificationSession()
                uvs = UserVerificationSession.objects.get(UserDetail_id=ud.id, verificationtype=0)
                if (uvs):
                    uvs.delete()

                else:

                    try:
                        uvs.delete()
                        pass
                    except:
                        pass
            except :

                try:
                    uvs.delete()

                except:
                    pass

            uvs = UserVerificationSession()
            uvs.full_name = ud.full_name
            uvs.email = ud.email
            uvs.User_Type=ud.user_type
            uvs.UserDetail_ref = ud
            uvs.UserDetail_id = ud.id
            k, d = generate_hash()
            uvs.UserSession_key = d
            uvs.verificationtype = 0
            uvs.save()
            verificationlink = settings.BASE_WEB_ADDRESS + "verifyuser/" + str(uvs.UserDetail_id) + "/" + str(
                uvs.UserSession_key)
            subject = "ONELINK : VERIFICATION OF YOUR ACCOUNT "
            body = "THIS IS AN AUTOGENERATED EMAIL. PLEASE DO NOT REPLY ON THIS MAIL. \nVERIFICATION LINK: " + verificationlink + "\nPLEASE VISIT THIS LINK TO VERIFY YOUR CUTLERY ACCOUNT"
            success_status = send_gmail(subject, body, ud.email)
            print("success_status = ", success_status)
            return success_status
        else:

            return -1
    except UserDetail.DoesNotExist:
        return -1


#resend the verification link to the user
class ResendVerificationLink(APIView):

    def post(self,request):
        responsedata={}
        if ((request.session.has_key('user_session_key')) or (request.POST['user_session_key'])):
            if( request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey=request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if us:
                    ud = UserDetail.objects.get(id=us.UserDetail_ref.id)  # also can b done like##### ud = us.UserDetail_ref
                    if (ud):
                        if not ud.validemail:
                            s=sendverificationlink_fun( ud.id)
                            if(s==0):
                                responsedata={"successstatus":"ok","message":"successfully sent the verification link.please check your email"}
                                return Response(responsedata)
                            else:

                                responsedata = {"successstatus": "error","message": "error occured.could not send the email."}
                                return Response(responsedata)
                        else:

                            responsedata = {"successstatus": "error", "message": "your email is already verified"}
                            return Response(responsedata)

                    else:
                        responsedata={"successstatus":"error","message":"your email id is not registered. please signup"}
                        return Response(responsedata)

                else:

                    try:

                        del request.session['username']
                    except:
                        pass

                    try:
                        us.delete()
                    except:
                        pass
                    responsedata = {"successstatus": "error", "message": "please login to continue"}
                    return Response(responsedata)


            except UserSession.DoesNotExist:

                try:

                    del request.session['username']
                except:
                    pass
                try:
                    us.delete()
                except:
                    pass

                responsedata = {"successstatus": "error", "message": "please login to continue"}
                return Response(responsedata)



            except UserDetail.DoesNotExist:
                try:

                    del request.session['username']
                except:
                    pass
                try:
                    us.delete()
                except:
                    pass

                responsedata = {"successstatus": "error", "message": "your email id is not registered. please signup"}
                return Response(responsedata)


        else:
            try:

                del request.session['username']
            except:
                pass


            try:
                us.delete()
            except:
                pass

            responsedata = {"successstatus": "error", "message": "please login to continue"}
            return Response(responsedata)


#verify the user
def verifyuser(request,userid,vkey):

    responsedata={}

    try:
        ud=UserDetail.objects.get(id=int(userid))
        if (ud):

            if(ud.validemail):
                return HttpResponse("<h1> Your email is already verified . please login through kadunaapp<h1>")

            uvs=UserVerificationSession.objects.get(UserSession_key=vkey)


            if(uvs):
                try:
                    ud.validemail=True
                    ud.save()
                    uvs.delete()
                    return HttpResponse("<h1> Your email is successfully verified . please login through kadunaapp to continue<h1>")
                except:
                    try:
                        uvs.delete()
                    except:
                        pass

                    return HttpResponse("<h1> this link is no more valid. please use the resend verification feature <h1>")




    except UserDetail.DoesNotExist:

        return HttpResponse("<h1> you are not registered with kaduna app <h1>")

    except UserVerificationSession.DoesNotExist:

        return HttpResponse("<h1> this link is no more valid. please use the resend verification feature <h1>")


    except:

        return HttpResponse("<h1> this link is no more valid. please use the resend verification feature <h1>")





class Login(APIView):

    def post(self,request):

        login_data = {}

        #print("trying login")




        try:

            if( request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey=request.POST['user_session_key']


            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):
                    print("sessionfound")
                    try:
                        del request.session['user_session_key']
                    except:
                        pass
                    try:
                        us.delete()
                    except:
                        pass
            except UserSession.DoesNotExist:
                try:
                    del request.session['user_session_key']
                except:
                    pass
                pass
        except:
            print("no session found")


            try:
                del(request.session['user_session_key'])
            except:
                pass

            try:
                us.delete()
            except:
                pass




        for key in request.POST:
            login_data[key] = request.POST[key].strip()

        print("login post : ",request.POST)
        print("login data :",login_data)

        try:
            if((not login_data['mobile']) or (not login_data['password'])):


                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print("if not data",responsedata)
                return Response(responsedata)

        except:

            responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
            print("except not data", responsedata)
            return Response(responsedata)

        try:

            ud = UserDetail.objects.get(mobile=login_data['mobile'])
            # bodytext+="<p>user data available</p>"

            correctpassword = ud.check_password(login_data['password'])
            # bodytext+="<p>"+str(correctpassword)+"</p>"

            if (correctpassword):

                try:
                    print("correct password")
                    us = UserSession.objects.get(mobile=ud.mobile)
                    uskey = us.UserSession_key
                    request.session['user_session_key'] = uskey
                    print("session available reinitialising the session")

                    #responsedata={"userid":ud.id,"user_type":ud.user_type,"areapincode":ud.pincode,'user_session_key':us.UserSession_key}
                    sud=UserDetailSerializer(ud)
                    responsedata = {"userdetail": sud.data,'user_session_key': us.UserSession_key}
                    print("after correct ",responsedata)

                    return Response(responsedata)

                except:
                    try:
                        print("No sessinon Available..creating new session..")
                        us.delete()
                    except:
                        pass

                us = UserSession()
                us.full_name = ud.full_name
                if ud.email:
                    us.email = ud.email
                us.User_Type=ud.user_type
                us.mobile=ud.mobile
                us.set_sessionkey()
                uskey = us.UserSession_key  # session key for the user
                us.UserDetail_id = ud.id
                us.UserDetail_ref = ud
                us.save()
                request.session['user_session_key'] = uskey
                sud=UserDetailSerializer(ud)

                responsedata = {"userdetail": sud.data, 'user_session_key': us.UserSession_key}
                print("New Login : ",responsedata)
                return Response(responsedata)
            else:
                responsedata={"successsatus":"error","message":"Mobile and password does not match"}
                return Response(responsedata)

        except UserDetail.DoesNotExist:

            try:

                del request.session['username']
            except:
                pass
            try:
                us.delete()
            except:
                pass

            responsedata = {"successstatus": "error", "message": "your Mobile Number is not registered. please signup"}
            return Response(responsedata)

        except :

                try:

                    del request.session['username']
                except:
                    pass
                try:
                    us.delete()
                except:
                    pass

                responsedata = {"successstatus": "error", "message": "Unknown error occured. Please try again"}

                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(True, exc_type, fname, exc_tb.tb_lineno)
                return Response(responsedata)





class Logout(APIView):

    def post(self,request):

        logout_data={}
        responsedata={}

        try:

            if( request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey=request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):
                    try:
                        del request.session['username']
                    except:
                        pass
                    try:
                        us.delete()
                        responsedata={"successstatus":"ok","message":"you have successfully Logged out"}
                        return  Response(responsedata)
                    except:
                        responsedata = {"successstatus": "error", "message": "Could not process your request"}
                        return Response(responsedata)

            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except:
            responsedata = {"successstatus": "error", "message": "You are not logged in"}
            return Response(responsedata)







class GetServiceCategory(APIView):

    def get(self,request):
        responsedata={}
        servicecategorydata=[]

        try:

            sc=ServiceCategory.objects.all()

            if(sc):




                for i in range(0,len(sc)):



                    tmpdata={"id":sc[i].id,"service_name":sc[i].service_name,"service_detail":sc[i].service_detail,"service_image":settings.BASE_IP+sc[i].service_image.url}
                    #print(tmpdata)
                    servicecategorydata.append(tmpdata)

                #print(servicecategorydata)
                #ssc=ServiceCategorySerializer(sc,many=True)
                #print(ssc.data)
                return Response(servicecategorydata)
            else:
                raise ( Exception(ServiceCategory.DoesNotExist))
        except:
            print("GetServiceCategory ERROR")
            responsedata={"successstatus":"Error","message":"No Service Category found"}
            return Response(responsedata)


class GetProductCategory(APIView):

    def get(self,request):
        responsedata={}
        productcategorydata=[]

        try:

            pc=ProductCategory.objects.all()

            if(pc):




                for i in range(0,len(pc)):



                    tmpdata={"id":pc[i].id,"product_name":pc[i].product_name,"product_detail":pc[i].product_detail,"product_image":settings.BASE_IP+pc[i].product_image.url}
                    #print(tmpdata)
                    productcategorydata.append(tmpdata)

                #print(servicecategorydata)
                #ssc=ServiceCategorySerializer(sc,many=True)
                #print(ssc.data)
                return Response(productcategorydata)
            else:
                raise ( Exception(ProductCategory.DoesNotExist))
        except:
            print("GetServiceCategory ERROR")
            responsedata={"successstatus":"Error","message":"No Product Category found"}
            return Response(responsedata)





class GetServiceSubCategory(APIView):

    def get(self,request,serviceid):
        responsedata={}


        try:

            sbsc=ServiceSubCategory.objects.filter(service_categorgy_id=int(serviceid))

            if(sbsc):

                #print(servicecategorydata)
                serializedsbsc=ServiceSubCategorySerializer(sbsc,many=True)
                #print(ssc.data)
                return Response(serializedsbsc.data)
            else:
                raise ( Exception(ServiceCategory.DoesNotExist))
        except:
            responsedata={"successstatus":"Error","message":"No Service Sub Category found"}
            return Response(responsedata)




#########################################################################################################################
#################################### Service provider section ###########################################################




######################################################################################################
#################################### Service Section #################################################


class RegisterService(APIView):

    def post(self,request):

        responsedata = {}
        registerservice_data={}
        print("trying to register service ")

        try:

            for key in request.POST:

                registerservice_data[key] = request.POST[key].strip()

            print("register service data : ", registerservice_data)

            print(registerservice_data['service_category_id'])
            print(registerservice_data['serviceprovider_id'])
            print(registerservice_data['service_name'])
            print(registerservice_data['areapincode'])

            print(registerservice_data['service_details'])


            if((not registerservice_data['service_category_id']) or (not registerservice_data['license_no']) or (not registerservice_data['under_gov']) or (not registerservice_data['serviceprovider_id']) or (not registerservice_data['service_name']) or (not registerservice_data['service_details']) or (not registerservice_data['areapincode'])):
                responsedata={"successstatus":"error","message":"please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)



            print("Register service data : ",registerservice_data)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']
                print("sess key ",sesskey)

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us.User_Type==0):
                    print("correct user")

                    try:

                        ud=UserDetail.objects.get(id=us.UserDetail_id)
                        if(ud):

                            if(not ud.user_type==0):
                                responsedata = {"successstatus": "error","message": "you are not registered as a service provider"}
                                print(responsedata)
                                return Response(responsedata)



                            try:
                                sc = ServiceCategory.objects.get(id=int(registerservice_data['service_category_id']))

                                sm = ServiceMap()
                                sm.serviceprovider_id=registerservice_data['serviceprovider_id']
                                sm.service_name=registerservice_data['service_name']
                                sm.service_details=registerservice_data['service_details']
                                sm.license_no=registerservice_data['license_no']
                                sm.under_gov=registerservice_data['under_gov']
                                print("service_details : ",sm.service_details)
                                sm.serviceprovider_email=ud.email
                                sm.mobile=ud.mobile
                                sm.service_category_id=registerservice_data['service_category_id']
                                sm.service_ref = sc
                                sm.areapincode=registerservice_data['areapincode']
                                if(registerservice_data.get("servicemap_image",None) is not None):
                                    sm.servicemap_image=registerservice_data["servicemap_image"]
                                sm.service_type="SERVICE"

                                sm.save()

                                responsedata={"successstatus":"ok","message":"You have successfully registered your service"}
                                return  Response(responsedata)

                            except ServiceMap.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "No Services Available"}
                                print(responsedata)
                                return  Response(responsedata)

                            except ServiceCategory.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "Service category not available"}
                                print(responsedata)
                                return  Response(responsedata)


                        else:
                            responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                            print(responsedata)
                            return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)
                    except Exception as e:

                        responsedata = {"successstatus": "error", "message": "Unknown Error"}


                        print("inner except : unknown error register service: ", responsedata)
                        print("Exception : ",e)
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(True, exc_type, fname, exc_tb.tb_lineno)
                        return Response(responsedata)


                else:
                    responsedata = {"successstatus": "error", "message": "you are not registered as a service provider"}
                    print(responsedata)
                    return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except Exception as e:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("register service in outer except : ",responsedata)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)





class UpdateService(APIView):

    def post(self,request):

        responsedata = {}
        updateservice_data={}

        try:

            for key in request.POST:
                updateservice_data[key] = request.POST[key].strip()

            print("updateservice_data : ",updateservice_data)

            #print(updateservice_data['service_category_id'])
            #print(updateservice_data['serviceprovider_id'])
            #print(updateservice_data['service_name'])
            #print(updateservice_data['areapincode'])
            #print(updateservice_data['servicemapid'])
            #print(updateservice_data['service_details'])



            if((not updateservice_data['servicemapid'])  or (not updateservice_data['license_no']) or (not updateservice_data['under_gov']) or (not updateservice_data['serviceprovider_id']) or (not updateservice_data['service_name']) or (not updateservice_data['service_details']) or (not updateservice_data['areapincode']) ):
                responsedata={"successstatus":"error","message":"please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)





            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']
                print("sess key ",sesskey)

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us.User_Type==0):
                    print("correct user")

                    try:

                        print("user session : ",us)
                        print("service provider id : ",updateservice_data['serviceprovider_id'])
                        ud=UserDetail.objects.get(id=us.UserDetail_id)
                        if(ud):

                            if(not ud.user_type==0):
                                responsedata = {"successstatus": "error","message": "you are not registered as a service provider"}
                                print(responsedata)
                                return Response(responsedata)



                            try:
                                #sc = ServiceCategory.objects.get(id=int(updateservice_data['service_category_id']))

                                sm = ServiceMap.objects.get(id=int(updateservice_data['servicemapid']))
                                sm.serviceprovider_id = updateservice_data['serviceprovider_id']
                                sm.service_name = updateservice_data['service_name']
                                sm.service_details = updateservice_data['service_details']
                                sm.license_no = updateservice_data['license_no']
                                sm.under_gov = updateservice_data['under_gov']
                                #print("service_details : ", sm.service_details)
                                sm.serviceprovider_email = ud.email
                                sm.mobile = ud.mobile

                                sm.areapincode = updateservice_data['areapincode']

                                if (updateservice_data.get("servicemap_image", None) is not None):
                                    sm.servicemap_image = updateservice_data["servicemap_image"]

                                sm.save()

                                responsedata={"successstatus":"ok","message":"You have successfully registered your service"}
                                return  Response(responsedata)

                            except ServiceMap.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "No Services Available"}
                                print(responsedata)
                                return  Response(responsedata)

                            except ServiceCategory.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "Service category not available"}
                                print(responsedata)
                                return  Response(responsedata)


                        else:
                            responsedata = {"sauccesssttus": "error", "message": "User Does Not Exist"}
                            print(responsedata)
                            return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)
                    except Exception as e:

                        responsedata = {"successstatus": "error", "message": "Unknown Error"}


                        print("userdetail try except  : ", responsedata)
                        print("Exception : ",e)
                        return Response(responsedata)


                else:
                    responsedata = {"successstatus": "error", "message": "you are not registered as a service provider"}
                    print(responsedata)
                    return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except Exception as e:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in update service outer except : ",responsedata)
            print("Error : ",e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)





class DeleteService(APIView):

    def post(self,request):

        responsedata = {}
        deleteservice_data={}

        try:

            for key in request.POST:
                deleteservice_data[key] = request.POST[key].strip()

            if((not deleteservice_data['service_id']) or (not deleteservice_data['user_session_key'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get services data : ",deleteservice_data)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud=UserDetail.objects.get(id=us.UserDetail_id)
                        if(ud):
                            try:
                                sm = ServiceMap.objects.get(id=int(deleteservice_data['service_id']),serviceprovider_id=ud.id)

                                if (sm):
                                    try:
                                        sm.delete()
                                        responsedata = {"successstatus": "ok","message": "successfully deleted the service"}
                                        print(responsedata)
                                        return Response(responsedata)
                                    except:
                                        responsedata={"successstatus":"error","message":"could not delete service try again later"}
                                        return Response(responsedata)


                                else:
                                    responsedata = {"successstatus": "error", "message": "No Services Available"}
                                    print(responsedata)
                                    return Response(responsedata)



                            except ServiceMap.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "No Services Available"}
                                print(responsedata)
                                return  Response(responsedata)


                        else:
                            responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                            print(responsedata)
                            return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except Exception as e:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in DeleteService : outer except : ",responsedata)
            print("Error : ",e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)







class GetMyServices(APIView):

    def post(self,request):

        responsedata = {}
        getservice_data={}

        try:

            for key in request.POST:
                getservice_data[key] = request.POST[key].strip()

            if((not getservice_data['id']) or (not getservice_data['user_session_key'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get services data : ",getservice_data)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud=UserDetail.objects.get(id=us.UserDetail_id)
                        if(ud):
                            try:
                                sm = ServiceMap.objects.filter(serviceprovider_id=int(getservice_data['id']))#.order_by("-id")

                                if (sm):
                                    ssm = ServiceMapSerializer(sm, many=True)

                                    #print("sm : ",sm)
                                    print(ssm.data)
                                    return Response(ssm.data)

                                else:
                                    responsedata = {"successstatus": "error", "message": "No Services Available"}
                                    print(responsedata)
                                    return Response(responsedata)



                            except ServiceMap.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "No Services Available"}
                                print(responsedata)
                                return  Response(responsedata)


                        else:
                            responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                            print(responsedata)
                            return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in outer except : ",responsedata)
            return Response(responsedata)



class GetMySingleService(APIView):

    def post(self, request):

        responsedata = {}
        getservice_data = {}

        try:

            for key in request.POST:
                getservice_data[key] = request.POST[key].strip()

            if ((not getservice_data['id']) or (not getservice_data['user_session_key']) or (not getservice_data["service_id"])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get services data : ", getservice_data)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud):
                            try:
                                sm = ServiceMap.objects.get(id=int(getservice_data["service_id"]))

                                if (sm):
                                    ssm = ServiceMapSerializer(sm)
                                    print(ssm.data)
                                    return Response(ssm.data)

                                else:
                                    responsedata = {"successstatus": "error","message": "No Services Available"}
                                    print(responsedata)
                                    return Response(responsedata)



                            except ServiceMap.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "No Services Available"}
                                print(responsedata)
                                return Response(responsedata)


                        else:
                            responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                            print(responsedata)
                            return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in getMySingleService outer except : ", responsedata)
            return Response(responsedata)





class GetMyRequests(APIView):

    def post(self, request):

        responsedata = {}
        getservice_data = {}
        xssr=[]

        try:

            for key in request.POST:
                getservice_data[key] = request.POST[key].strip()

            if ((not getservice_data['id']) or (not getservice_data['user_session_key'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get services data : ", getservice_data)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud):
                            try:
                                if(ud.user_type==0):
                                    sr = ServiceRequest.objects.filter(serviceprovider_id=ud.id).order_by("-request_time")
                                else:
                                    sr = ServiceRequest.objects.filter(user_id=ud.id).order_by("-request_time")

                                if (sr):
                                    ssr = ServiceRequestSerializer(sr, many=True)

                                    # print("sm : ",sm)
                                    #print(ssr.data)
                                    xssr=ssr.data
                                    for s in range(0,len(xssr)):
                                        tmsg=0
                                        try:
                                            rm=RequestMessage.objects.filter(request_id=xssr[s]["id"],receiver_id=ud.id,request_type="SERVICE").order_by("sending_time")
                                            for r in rm:
                                                try:
                                                    if not r.read:
                                                        tmsg+=1
                                                        #print("message count ......................................................................................................................",tmsg)
                                                except:
                                                    print("error.......")
                                                    #input()
                                                    continue
                                            xssr[s]["unread_message"]=tmsg
                                        except Exception as e:
                                            #print("===============================================================================error        ")
                                            xssr[s]["unread_message"]=tmsg
                                            #input()
                                    print(xssr)

                                    responsedata = {"successstatus": "ok", "requests": xssr}
                                    return Response(responsedata)

                                else:
                                    responsedata = {"successstatus": "error","message": "No request Available"}
                                    print(responsedata)
                                    return Response(responsedata)

                                    

                            except ServiceRequest.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "No request Available"}
                                print(responsedata)
                                return Response(responsedata)


                        else:
                            responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                            print(responsedata)
                            return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in outer except : ", responsedata)
            return Response(responsedata)




class GetMyQuickRequests(APIView):

    def post(self, request):

        responsedata = {}
        getservice_data = {}

        try:

            for key in request.POST:
                getservice_data[key] = request.POST[key].strip()

            if ((not getservice_data['id']) or (not getservice_data['user_session_key'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get services data : ", getservice_data)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud):
                            try:
                                if(ud.user_type==0):
                                    sr = ServiceRequest.objects.filter(serviceprovider_id=ud.id,service_type="QUICK SERVICE").order_by("-request_time")
                                else:
                                    sr = ServiceRequest.objects.filter(user_id=ud.id,service_type="QUICK SERVICE").order_by("-request_time")

                                if (sr):
                                    ssr = ServiceRequestSerializer(sr, many=True)

                                    # print("sm : ",sm)
                                    print(ssr.data)
                                    responsedata = {"successstatus": "ok", "requests": ssr.data}
                                    return Response(responsedata)

                                else:
                                    responsedata = {"successstatus": "error","message": "No request Available"}
                                    print(responsedata)
                                    return Response(responsedata)



                            except ServiceMap.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "No request Available"}
                                print(responsedata)
                                return Response(responsedata)


                        else:
                            responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                            print(responsedata)
                            return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in outer except : ", responsedata)
            return Response(responsedata)







class GetMySingleRequest(APIView):

    def post(self, request):

        responsedata = {}
        getservice_data = {}

        try:

            for key in request.POST:
                getservice_data[key] = request.POST[key].strip()

            print("get my single request : ", getservice_data)

            if ((not getservice_data['id']) or (not getservice_data['user_session_key']) or (not getservice_data['request_id'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get services data : ", getservice_data)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud):
                            try:
                                print("ud id : ", ud.id)
                                print("request id : ", getservice_data['request_id'])
                                if (ud.user_type == 0):
                                    sr = ServiceRequest.objects.get(serviceprovider_id=ud.id,id=int(getservice_data['request_id']))#.order_by("-request_time")
                                else:
                                    sr = ServiceRequest.objects.get(user_id=ud.id,id=int(getservice_data['request_id']))#.order_by("-request_time")

                                # if (getservice_data.get("notification_id", None) is not None):
                                #     try:
                                #         sn = ServiceNotification.objects.get(id=int(getservice_data["notification_id"]))
                                #         sn.read = True
                                #         sn.save()
                                #     except:
                                #         pass

                                if (sr):
                                    if(not sr.read and ud.user_type==0):
                                        sr.read=True
                                        sr.save()
                                    ssr = ServiceRequestSerializer(sr)
                                    tdata=ssr.data
                                    # try:
                                    #     rud = UserDetail.objects.get(id=sr.user_id)
                                    # except Exception as e:
                                    #     responsedata={"successstatus":"error","messgae":"could not get requester's details"}
                                    #     print("response data : ",responsedata)
                                    #     print("Error occured : ",e)
                                    #     return Response(responsedata)
                                    tdata["user_name"]=sr.user_ref.full_name
                                    tdata["mobile"]=sr.user_ref.mobile
                                    tdata["service_name"]=sr.service_map_ref.service_name

                                    try:
                                        rm=RequestMessage.objects.filter(request_id=sr.id,request_type=sr.request_type).order_by("sending_time")
                                        for r in rm:
                                            try:
                                                if not r.read:
                                                    r.read=True
                                                    r.save()
                                            except:
                                                #print("error.......")
                                                pass
                                    except Exception as e:
                                        pass
                                        #print("Error in reqading service message : ",e)

                                    #srm=RequestMessageSerializer(rm,many=True)

                                    # print("sm : ",sm)
                                    print("final data : ",tdata)

                                    responsedata = {"successstatus": "ok", "request_detail": tdata}

                                    return Response(responsedata)

                                else:
                                    responsedata = {"successstatus": "error", "message": "No request Available"}
                                    print(responsedata)
                                    return Response(responsedata)



                            except ServiceMap.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "No request Available"}
                                print(responsedata)
                                return Response(responsedata)


                        else:
                            responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                            print(responsedata)
                            return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except Exception as e:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in outer except : ", responsedata)
            print("Error : ", e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)






############################################################################################################################
###########################################  Item Section ##################################################################

from .models import ProductCategory
from .serializers import ProductCategorySerializer

class AddItem(APIView):

    def post(self,request):

        responsedata = {}
        additem_data={}

        try:

            for key in request.POST:
                additem_data[key] = request.POST[key].strip()

            print("add item data : ",additem_data)


            if((not additem_data['serviceprovider_id']) or (not additem_data['user_session_key'])  or (not additem_data['item_name']) or (not additem_data['item_details']) or (not additem_data['item_category_id'])      or (not additem_data['item_MRP'])  or (not additem_data['item_SLP'])  or (not additem_data['item_features']) ):
                responsedata={"successstatus":"error","message":"please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            if request.FILES.get("item_image",None) is not None:
                additem_data['item_image']=request.FILES['item_image']
            else:
                additem_data["item_image"]=None
            print("Register service data : ",additem_data)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']
                print("sess key ",sesskey)

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us.User_Type==0):
                    print("correct user")

                    try:

                        ud=UserDetail.objects.get(id=us.UserDetail_id)
                        if(ud):

                            if(not ud.user_type==0):
                                responsedata = {"successstatus": "error","message": "you are not registered as a service provider"}
                                print(responsedata)
                                return Response(responsedata)



                            try:
                                sc = ProductCategory.objects.get(id=int(additem_data['item_category_id']))

                                im = ItemMap()
                                im.serviceprovider_id=additem_data['serviceprovider_id']
                                im.item_name=additem_data['item_name']
                                im.item_details=additem_data['item_details']
                                im.serviceprovider_email=ud.email
                                im.product_category_id=int(additem_data['item_category_id'])
                                im.product_ref=sc
                                if  additem_data.get('item_image',None) is not None:
                                    im.item_image=additem_data['item_image']
                                #im.areapincode=additem_data['areapincode']
                                im.item_features=additem_data['item_features']
                                im.item_MRP=additem_data['item_MRP']
                                im.item_SLP=additem_data['item_SLP']
                                im.mobile=ud.mobile

                                if(additem_data.get("itemmap_image1",None) is not None):
                                    im.itemmap_image1=additem_data["itemmap_image1"]
                                if (additem_data.get("itemmap_image2", None) is not None):
                                    im.itemmap_image2 = additem_data["itemmap_image2"]
                                if (additem_data.get("itemmap_image3", None) is not None):
                                    im.itemmap_image3 = additem_data["itemmap_image3"]
                                if (additem_data.get("itemmap_image4", None) is not None):
                                    im.itemmap_image4 = additem_data["itemmap_image4"]
                                if (additem_data.get("itemmap_image5", None) is not None):
                                    im.itemmap_image5 = additem_data["itemmap_image5"]


                                im.save()

                                responsedata={"successstatus":"ok","message":"item successfully added"}
                                return  Response(responsedata)



                            except ProductCategory.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "Product category not available"}
                                print(responsedata)
                                return  Response(responsedata)


                        else:
                            responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                            print(responsedata)
                            return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)
                    except Exception as e:

                        responsedata = {"successstatus": "error", "message": "Unknown Error"}


                        print("userdetail try except  : ", responsedata)
                        print("Exception : ",e)
                        return Response(responsedata)


                else:
                    responsedata = {"successstatus": "error", "message": "you are not registered as a service provider"}
                    print(responsedata)
                    return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except Exception as e:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in outer except : AddItem : ",responsedata)
            print("Error : ",e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)



class UpdateItem(APIView):

    def post(self, request):

        responsedata = {}
        updateitem_data = {}

        try:

            for key in request.POST:
                updateitem_data[key] = request.POST[key].strip()

            if ((not updateitem_data['itemmap_id'])or (not updateitem_data['user_session_key'])  or (not updateitem_data['serviceprovider_id']) or (not updateitem_data['item_name'])  or (not updateitem_data['item_details'])   or (not updateitem_data['item_MRP']) or (not updateitem_data['item_SLP']) or (not updateitem_data['item_features'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)


            print("Register service data : ", updateitem_data)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']
                print("sess key ", sesskey)


            if updateitem_data.get("item_image",None) is None:
                updateitem_data["item_image"] = None


            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us.User_Type == 0):
                    print("correct user")

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud):

                            if (not ud.user_type == 0):
                                responsedata = {"successstatus": "error","message": "you are not registered as a service provider"}
                                print(responsedata)
                                return Response(responsedata)

                            try:
                                #sc = ServiceCategory.objects.get(id=int(updateitem_data['service_category_id']))

                                im = ItemMap.objects.get(id=int(updateitem_data['itemmap_id']))
                                im.serviceprovider_id = updateitem_data['serviceprovider_id']
                                #im.service_category_id = int(updateitem_data['service_category_id'])
                                #im.service_ref = sc
                                im.service_name = updateitem_data['item_name']
                                im.service_details = updateitem_data['item_details']
                                im.serviceprovider_email = ud.email
                                if(updateitem_data["item_image"]):
                                    im.item_image = updateitem_data['item_image']
                                #im.areapincode = updateitem_data['areapincode']
                                im.item_features = updateitem_data['item_features']
                                im.item_MRP = updateitem_data['item_MRP']
                                im.item_SLP = updateitem_data['item_SLP']

                                if (updateitem_data.get("itemmap_image1", None) is not None):
                                    im.itemmap_image1 = updateitem_data["itemmap_image1"]
                                if (updateitem_data.get("itemmap_image2", None) is not None):
                                    im.itemmap_image2 = updateitem_data["itemmap_image2"]
                                if (updateitem_data.get("itemmap_image3", None) is not None):
                                    im.itemmap_image3 = updateitem_data["itemmap_image3"]
                                if (updateitem_data.get("itemmap_image4", None) is not None):
                                    im.itemmap_image4 = updateitem_data["itemmap_image4"]
                                if (updateitem_data.get("itemmap_image5", None) is not None):
                                    im.itemmap_image5 = updateitem_data["itemmap_image5"]

                                im.save()

                                responsedata = {"successstatus": "ok","message": "successfully Updated Your Item"}
                                return Response(responsedata)

                            except ItemMap.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "No Item Available"}
                                print(responsedata)
                                return Response(responsedata)

                            # except ServiceCategory.DoesNotExist:
                            #     responsedata = {"successstatus": "error","message": "Service category not available"}
                            #     print(responsedata)
                            #     return Response(responsedata)


                        else:
                            responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                            print(responsedata)
                            return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)
                    except Exception as e:

                        responsedata = {"successstatus": "error", "message": "Unknown Error"}

                        print("userdetail try except  : ", responsedata)
                        print("Exception : ", e)
                        return Response(responsedata)


                else:
                    responsedata = {"successstatus": "error",
                                    "message": "you are not registered as a service provider"}
                    print(responsedata)
                    return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except Exception as e:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in outer except : ", responsedata)
            print("Error : ",e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)

class DeleteItem(APIView):

    def post(self, request):

        responsedata = {}
        deleteitem_data = {}

        try:

            for key in request.POST:
                deleteitem_data[key] = request.POST[key].strip()

            if ((not deleteitem_data['item_id']) or (not deleteitem_data['user_session_key'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get services data : ", deleteitem_data)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud):
                            try:
                                im = ItemMap.objects.get(id=int(deleteitem_data['item_id']),serviceprovider_id=ud.id)

                                if (im):
                                    try:
                                        im.delete()
                                        responsedata = {"successstatus": "ok","message": "successfully deleted the item"}
                                        print(responsedata)
                                        return Response(responsedata)
                                    except:
                                        responsedata = {"successstatus": "error","message": "could not delete Item try again later"}
                                        return Response(responsedata)


                                else:
                                    responsedata = {"successstatus": "error","message": "No Item Available"}
                                    print(responsedata)
                                    return Response(responsedata)



                            except ItemMap.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "No Item Available"}
                                print(responsedata)
                                return Response(responsedata)


                        else:
                            responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                            print(responsedata)
                            return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except Exception as e:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in DeleteItem : outer except : ", responsedata)
            print("Error : ", e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)

class GetMyItems(APIView):

    def post(self, request):

        responsedata = {}
        getitem_data = {}

        try:

            for key in request.POST:
                getitem_data[key] = request.POST[key].strip()

            if ((not getitem_data['id']) or (not getitem_data['user_session_key'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get items data : ", getitem_data)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud):
                            try:
                                # print("service provider's id is : ",ud.id)
                                im = ItemMap.objects.filter(serviceprovider_id=ud.id)

                                # print("items : ",im)

                                if (im):
                                    sim = ItemMapSerializer(im, many=True)
                                    print("Items : ",sim.data)
                                    return Response(sim.data)

                                else:
                                    responsedata = {"successstatus": "error","message": "No Item Available"}
                                    print(responsedata)
                                    return Response(responsedata)



                            except ItemMap.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "No Item Available"}
                                print(responsedata)
                                return Response(responsedata)


                        else:
                            responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                            print(responsedata)
                            return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in getmyitems : outer except : ", responsedata)
            return Response(responsedata)




from .serializers import ProviderNotificationSerializer
from .models import ServiceNotification
from .serializers import ItemNotificationSerializer
from .models import ItemNotification

class GetMyNotifications(APIView):

    def post(self, request):

        responsedata = {}
        getnoti_data = {}
        notidata=[]
        tn={}
        snot=[]
        pnot=[]
        tot_servicenot=0
        tot_productnot=0
        tot_smessagecount=0
        tot_pmessagecount=0

        try:

            for key in request.POST:
                getnoti_data[key] = request.POST[key].strip()

            print(getnoti_data)

            if ((not getnoti_data['id']) or (not getnoti_data['user_session_key'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get items data : ", getnoti_data)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud):
                            try:
                                sud=UserDetailSerializer(ud)
                                #print("ud : ",ud.id).order_by("-request_time")
                                print("getting notifications ...")

                                try:
                                    if(ud.user_type==0):
                                        sr = ServiceRequest.objects.filter(serviceprovider_id=ud.id).order_by("-request_time")
                                    else:
                                        sr = ServiceRequest.objects.filter(user_id=ud.id).order_by("-request_time")

                                    if (sr):
                                        ssr = ServiceRequestSerializer(sr, many=True)

                                        snot=ssr.data
                                        for s in range(0,len(snot)):

                                            snot[s]["requester"]=sr[s].user_ref.full_name
                                            snot[s]["service"]=sr[s].service_map_ref.service_name
                                            if not snot[s]["read"]:

                                                tot_servicenot+=1

                                        # print("sm : ",sm)
                                        

                                    else:
                                        snot=None



                                except ServiceRequest.DoesNotExist:
                                    snot=None

                                
                                try:
                                    if(ud.user_type==0):
                                        ir = ItemRequest.objects.filter(serviceprovider_id=ud.id).order_by("-request_time")
                                    else:
                                        ir = ItemRequest.objects.filter(user_id=ud.id).order_by("-request_time")

                                    if (ir):
                                        sir = ItemRequestSerializer(ir, many=True)

                                        # print("sm : ",sm)
                                        pnot=sir.data
                                        for s in range(0,len(pnot)):

                                            pnot[s]["requester"]=ir[s].user_ref.full_name
                                            pnot[s]["service"]=ir[s].item_map_ref.item_name
                                            if not pnot[s]["read"]:
                                                tot_productnot+=1

                                    else:
                                        pnot=None



                                except ItemRequest.DoesNotExist:
                                    pnot=None

                                try:
                                    rm=RequestMessage.objects.filter(receiver_id=ud.id,request_type="SERVICE").order_by("sending_time")
                                    for r in rm:
                                        try:
                                            if(not r.read):
                                                tot_smessagecount+=1
                                        except:
                                            continue
                                    del(rm)
                                except:
                                    pass

                                try:
                                    rm=RequestMessage.objects.filter(receiver_id=ud.id,request_type="PRODUCT").order_by("sending_time")
                                    for r in rm:
                                        try:
                                            if(not r.read):
                                                tot_pmessagecount+=1
                                        except:
                                            continue
                                    del(rm)
                                except:
                                    pass

                                

                                responsedata = {"unread_servicerequestmessage": tot_smessagecount,"unread_servicerequest":tot_servicenot, "unread_productrequestmessage": tot_pmessagecount,"unread_productrequest":tot_productnot,"successstatus": "ok"}
                                print(responsedata)
                                return Response(responsedata)



                            except Exception as e:
                                responsedata={"successstatus":"error","message":"error occured while fetching notification"}
                                print("Error : ",e)
                                print(responsedata)
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                print(True, exc_type, fname, exc_tb.tb_lineno)
                                return Response(responsedata)



                        else:
                            responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                            print(responsedata)
                            return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except Exception as e:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in getmynotifications : outer except : ", responsedata)
            print("Error : ",e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)





from .models import OrderHistory
from .serializers import OrderHistorySerializer

class ConfirmRequest(APIView):
    def post(self,request):

        responsedata = {}
        requestdata={}
        try:

            for key in request.POST:
                requestdata[key] = request.POST[key].strip()

            print(requestdata)

            if ((not requestdata['id']) or (not requestdata['user_session_key']) or (not requestdata['request_id'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get items data : ", requestdata)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud and ud.user_type==0):
                            try:

                                sr=ServiceRequest.objects.get(id=int(requestdata["request_id"]),serviceprovider_id=ud.id)
                                try:
                                    oh = OrderHistory.objects.get(serviceprovider_id=ud.id, request_id=sr.id)
                                    if(oh or sr.service_status!=0):
                                        responsedata={"successstatus":"error","message":"request is already confirmed"}
                                        print(responsedata)
                                        return Response(responsedata)
                                except :
                                    pass
                                sr.service_status=1
                                sr.save()

                                cr=OrderHistory()

                                cr.user_id=sr.user_id
                                cr.user_ref=sr.user_ref
                                cr.serviceprovider_id=sr.serviceprovider_id
                                cr.serviceprovider_ref=sr.serviceprovider_ref
                                cr.service_map_id=sr.service_map_id
                                cr.service_map_ref=sr.service_map_ref
                                cr.service_request_id=sr.id
                                cr.service_request_ref=sr
                                cr.confirmation_id=GetConfirmationId(rtype="SER",rid=sr.id)
                                cr.service_type=sr.service_type

                                cr.save()

                                responsedata={"successstatus":"ok","confirmation_id":cr.confirmation_id}
                                print(responsedata)
                                return Response(responsedata)

                            except ServiceRequest.DoesNotExist:
                                responsedata={"successstatus":"error","messsage":'No request availabe for you with given details'}
                                print(responsedata)
                                return  Response(responsedata)

                    except Exception as e:
                        responsedata={"successstatus":"error","message":"Unknown error occured"}
                        print(responsedata)
                        print("Error occured : ",e)
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(True, exc_type, fname, exc_tb.tb_lineno)
                        return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except Exception as e:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in Confirm Order : outer except : ", responsedata)
            print("Error : ",e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)


class GetMyHistory(APIView):
    def post(self,request):
        responsedata = {}
        requestdata = {}
        try:

            for key in request.POST:
                requestdata[key] = request.POST[key].strip()

            print(requestdata)

            if ((not requestdata['id']) or (not requestdata['user_session_key'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get items data : ", requestdata)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud):
                            try:


                                if(ud.user_type==0):
                                    cr = OrderHistory.objects.filter(serviceprovider_id=ud.id).order_by("-booked_time")
                                else:
                                    cr = OrderHistory.objects.filter(user_id=ud.id).order_by("-booked_time")

                                scr=OrderHistorySerializer(cr,many=True)

                                responsedata = {"successstatus": "ok", "history":scr.data}
                                print(responsedata)
                                return Response(responsedata)

                            except OrderHistory.DoesNotExist:
                                responsedata = {"successstatus": "error","messsage": 'No history availabe for you with given details'}
                                print(responsedata)
                                return Response(responsedata)

                    except Exception as e:
                        responsedata = {"successstatus": "error", "message": "Unknown error occured"}
                        print(responsedata)
                        print("Error occured : ", e)
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(True, exc_type, fname, exc_tb.tb_lineno)
                        return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except Exception as e:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in get order history : outer except : ", responsedata)
            print("Error : ", e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)


##############################################################################################################################
####################################### Normal user section ##################################################################
from functools import reduce
class GetProvidersList(APIView):
    def get(self,request,serviceid,areapincodes):
        responsedata={}

        print("service id : ",serviceid)
        print("pincodes : ",areapincodes)

        if((not serviceid) or (not areapincodes)):
            print("not all data in getproviderslist")
            responsedata={"successstatus":"error","message":"please procvide all the details necessary"}
            print("in get providers list : ",responsedata)
            return  Response(responsedata)

        areapincodes=areapincodes.replace("%22",'"')
        #print(type(areapincodes))


        areapincodes=json.loads(areapincodes)
        #print(type(areapincodes))

        try:
            sm = ServiceMap.objects.filter(service_category_id=int(serviceid))#,areapincode=areapincodes[0])
            #sm=ServiceMap.objects.filter(reduce(lambda x, y: x | y, [Q(service_category_id=int(serviceid),areapincode=pincode) for pincode in areapincodes])).order_by("-areapincode")
            #print("sm : ",sm)
            if (sm):
                ssm = ServiceMapSerializer(sm, many=True)
                print(ssm.data)
                return Response(ssm.data)

            else:
                responsedata = {"successstatus": "error", "message": "No Services Available"}
                print(responsedata)
                return Response(responsedata)



        except ServiceMap.DoesNotExist:
            responsedata = {"successstatus": "error", "message": "No Services Available"}
            print(responsedata)
            return Response(responsedata)
        except Exception as e:
            print("unknown error occured")
            print("erro : ",e)
            responsedata = {"successstatus": "error", "message": "Unknown Error"}

            print("In GetProvidersList Outer Except : ",responsedata)
            return  Response(responsedata)



class GetSingleService(APIView):
    def get(self,request,serviceid):
        responsedata={}

        if((not serviceid)):
            print("not all data in getproviderslist")
            responsedata={"successstatus":"error","message":"please procvide all the details necessary"}
            print("in get providers list : ",responsedata)
            return  Response(responsedata)

        try:

            #print(ServiceMap._meta.pk.name)

            sm = ServiceMap.objects.get(id=int(serviceid))
            if (sm):
                print("id : ",sm.id)
                ssm = ServiceMapSerializer(sm)
                print(ssm.data)
                responsedata["service_details"] = ssm.data

            ud = UserDetail.objects.get(id=int(sm.serviceprovider_id))
            if (ud):

                sud=UserDetailSerializer(ud)
                print(sud.data)
                responsedata["provider_details"]=sud.data

            else:
                responsedata = {"successstatus": "error", "message": "No Services Available"}
                print(responsedata)
                return Response(responsedata)

            try:

                r = Review.objects.filter(map_id=sm.id, review_type="SERVICE".upper(), provider_id=ud.id).order_by("-review_time")
                if(r):
                    rs=ReviewSerializer(r,many=True)
                    print(rs.data)
                    responsedata["review_data"]=rs.data
            except Review.DoesNotExist:
                responsedata["review_data"] = None

            print("Final service data : ",responsedata)
            return Response(responsedata)


        except UserDetail.DoesNotExist:
            responsedata = {"successstatus": "error", "message": "No Provider Available"}
            print(responsedata)
            return Response(responsedata)

        except Exception as e:
            print("unknown error occured")
            print("erro : ",e)
            responsedata = {"successstatus": "error", "message": "Unknown Error"}

            print("In GetProvidersList Outer Except : ",responsedata)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return  Response(responsedata)


from .models import  ServiceRequest
from .serializers import ServiceRequestSerializer

from .models import ServiceNotification
from .serializers import ServiceRequestSerializer

class RequestService(APIView):

    def post(self,request):
        responsedata={}
        requestdata={}
        userstat=0
        service_request_address=None
        areapincode=None


        try:
            for key in request.POST:
                requestdata[key]=request.POST[key]

            print("obtained request service data : ",requestdata)

            if ((not requestdata["serviceprovider_id"]) or (not requestdata["user_id"]) or (not requestdata["service_map_id"]) or (not requestdata['user_session_key'])) :
                responsedata={"successstatus":"error","message":"please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)
            us=UserSession.objects.get(UserSession_key=requestdata['user_session_key'])

            ud=UserDetail.objects.get(id=int(requestdata["user_id"]))
            userstat+=1
            sd=UserDetail.objects.get(id=int(requestdata["serviceprovider_id"]))
            userstat+=1

            smap=ServiceMap.objects.get(id=int(requestdata["service_map_id"]))

            if(requestdata.get("service_request_address",None) is None):
                service_request_address=ud.address
            else:
                service_request_address=requestdata["service_request_address"]

            if(requestdata.get("areapincode",None) is None):
                areapincode=ud.pincode
            else:
                areapincode=requestdata["areapincode"]

            sm=ServiceMap.objects.get(id=int(requestdata["service_map_id"]))

            sr=ServiceRequest()
            sr.user_id=ud.id
            sr.user_ref=ud
            sr.serviceprovider_id=sd.id
            sr.serviceprovider_ref=sd
            sr.service_map_id=sm.id
            sr.service_map_ref=sm
            sr.service_category_id=sm.service_category_id
            sr.areapincode=areapincode
            sr.service_request_address=service_request_address
            sr.notification=sr.getMessage()
            if(requestdata.get("request_detail",None) is not None):
                sr.request_detail = requestdata["request_detail"]

            if(requestdata.get("request_image",None) is not None):
                sr.request_image=requestdata["request_image"]
            sr.service_type="SERVICE"

            sr.save()

            sn=ServiceNotification()
            sn.serviceprovider_id=sr.serviceprovider_id
            sn.serviceprovider_ref=sr.serviceprovider_ref
            sn.servicerequest_id=sr.id
            sn.servicerequest_ref=sr
            sn.read=False
            #sn.save()
            sn.notification = sn.getMessage()
            sn.service_type="SERVICE"
            sn.save()



            responsedata={"successstatus":"ok","message":"You have successfully requested for the service","request_id":sr.id}

            print(responsedata)
            return  Response(responsedata)


        except UserSession.DoesNotExist:
            responsedata = {"successstatus": "error","message": "Please Login To Continue"}
            print(responsedata)
            return Response(responsedata)
        except UserDetail.DoesNotExist:
            if userstat==0:
                responsedata={"successstatus":"error","message":"the user doesnot exists"}

            elif userstat==2:
                responsedata = {"successstatus": "error", "message": "the user doesnot exists"}

            print(responsedata)
            return Response(responsedata)

        except ServiceMap.DoesNotExist:

            responsedata = {"successstatus": "error", "message": "the service you are requesting is not available any more"}
            print(responsedata)
            return  Response(responsedata)



        except Exception as e:


            print("error occured in outer except RequestService ")
            print("error : ",e)
            responsedata={"successstatus":"error","message":"error occured trying to request the service"}
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return  Response(responsedata)



class RequestQuickService(APIView):

    def post(self,request):
        responsedata={}
        requestdata={}
        userstat=0
        service_request_address=None
        areapincode=None


        try:
            for key in request.POST:
                requestdata[key]=request.POST[key]

            print("obtained request service data : ",requestdata)

            if ((not requestdata["user_id"])or (not requestdata['user_session_key']) or (not requestdata['service_category']) or (not requestdata['pincode']) or (not requestdata['request_detail'])) :
                responsedata={"successstatus":"error","message":"please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)
            us=UserSession.objects.get(UserSession_key=requestdata['user_session_key'])

            ud=UserDetail.objects.get(id=int(requestdata["user_id"]))
            userstat+=1




            if(requestdata.get("service_request_address",None) is None):
                service_request_address="Not Provided"
            else:
                service_request_address=requestdata["service_request_address"]

            if(requestdata.get("pincode",None) is None):
                areapincode=ud.pincode
            else:
                areapincode=requestdata["pincode"]

            sm=ServiceMap.objects.filter(service_category_id=int(requestdata['service_category']),areapincode=areapincode).order_by("-register_time")
            if(len(sm)<=0):
                responsedata = {"successstatus": "error", "message": "No Service Available in this Area"}

                print(responsedata)
                return Response(responsedata)
            requestsent=0
            for i in range(0,len(sm)):
                print("requesting : ",i)

                try :
                    sd = UserDetail.objects.get(id=sm[i].serviceprovider_id)
                    requestsent+=1
                except :
                    continue
                sr=ServiceRequest()
                sr.user_id=ud.id
                sr.user_ref=ud
                sr.serviceprovider_id=sd.id
                sr.serviceprovider_ref=sd
                sr.service_map_id=sm[i].id
                sr.service_map_ref=sm[i]
                sr.service_category_id=sm[i].service_category_id
                sr.areapincode=areapincode
                sr.service_request_address=service_request_address
                sr.request_detail=requestdata['request_detail']
                sr.notification = sr.getMessage()
                sr.service_type = "QUICK SERVICE"

                sr.save()

                sn=ServiceNotification()
                sn.serviceprovider_id=sr.serviceprovider_id
                sn.serviceprovider_ref=sr.serviceprovider_ref
                sn.servicerequest_id=sr.service_category_id
                sn.servicerequest_ref=sr
                sn.read=False
                #sn.save()
                sn.notification = sn.getMessage()
                sn.service_type="QUICK SERVICE"
                sn.save()


            if(requestsent<=0):
                responsedata = {"successstatus": "error", "message": "No Service Available in this Area"}

                print(responsedata)
                return Response(responsedata)

            responsedata={"successstatus":"ok","message":"You have successfully requested for a quick service"}

            print(responsedata)
            return  Response(responsedata)


        except UserSession.DoesNotExist:
            responsedata = {"successstatus": "error","message": "Please Login To Continue"}
            print(responsedata)
            return Response(responsedata)
        except UserDetail.DoesNotExist:
            if userstat==0:
                responsedata={"successstatus":"error","message":"the user doesnot exists"}

            elif userstat==2:
                responsedata = {"successstatus": "error", "message": "the user doesnot exists"}

            print(responsedata)
            return Response(responsedata)

        except ServiceMap.DoesNotExist:

            responsedata = {"successstatus": "error", "message": "the service you are requesting is not available any more"}
            print(responsedata)
            return  Response(responsedata)



        except Exception as e:


            print("error occured in outer except RequestService ")
            print("error : ",e)
            responsedata={"successstatus":"error","message":"error occured trying to request the service"}
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return  Response(responsedata)








class UpdateStatus(APIView):
    def post(self,request):

        responsedata = {}
        requestdata={}
        try:

            for key in request.POST:
                requestdata[key] = request.POST[key].strip()

            print(requestdata)

            if ((not requestdata['id']) or (not requestdata['user_session_key']) or (not requestdata['history_id']) or (not requestdata['history_type'])  or (not requestdata["status_id"])):
                
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get items data : ", requestdata)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud and ud.user_type==0):
                            try:
                                if(requestdata['history_type'].upper()=="SERVICE"):
                                    ir=OrderHistory.objects.get(id=int(requestdata["history_id"]),serviceprovider_id=ud.id)


                                    if(ir.service_status>int(requestdata["status_id"]) and int(requestdata["status_id"])!=3 ):

                                        responsedata={"successstatus":"error","message":"you can not change to previous status"}
                                        print(responsedata)
                                        return  Response(responsedata)
                                    ir.service_status=int(requestdata["status_id"])
                                    ir.save()

                                    sr=ServiceRequest.objects.get(id=ir.service_map_id)
                                    sr.service_status=int(requestdata["status_id"])
                                    sr.save()
                                if(requestdata['history_type'].upper()=="PRODUCT"):
                                    ir=ItemOrderHistory.objects.get(id=int(requestdata["history_id"]),serviceprovider_id=ud.id)


                                    if(ir.item_status>int(requestdata["status_id"]) and int(requestdata["status_id"])!=3 ):

                                        responsedata={"successstatus":"error","message":"you can not change to previous state"}
                                        print(responsedata)
                                        return  Response(responsedata)
                                    ir.item_status=int(requestdata["status_id"])
                                    ir.save()

                                    sr=ItemRequest.objects.get(id=ir.item_map_id)
                                    sr.item_status=int(requestdata["status_id"])
                                    sr.save()

                                responsedata={"successstatus":"ok","message":"status updated successfully"}
                                print(responsedata)
                                return Response(responsedata)

                            except OrderHistory.DoesNotExist:
                                responsedata={"successstatus":"error","messsage":'No History availabe for you with given details'}
                                print(responsedata)
                                return  Response(responsedata)

                            except ServiceRequest.DoesNotExist:
                                responsedata={"successstatus":"error","messsage":'No Service availabe for you with given details'}
                                print(responsedata)
                                return  Response(responsedata)
                            except ItemOrderHistory.DoesNotExist:
                                responsedata={"successstatus":"error","messsage":'No History availabe for you with given details'}
                                print(responsedata)
                                return  Response(responsedata)

                            except ItemRequest.DoesNotExist:
                                responsedata={"successstatus":"error","messsage":'No Service availabe for you with given details'}
                                print(responsedata)
                                return  Response(responsedata)

                    except Exception as e:
                        responsedata={"successstatus":"error","message":"Unknown error occured"}
                        print(responsedata)
                        print("Error occured : ",e)
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(True, exc_type, fname, exc_tb.tb_lineno)
                        return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except Exception as e:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in Confirm Order : outer except : ", responsedata)
            print("Error : ",e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)











class AddToFavouriteService(APIView):
    def post(self,request):
        responsedata = {}
        requestdata = {}
        userstat = 0
        service_request_address = None
        areapincode = None

        try:
            for key in request.POST:
                requestdata[key] = request.POST[key]

            print("obtained request service data : ", requestdata)

            if ((not requestdata["user_id"]) or (not requestdata['user_session_key']) or (not requestdata['servicemap_id'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)
            us = UserSession.objects.get(UserSession_key=requestdata['user_session_key'])

            ud = UserDetail.objects.get(id=int(requestdata["user_id"]))
            userstat+=1

            userstat+=1


            try:
                sm = ServiceMap.objects.get(id=int(requestdata["servicemap_id"]))
                if(sm):
                    try:
                        fsp=FavouriteService.objects.get(user_id=ud.id,servicemap_id=sm.id)
                        responsedata = {"successstatus": "error","message": "service is already in your favourites list"}
                        print(responsedata)
                        return Response(responsedata)
                    except FavouriteService.DoesNotExist:
                        pass
                    #print("user id : ",ud.id)
                    #print("service provider id : ",sp.id)
                    fs = FavouriteService()
                    fs.user_id = ud.id
                    fs.servicemap_id = sm.id
                    fs.servicemap_ref = sm
                    fs.save()

                    responsedata = {"successstatus": "ok", "message": "added to your favourites list"}
                    print(responsedata)
                    return Response(responsedata)


            except ServiceMap.DoesNotExist:
                responsedata={"successstatus":"error","message":"the service does not exists"}
                print(responsedata)
                return Response(responsedata)

            except Exception as e:
                responsedata={"successstatus":"error","message":"unknown error occured while Adding To Favourite"}
                print("error occured")
                print("Error : ",e)
                print(responsedata)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(True, exc_type, fname, exc_tb.tb_lineno)
                return  Response(responsedata)




        except UserSession.DoesNotExist:
            responsedata = {"successstatus": "error", "message": "Please Login To Continue"}
            print(responsedata)
            return Response(responsedata)
        except UserDetail.DoesNotExist:
            responsedata = {"successstatus": "error", "message": "the user does not exists"}

            print(responsedata)
            return Response(responsedata)

        except ServiceMap.DoesNotExist:

            responsedata = {"successstatus": "error","message": "the service you are requesting is not available any more"}
            print(responsedata)
            return Response(responsedata)

        except ServiceRequest.DoesNotExist:
            responsedata = {"successstatus": "error", "message": "the service doesnot exist anymore"}
            print(responsedata)
            return Response(responsedata)


        except Exception as e:

            print("error occured in outer except RequestService ")
            print("error : ", e)
            responsedata = {"successstatus": "error", "message": "error occured trying to request the service"}
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)


class RemoveFavouriteService(APIView):
    def post(self,request):
        responsedata = {}
        requestdata = {}
        userstat = 0
        service_request_address = None
        areapincode = None

        try:
            for key in request.POST:
                requestdata[key] = request.POST[key]

            print("obtained request service data : ", requestdata)

            if ((not requestdata["user_id"]) or (not requestdata['user_session_key']) or (not requestdata['servicemap_id'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)
            us = UserSession.objects.get(UserSession_key=requestdata['user_session_key'])

            ud = UserDetail.objects.get(id=int(requestdata["user_id"]))
            userstat += 1

            userstat += 1

            try:
                sm = ServiceMap.objects.get(id=int(requestdata["servicemap_id"]))
                if (sm):
                    try:
                        fsp = FavouriteService.objects.get(user_id=ud.id, servicemap_id=sm.id)
                        fsp.delete()
                        responsedata = {"successstatus": "ok","message": "service is deleted from your favourites list"}
                        print(responsedata)
                        return Response(responsedata)
                    except FavouriteService.DoesNotExist:
                        responsedata = {"successstatus": "error","message": "service is not in your favourites list"}
                        print(responsedata)
                        return Response(responsedata)



            except ServiceMap.DoesNotExist:
                responsedata = {"successstatus": "error", "message": "the service does not exists"}
                print(responsedata)
                return Response(responsedata)

            except Exception as e:
                responsedata = {"successstatus": "error", "message": "unknown error occured while Adding To Favourite"}
                print("error occured")
                print("Error : ", e)
                print(responsedata)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(True, exc_type, fname, exc_tb.tb_lineno)
                return Response(responsedata)




        except UserSession.DoesNotExist:
            responsedata = {"successstatus": "error", "message": "Please Login To Continue"}
            print(responsedata)
            return Response(responsedata)
        except UserDetail.DoesNotExist:
            responsedata = {"successstatus": "error", "message": "the user does not exists"}

            print(responsedata)
            return Response(responsedata)



        except Exception as e:

            print("error occured in outer except RequestService ")
            print("error : ", e)
            responsedata = {"successstatus": "error", "message": "error occured trying to request the service"}
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)


class GetFavouriteServices(APIView):
    def post(self,request):
        responsedata = {}
        requestdata = {}
        favservice=[]
        # userstat = 0
        service_request_address = None
        areapincode = None

        try:
            for key in request.POST:
                requestdata[key] = request.POST[key]

            print("obtained request service data : ", requestdata)

            if ((not requestdata["user_id"]) or (not requestdata['user_session_key']) ):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)
            us = UserSession.objects.get(UserSession_key=requestdata['user_session_key'])

            ud = UserDetail.objects.get(id=int(requestdata["user_id"]))


            fs = FavouriteService.objects.filter(user_id=ud.id)
            sfs=FavouriteServiceSerializer(fs,many=True)

            for i in range (0,len(fs)):
                try:
                    sm=ServiceMap.objects.get(id=fs[i].servicemap_id)
                    #tmpdata = {"fav_id":fs[i].id,"service_id": sc.id, "service_name": sc.service_name, "service_detail": sc.service_detail,"service_image": settings.BASE_IP + sc.service_image.url}
                    ssm=ServiceMapSerializer(sm)
                    favservice.append(ssm.data)
                except:
                    continue


            responsedata = {"successstatus": "ok", "favservices":favservice}
            #print(responsedata)
            print("succesfully fetched the favourites list")
            return Response(responsedata)


        except UserSession.DoesNotExist:
            responsedata = {"successstatus": "error", "message": "Please Login To Continue"}
            print(responsedata)
            return Response(responsedata)
        except UserDetail.DoesNotExist:
            responsedata = {"successstatus": "error", "message": "the user doesnot exists"}

            print(responsedata)
            return Response(responsedata)

        except ServiceMap.DoesNotExist:

            responsedata = {"successstatus": "error",
                            "message": "the service you are requesting is not available any more"}
            print(responsedata)
            return Response(responsedata)

        except ServiceRequest.DoesNotExist:
            responsedata = {"successstatus": "error", "message": "the service doesnot exist anymore"}
            print(responsedata)
            return Response(responsedata)

        except FavouriteService.DoesNotExist:
            responsedata={"successstatus":"error","message":"No favourites list available for this user"}
            print(responsedata)
            return Response(responsedata)
        except Exception as e:

            print("error occured in outer except RequestService ")
            print("error : ", e)
            responsedata = {"successstatus": "error", "message": "error occured trying to request the service"}
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)


class IsInFavourite(APIView):
    def post(self,request):
        responsedata = {}
        requestdata = {}
        favservice = []
        # userstat = 0
        service_request_address = None
        areapincode = None

        try:
            for key in request.POST:
                requestdata[key] = request.POST[key]

            print("obtained request service data : ", requestdata)

            if ((not requestdata["user_id"]) or (not requestdata['user_session_key']) or (not requestdata['servicemap_id'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)
            us = UserSession.objects.get(UserSession_key=requestdata['user_session_key'])

            ud = UserDetail.objects.get(id=int(requestdata["user_id"]))

            try:
                sm = ServiceMap.objects.get(id=int(requestdata["servicemap_id"]))
                if(sm):
                    try:
                        fsp=FavouriteService.objects.get(user_id=ud.id,servicemap_id=sm.id)
                        responsedata = {"successstatus": "ok","message": "service is in your favourites list","isfavourite":True}
                        print(responsedata)
                        return Response(responsedata)
                    except FavouriteService.DoesNotExist:
                        responsedata = {"successstatus": "error", "message": "service is not in your favourites list","isfavourite": False}
                        print(responsedata)
                        return Response(responsedata)


            except ServiceMap.DoesNotExist:
                responsedata={"successstatus":"error","message":"the service does not exists"}
                print(responsedata)
                return Response(responsedata)

            except Exception as e:
                responsedata={"successstatus":"error","message":"unknown error occured while Trying To get  isfavourite"}
                print("error occured")
                print("Error : ",e)
                print(responsedata)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(True, exc_type, fname, exc_tb.tb_lineno)
                return  Response(responsedata)


        except UserSession.DoesNotExist:
            responsedata = {"successstatus": "error", "message": "Please Login To Continue"}
            print(responsedata)
            return Response(responsedata)
        except UserDetail.DoesNotExist:
            responsedata = {"successstatus": "error", "message": "the user doesnot exists"}

            print(responsedata)
            return Response(responsedata)

        except ServiceMap.DoesNotExist:

            responsedata = {"successstatus": "error",
                            "message": "the service you are requesting is not available any more"}
            print(responsedata)
            return Response(responsedata)

        except Exception as e:

            print("error occured in outer except RequestService ")
            print("error : ", e)
            responsedata = {"successstatus": "error", "message": "error occured trying to request the service"}
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)

class GetItemByCategory(APIView):
    def get(self,request,catid):
        if (not catid) :
            print("not all data in GetItemByCategory")
            responsedata = {"successstatus": "error", "message": "please procvide all the details necessary"}
            print("in get providers list : ", responsedata)
            return Response(responsedata)

        try:
            itemsdata=[]
            im=ItemMap.objects.filter(product_category_id=int(catid))
            # for i in range(0,len(im)):
            #     tmpdata={"iteme_image":settings.BASE_IP+im[i].item_image.url,"id":im[i].id,"serviceprovider_id":im[i].serviceprovider_id,"serviceprovider_email":im[i].serviceprovider_email,'item_category_id':im[i].product_category_id,'item_name':im[i].item_name,'item_details':im[i].item_details,'item_features':im[i].item_features,'item_MRP':im[i].item_MRP,'item_SLP':im[i].item_SLP}
            #     itemsdata.append(tmpdata)
            sim=ItemMapSerializer(im,many=True)
            if(len(sim.data)<=0):

                responsedata={"successstatus":"error","message":"{0} Items Found".format(len(im)),"itemdata":sim.data}
            else:
                responsedata = {"successstatus": "ok", "message": "{0} Items Found".format(len(im)),"itemdata": sim.data}
            print(responsedata)
            return  Response(responsedata)

        except ItemMap.DoesNotExist:
            responsedata={"successstatus":"error","message":"no items available for this category"}
            print(responsedata)
            return Response(responsedata)
        except Exception as e:
            responsedata={"successstatus":"error","message":"unknown error occured getting item by category"}
            print("Error : ", e)
            print(responsedata)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return  Response(responsedata)






class GetItemById(APIView):
    def get(self,request,itemid):
        if (not itemid) :
            print("not all data in GetItemByCategory")
            responsedata = {"successstatus": "error", "message": "please procvide all the details necessary"}
            print("in get providers list : ", responsedata)
            return Response(responsedata)

        try:
            itemsdata=[]
            im=ItemMap.objects.get(id=int(itemid))
            # for i in range(0,len(im)):
            #     tmpdata={"iteme_image":settings.BASE_IP+im[i].item_image.url,"id":im[i].id,"serviceprovider_id":im[i].serviceprovider_id,"serviceprovider_email":im[i].serviceprovider_email,'item_category_id':im[i].product_category_id,'item_name':im[i].item_name,'item_details':im[i].item_details,'item_features':im[i].item_features,'item_MRP':im[i].item_MRP,'item_SLP':im[i].item_SLP}
            #     itemsdata.append(tmpdata)
            sim=ItemMapSerializer(im)
            responsedata = {"successstatus": "ok","itemdata": sim.data}
            print(responsedata)
            return  Response(responsedata)

        except ItemMap.DoesNotExist:
            responsedata={"successstatus":"error","message":"no items available for this id"}
            print(responsedata)
            return Response(responsedata)
        except Exception as e:
            responsedata={"successstatus":"error","message":"unknown error occured getting item by id"}
            print("Error : ", e)
            print(responsedata)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return  Response(responsedata)





class GetItemByProvider(APIView):
    def get(self,request,providerid):
        if (not providerid) :
            print("not all data in GetItemByCategory")
            responsedata = {"successstatus": "error", "message": "please procvide all the details necessary"}
            print("in get providers list : ", responsedata)
            return Response(responsedata)

        try:
            itemsdata=[]
            im=ItemMap.objects.filter(product_category_id=int(providerid))
            for i in range(0,len(im)):
                tmpdata={"iteme_image":settings.BASE_IP+im[i].item_image.url,"id":im[i].id,"serviceprovider_id":im[i].serviceprovider_id,"serviceprovider_email":im[i].serviceprovider_email,'item_category_id':im[i].product_category_id,'item_name':im[i].item_name,'item_details':im[i].item_details,'item_features':im[i].item_features,'item_MRP':im[i].item_MRP,'item_SLP':im[i].item_SLP}
                itemsdata.append(tmpdata)
            responsedata={"successstatus":"ok","message":"{0} Items Found".format(len(im)),"itemdata":itemsdata}
            print(responsedata)
            return  Response(responsedata)

        except ItemMap.DoesNotExist:
            responsedata={"successstatus":"error","message":"no items available for this category"}
            print(responsedata)
            return Response(responsedata)
        except Exception as e:
            responsedata={"successstatus":"error","message":"unknown error occured getting item by provider"}
            print(responsedata)
            return  Response(responsedata)

import json
import urllib
from urllib.request import urlopen

class GetPincode(APIView):
    def get(self,request,lan,lat):
        responsedata={}
        pincodes=[]
        a={}
        try:
            if((not lan) or  (not lat)):
                responsedata={"successstatus":"error","message":"please provide all the details necessary"}
                print(responsedata)
                return  Response(responsedata)
            url="http://api.geonames.org/findNearbyPostalCodesJSON?lat={0}&lng={1}&radius=5&maxRows=100&username=vaibhawm"
            furl=url.format(float(lan),float(lat))
            r=urlopen(furl)
            d=r.read().decode()
            #print(type(d))
            d=json.loads(d)
            #print(d)
            d=d["postalCodes"]
            for i in d:
                pincodes.append(i["postalCode"])
            for p in pincodes:
                a[p] = 0
            pincodes=list(a.keys())
            responsedata={"successstatus":"ok","pincodes":pincodes}
            print(responsedata)
            return Response(responsedata)
        except Exception as e:
            responsedata = {"successstatus": "error", "message": "unknown error occured getting pincode"}
            print(responsedata)
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)









from .models import  ItemRequest
from .serializers import ItemRequestSerializer

from .models import ItemNotification
from .serializers import ItemRequestSerializer
class RequestProduct(APIView):

    def post(self,request):
        responsedata={}
        requestdata={}
        userstat=0
        service_request_address=None
        areapincode=None


        try:
            for key in request.POST:
                requestdata[key]=request.POST[key]

            print("obtained request service data : ",requestdata)

            if ((not requestdata["serviceprovider_id"]) or (not requestdata["user_id"]) or (not requestdata["item_map_id"]) or (not requestdata['user_session_key']) or (not requestdata['quantity']) ) :
                responsedata={"successstatus":"error","message":"please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)
            us=UserSession.objects.get(UserSession_key=requestdata['user_session_key'])

            ud=UserDetail.objects.get(id=int(requestdata["user_id"]))
            userstat+=1
            sd=UserDetail.objects.get(id=int(requestdata["serviceprovider_id"]))
            userstat+=1

            imap=ItemMap.objects.get(id=int(requestdata["item_map_id"]))

            if(requestdata.get("item_request_address",None) is None):
                item_request_address=None
            else:
                item_request_address=requestdata["item_request_address"]

            if(requestdata.get("areapincode",None) is None):
                areapincode=ud.pincode
            else:
                areapincode=requestdata["areapincode"]

            #sm=ServiceMap.objects.get(id=int(requestdata["service_map_id"]))

            ir=ItemRequest()
            ir.user_id=ud.id
            ir.user_ref=ud
            ir.serviceprovider_id=sd.id
            ir.serviceprovider_ref=sd
            ir.item_map_id=imap.id
            ir.item_map_ref=imap
            ir.item_category_id=imap.product_category_id
            ir.areapincode=areapincode
            ir.item_request_address=item_request_address
            ir.item_quantity=int(requestdata['quantity'])
            ir.notification = ir.getMessage()

            ir.save()

            ino=ItemNotification()
            ino.serviceprovider_id=ir.serviceprovider_id
            ino.serviceprovider_ref=ir.serviceprovider_ref
            ino.itemrequest_id=ir.id
            ino.itemrequest_ref=ir
            ino.read=False
            #sn.save()
            ino.notification = ino.getMessage()
            ino.save()



            responsedata={"successstatus":"ok","message":"You have successfully requested for the item","request_id":ir.id}

            print(responsedata)
            return  Response(responsedata)


        except UserSession.DoesNotExist:
            responsedata = {"successstatus": "error","message": "Please Login To Continue"}
            print(responsedata)
            return Response(responsedata)
        except UserDetail.DoesNotExist:
            if userstat==0:
                responsedata={"successstatus":"error","message":"the user doesnot exists"}

            elif userstat==2:
                responsedata = {"successstatus": "error", "message": "the user doesnot exists"}

            print(responsedata)
            return Response(responsedata)

        except ItemMap.DoesNotExist:

            responsedata = {"successstatus": "error", "message": "the Item you are requesting is not available any more"}
            print(responsedata)
            return  Response(responsedata)



        except Exception as e:


            print("error occured in outer except RequestService ")
            print("error : ",e)
            responsedata={"successstatus":"error","message":"error occured trying to request the item"}
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return  Response(responsedata)










from .models import ItemOrderHistory
from .serializers import ItemOrderHistorySerializer

class ConfirmItemRequest(APIView):
    def post(self,request):

        responsedata = {}
        requestdata={}
        try:

            for key in request.POST:
                requestdata[key] = request.POST[key].strip()

            print(requestdata)

            if ((not requestdata['id']) or (not requestdata['user_session_key']) or (not requestdata['itemrequest_id'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get items data : ", requestdata)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud and ud.user_type==0):
                            try:
                                ir=ItemRequest.objects.get(id=int(requestdata["itemrequest_id"]),serviceprovider_id=ud.id)

                                try:
                                    ioh = ItemOrderHistory.objects.get(serviceprovider_id=ud.id, request_id=ir.id)
                                    if (ioh or ir.item_status != 0):
                                        responsedata = {"successstatus": "error","message": "request is already confirmed"}
                                        print(responsedata)
                                        return Response(responsedata)
                                except:
                                    pass
                                ir.item_status=1
                                ir.save()

                                cr=ItemOrderHistory()

                                cr.user_id=ir.user_id
                                cr.user_ref=ir.user_ref
                                cr.serviceprovider_id=ir.serviceprovider_id
                                cr.serviceprovider_ref=ir.serviceprovider_ref
                                cr.item_map_id=ir.item_map_id
                                cr.item_map_ref=ir.item_map_ref
                                cr.item_request_id=ir.id
                                cr.item_request_ref=ir
                                cr.confirmation_id=GetConfirmationId(rtype="PRO",rid=ir.id)

                                cr.save()

                                responsedata={"successstatus":"ok","confirmation_id":cr.confirmation_id}
                                print(responsedata)
                                return Response(responsedata)

                            except ItemRequest.DoesNotExist:
                                responsedata={"successstatus":"error","messsage":'No Item availabe for you with given details'}
                                print(responsedata)
                                return  Response(responsedata)

                    except Exception as e:
                        responsedata={"successstatus":"error","message":"Unknown error occured"}
                        print(responsedata)
                        print("Error occured : ",e)
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(True, exc_type, fname, exc_tb.tb_lineno)
                        return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except Exception as e:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in Confirm Order : outer except : ", responsedata)
            print("Error : ",e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)




class GetMyItemRequests(APIView):

    def post(self, request):

        responsedata = {}
        request_data = {}
        xssr=[]

        try:

            for key in request.POST:
                request_data[key] = request.POST[key].strip()

            if ((not request_data['id']) or (not request_data['user_session_key'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get item request data : ", request_data)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud):
                            try:
                                if(ud.user_type==0):
                                    sr = ItemRequest.objects.filter(serviceprovider_id=ud.id).order_by("-request_time")
                                else:
                                    sr = ItemRequest.objects.filter(user_id=ud.id).order_by("-request_time")

                                if (sr):
                                    ssr = ItemRequestSerializer(sr, many=True)

                                    # print("sm : ",sm)
                                    #print(ssr.data)
                                    xssr=ssr.data
                                    for s in range(0,len(xssr)):
                                        tmsg=0
                                        try:
                                            rm=RequestMessage.objects.filter(request_id=xssr[s]["id"],receiver_id=ud.id,request_type="PRODUCT").order_by("sending_time")
                                            for r in rm:
                                                try:
                                                    if not r.read:
                                                        tmsg+=1
                                                except:
                                                    print("error.......")
                                                    continue
                                            xssr[s]["unread_message"]=tmsg
                                        except Exception as e:
                                            xssr[s]["unread_message"]=tmsg
                                    print(xssr)
                                    responsedata={"successstatus":"ok","requests":xssr}
                                    return Response(responsedata)

                                else:
                                    responsedata = {"successstatus": "error","message": "No request Available"}
                                    print(responsedata)
                                    return Response(responsedata)



                            except ItemRequest.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "No request Available"}
                                print(responsedata)
                                return Response(responsedata)


                        else:
                            responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                            print(responsedata)
                            return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in outer except : ", responsedata)
            return Response(responsedata)










class GetMySingleItemRequest(APIView):

    def post(self, request):

        responsedata = {}
        request_data = {}

        try:

            for key in request.POST:
                request_data[key] = request.POST[key].strip()

            print("request data : ",request_data)

            if ((not request_data['id']) or (not request_data['user_session_key']) or (not request_data['request_id'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get single item request data : ", request_data)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud):
                            try:
                                if (ud.user_type == 0):
                                    print("ud id : ",ud.id)
                                    print("request id : ",request_data['request_id'])
                                    sr = ItemRequest.objects.get(id=int(request_data['request_id']),serviceprovider_id=int(request_data['id']))#.order_by("-request_time")
                                else:
                                    sr = ItemRequest.objects.get(user_id=ud.id,id=int(request_data['request_id']))#.order_by("-request_time")

                                # if(request_data.get("notification_id",None) is not None):
                                #     try:
                                #         pn=ItemNotification.objects.get(id=int(request_data["notification_id"]))
                                #         pn.read=True
                                #         pn.save()
                                #     except:
                                #         pass

                                if (sr):
                                    if(not sr.read  and ud.user_type==0):
                                        sr.read=True
                                        sr.save()
                                    ssr = ItemRequestSerializer(sr)
                                    tdata=ssr.data
                                    # try:
                                    #     rud = UserDetail.objects.get(id=sr.user_id)
                                    # except Exception as e:
                                    #     responsedata={"successstatus":"error","messgae":"could not get requester's details"}
                                    #     print("response data : ",responsedata)
                                    #     print("Error occured : ",e)
                                    #     return Response(responsedata)
                                    tdata["user_name"]=sr.user_ref.full_name
                                    tdata["mobile"]=sr.user_ref.mobile
                                    tdata["item_name"]=sr.item_map_ref.item_name


                                    try:
                                        rm=RequestMessage.objects.filter(request_id=sr.id,request_type=sr.request_type).order_by("sending_time")
                                        for r in rm:
                                            try:
                                                if (not r.read):
                                                    r.read=True
                                                    r.save()
                                            except:
                                                continue
                                    except Exception as e:
                                        pass
                                        #print("Error in reqading item message : ",e)

                                    # print("sm : ",sm)
                                    print("final data : ",tdata)
                                    responsedata={"successstatus":"ok","request_detail":tdata}

                                    return Response(responsedata)

                                else:
                                    responsedata = {"successstatus": "error", "message": "No request Available"}
                                    print(responsedata)
                                    return Response(responsedata)



                            except ItemRequest.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "No request Available"}
                                print(responsedata)
                                return Response(responsedata)
                            except Exception as e:

                                responsedata = {"successstatus": "error", "message": "Unknown Error"}
                                print("in inner : ", responsedata)
                                print("Error : ", e)
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                print(True, exc_type, fname, exc_tb.tb_lineno)
                                return Response(responsedata)


                        else:
                            responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                            print(responsedata)
                            return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except Exception as e:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in outer except : ", responsedata)
            print("Error : ", e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)


from .models import RequestMessage
from .serializers import RequestMessageSerializer
class SendMessage(APIView):
    def post(self,request):
        responsedata={}
        requestdata={}
        userstat=0
        service_request_address=None
        areapincode=None


        try:
            for key in request.POST:
                requestdata[key]=request.POST[key]

            print("obtained request service data : ",requestdata)

            if ( (not requestdata["receiver_id"]) or (not requestdata["user_id"]) or (not requestdata["request_id"]) or (not requestdata['user_session_key']) or (not requestdata['request_type']) or (not requestdata["message"]) ) :
                responsedata={"successstatus":"error","message":"please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)
            us=UserSession.objects.get(UserSession_key=requestdata['user_session_key'])

            ud=UserDetail.objects.get(id=int(requestdata["user_id"]))
            userstat+=1
            sd=UserDetail.objects.get(id=int(requestdata["receiver_id"]))
            userstat+=1

            if(requestdata['request_type'].upper()=="SERVICE"):
                try:
                    r=ServiceRequest.objects.get(id=int(requestdata["request_id"]))
                except ServiceRequest.DoesNotExist:
                    responsedata={"successstatus":"error","message":"service request not available"}
                    print(responsedata)
                    return Response(responsedata)

            elif(requestdata['request_type'].upper()=="PRODUCT"):
                try:
                    r=ItemRequest.objects.get(id=int(requestdata["request_id"]))
                except ItemRequest.DoesNotExist:
                    responsedata={"successstatus":"error","message":"product request not available"}
                    print(responsedata)
                    return Response(responsedata)
            else:
                responsedata={"successstatus":"error","message":"please provide correct request type [SERVICE] or [PRODUCT]"}
                print(responsedata)
                return  Response(responsedata)

            rm=RequestMessage()
            rm.sender_id=ud.id
            rm.sender_ref=ud
            rm.receiver_id=sd.id
            rm.receiver_ref=sd
            rm.request_id=r.id
            rm.request_type=requestdata['request_type'].upper()
            if(rm.request_type=="SERVICE"):
                rm.servicerequest_ref=r
            elif(rm.request_type=="PRODUCT"):
                rm.itemrequest_ref=r
            else:
                responsedata = {"successstatus": "error","message": "please provide correct request type [SERVICE] or [PRODUCT]"}
                print(responsedata)
                return Response(responsedata)
            rm.message_text=requestdata['message']
            rm.save()



            responsedata={"successstatus":"ok","message":"message sent"}

            print(responsedata)
            return  Response(responsedata)


        except UserSession.DoesNotExist:
            responsedata = {"successstatus": "error","message": "Please Login To Continue"}
            print(responsedata)
            return Response(responsedata)
        except UserDetail.DoesNotExist:
            if userstat==0:
                responsedata={"successstatus":"error","message":"the user doesnot exists"}

            elif userstat==2:
                responsedata = {"successstatus": "error", "message": "the user doesnot exists"}

            print(responsedata)
            return Response(responsedata)

        except ItemMap.DoesNotExist:

            responsedata = {"successstatus": "error", "message": "the Item you are messaging for is not available any more"}
            print(responsedata)
            return  Response(responsedata)



        except Exception as e:


            print("error occured in outer except RequestService ")
            print("error : ",e)
            responsedata={"successstatus":"error","message":"error occured trying to request the item"}
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return  Response(responsedata)



class GetMessages(APIView):
    def post(self,request):
        responsedata={}
        requestdata={}
        userstat=0
        service_request_address=None
        areapincode=None
        budget=0.0


        try:
            for key in request.POST:
                requestdata[key]=request.POST[key]

            print("obtained request service data : ",requestdata)

            if ( (not requestdata["user_id"]) or (not requestdata["request_id"]) or (not requestdata['user_session_key'])  or (not requestdata['request_type']) ) :
                responsedata={"successstatus":"error","message":"please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)
            us=UserSession.objects.get(UserSession_key=requestdata['user_session_key'])

            ud=UserDetail.objects.get(id=int(requestdata["user_id"]))
            userstat+=1
            # sd=UserDetail.objects.get(id=int(requestdata["receiver_id"]))
            # userstat+=1



            rm=RequestMessage.objects.filter(request_id=int(requestdata["request_id"]),request_type=requestdata['request_type']).order_by("sending_time")
            srm=RequestMessageSerializer(rm,many=True)
            try:

                if(requestdata['request_type']=="PRODUCT"):
                    budget=rm[0].itemrequest_ref.final_budget
                elif(requestdata['request_type']=="SERVICE"):
                    budget = rm[0].servicerequest_ref.final_budget

                responsedata={"successstatus":"ok","messages":srm.data,"budget":budget}
            except:
                pass

            #print(responsedata)
            return  Response(responsedata)


        except UserSession.DoesNotExist:
            responsedata = {"successstatus": "error","message": "Please Login To Continue"}
            print(responsedata)
            return Response(responsedata)
        except UserDetail.DoesNotExist:
            if userstat==0:
                responsedata={"successstatus":"error","message":"the user doesnot exists"}

            elif userstat==2:
                responsedata = {"successstatus": "error", "message": "the user doesnot exists"}

            print(responsedata)
            return Response(responsedata)

        except ItemMap.DoesNotExist:

            responsedata = {"successstatus": "error", "message": "the Item you are requesting is not available any more"}
            print(responsedata)
            return  Response(responsedata)



        except Exception as e:


            print("error occured in outer except GetMessage ")
            print("error : ",e)
            responsedata={"successstatus":"error","message":"error occured trying to request the item"}
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return  Response(responsedata)




from .models import Review
from .serializers import ReviewSerializer
class WriteReview(APIView):
    def post(self,request):
        responsedata = {}
        requestdata = {}
        userstat = 0
        service_request_address = None
        areapincode = None

        try:
            for key in request.POST:
                requestdata[key] = request.POST[key]

            print("obtained request service data : ", requestdata)

            if ( (not requestdata["user_id"]) or (not requestdata['user_session_key']) or (not requestdata["service_star"]) or (not requestdata["quality_star"]) or (not requestdata['value_star'])  or (not requestdata['title'])   or (not requestdata['comment'])   or (not requestdata['history_id'])   or (not requestdata['review_type'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)
            us = UserSession.objects.get(UserSession_key=requestdata['user_session_key'])

            ud = UserDetail.objects.get(id=int(requestdata["user_id"]))


            try:
                tr=Review.objects.get(history_id=int(requestdata['history_id']),review_type=requestdata['review_type'],user_id=ud.id)
                if(tr):
                    responsedata={"successstatus":"error","message":"You have already written a Review before"}
                    print(responsedata)
                    return Response(responsedata)
            except:
                pass

            rv=Review()

            if (requestdata['review_type'].upper() == "SERVICE"):
                try:
                    h = OrderHistory.objects.get(id=int(requestdata["history_id"]))
                    if(h.review_written):
                        responsedata = {"successstatus": "error", "message": "You have already written a Review before"}
                        print(responsedata)
                        return Response(responsedata)

                    m = ServiceMap.objects.get(id=h.service_map_id)

                    rv.review_type="SERVICE".upper()
                    rv.map_id=m.id
                    rv.servicemap_ref=m
                    rv.history_id = h.id
                    rv.servicehistory_ref=h
                    rv.provider_id = h.serviceprovider_id
                    rv.provider_ref = h.serviceprovider_ref

                except OrderHistory.DoesNotExist:
                    responsedata = {"successstatus": "error", "message": "service history is not available"}
                    print(responsedata)
                    return Response(responsedata)

                except ServiceMap.DoesNotExist:
                    responsedata = {"successstatus": "error", "message": "service is not available"}
                    print(responsedata)
                    return Response(responsedata)

            elif (requestdata['review_type'].upper() == "PRODUCT"):
                try:
                    h = ItemOrderHistory.objects.get(id=int(requestdata["history_id"]))
                    if (h.review_written):
                        responsedata = {"successstatus": "error", "message": "You have already written a Review before"}
                        print(responsedata)
                        return Response(responsedata)

                    m = ItemMap.objects.get(id=h.item_map_id)

                    rv.review_type = "PRODUCT".upper()
                    rv.map_id=m.id
                    rv.itemmapt_ref=m
                    rv.history_id=h.id
                    rv.itemhistory_ref=h
                    rv.provider_id=h.serviceprovider_id
                    rv.provider_ref=h.serviceprovider_ref

                except ItemOrderHistory.DoesNotExist:
                    responsedata = {"successstatus": "error", "message": "product history is not available"}
                    print(responsedata)
                    return Response(responsedata)
                except ItemRequest.DoesNotExist:
                    responsedata = {"successstatus": "error", "message": "product is not available"}
                    print(responsedata)
                    return Response(responsedata)
            else:
                responsedata = {"successstatus": "error","message": "please provide correct request type [SERVICE] or [PRODUCT]"}
                print(responsedata)
                return Response(responsedata)


            rv.user_id=ud.id
            rv.user_name=ud.full_name
            rv.user_ref=ud
            rv.service_star=int(requestdata["service_star"])
            rv.value_star=int(requestdata["value_star"])
            rv.quality_star = int(requestdata["quality_star"])
            rv.title=requestdata["title"]
            rv.comment=requestdata["comment"]

            rv.save()

            h.review_written = True
            h.save()





            responsedata = {"successstatus": "ok", "message": "review posted"}

            print(responsedata)
            return Response(responsedata)


        except UserSession.DoesNotExist:
            responsedata = {"successstatus": "error", "message": "Please Login To Continue"}
            print(responsedata)
            return Response(responsedata)
        except UserDetail.DoesNotExist:
            if userstat == 0:
                responsedata = {"successstatus": "error", "message": "the user doesnot exists"}

            elif userstat == 2:
                responsedata = {"successstatus": "error", "message": "the user doesnot exists"}

            print(responsedata)
            return Response(responsedata)

        except ItemMap.DoesNotExist:

            responsedata = {"successstatus": "error",
                            "message": "the Item you are messaging for is not available any more"}
            print(responsedata)
            return Response(responsedata)



        except Exception as e:

            print("error occured in outer except RequestService ")
            print("error : ", e)
            responsedata = {"successstatus": "error", "message": "error occured trying to write the review"}
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)






#
#
#
# class GetMyReviews(APIView):
#     def post(self,request):
#         responsedata={}
#         requestdata={}
#         userstat=0
#         service_request_address=None
#         areapincode=None
#         h=None
#         r=None
#
#
#         try:
#             for key in request.POST:
#                 requestdata[key]=request.POST[key]
#
#             print("obtained request service data : ",requestdata)
#
#             if ( (not requestdata["user_id"]) or (not requestdata["history_id"]) or (not requestdata['user_session_key'])  or (not requestdata['review_type']) ) :
#                 responsedata={"successstatus":"error","message":"please provide all the details necessary"}
#                 print(responsedata)
#                 return Response(responsedata)
#             us=UserSession.objects.get(UserSession_key=requestdata['user_session_key'])
#
#             ud=UserDetail.objects.get(id=int(requestdata["user_id"]))
#             h = Review.objects.get(id=int(requestdata["history_id"]))
#
#             if(requestdata['request_type'].upper()=="SERVICE"):
#                 try:
#                     if(ud.user_type==0):
#
#                         r=Review.objects.filter(history_id=h.id,review_type="SERVICE".upper(),provider_id=ud.id).order_by("-review_time")
#                     elif(ud.user_type==1):
#                         r = Review.objects.filter(history_id=h.id, review_type="SERVICE".upper(), user_id=ud.id).order_by("-review_time")
#                     else:
#                         responsedata={"successstatus":"error","message":"You are not a valid user"}
#                         print(responsedata)
#                         return  Response(responsedata)
#                 except Review.DoesNotExist:
#                     responsedata={"successstatus":"error","message":"no review available"}
#                     print(responsedata)
#                     return Response(responsedata)
#
#                 if (requestdata['request_type'].upper() == "PRODUCT"):
#                     try:
#                         if (ud.user_type == 0):
#
#                             r = Review.objects.filter(history_id=h.id, review_type="PRODUCT".upper(),provider_id=ud.id).order_by("-review_time")
#                         elif (ud.user_type == 1):
#                             r = Review.objects.filter(history_id=h.id, review_type="PRODUCT".upper(),user_id=ud.id).order_by("-review_time")
#                         else:
#                             responsedata = {"successstatus": "error", "message": "You are not a valid user"}
#                             print(responsedata)
#                             return Response(responsedata)
#                     except Review.DoesNotExist:
#                         responsedata = {"successstatus": "error", "message": "no review available"}
#                         print(responsedata)
#                         return Response(responsedata)
#
#                     rs=ReviewSerializer(r,many=True)
#
#
#             responsedata={"successstatus":"ok","reviews":rs.data}
#
#             print(responsedata)
#             return  Response(responsedata)
#
#
#         except UserSession.DoesNotExist:
#             responsedata = {"successstatus": "error","message": "Please Login To Continue"}
#             print(responsedata)
#             return Response(responsedata)
#         except UserDetail.DoesNotExist:
#             if userstat==0:
#                 responsedata={"successstatus":"error","message":"the user doesnot exists"}
#
#             elif userstat==2:
#                 responsedata = {"successstatus": "error", "message": "the user doesnot exists"}
#
#             print(responsedata)
#             return Response(responsedata)
#
#         except ItemMap.DoesNotExist:
#
#             responsedata = {"successstatus": "error", "message": "the Item you are requesting is not available any more"}
#             print(responsedata)
#             return  Response(responsedata)
#
#
#
#         except Exception as e:
#
#
#             print("error occured in outer except GetMessage ")
#             print("error : ",e)
#             responsedata={"successstatus":"error","message":"error occured trying to request the item"}
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print(True, exc_type, fname, exc_tb.tb_lineno)
#             return  Response(responsedata)
#
#
#









class GetMyItemHistory(APIView):
    def post(self,request):
        responsedata = {}
        requestdata = {}
        try:

            for key in request.POST:
                requestdata[key] = request.POST[key].strip()

            print(requestdata)

            if ((not requestdata['id']) or (not requestdata['user_session_key'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get items data : ", requestdata)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud):
                            try:


                                if(ud.user_type==0):
                                    cr = ItemOrderHistory.objects.filter(serviceprovider_id=ud.id).order_by("-booked_time")
                                else:
                                    cr = ItemOrderHistory.objects.filter(user_id=ud.id).order_by("-booked_time")

                                scr=ItemOrderHistorySerializer(cr,many=True)

                                responsedata = {"successstatus": "ok", "history":scr.data}
                                print(responsedata)
                                return Response(responsedata)

                            except OrderHistory.DoesNotExist:
                                responsedata = {"successstatus": "error","messsage": 'No history availabe for you with given details'}
                                print(responsedata)
                                return Response(responsedata)

                    except Exception as e:
                        responsedata = {"successstatus": "error", "message": "Unknown error occured"}
                        print(responsedata)
                        print("Error occured : ", e)
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(True, exc_type, fname, exc_tb.tb_lineno)
                        return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except Exception as e:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in get order history : outer except : ", responsedata)
            print("Error : ", e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)


class GetMySingleItemHistory(APIView):
    def post(self,request):
        responsedata = {}
        requestdata = {}
        try:

            for key in request.POST:
                requestdata[key] = request.POST[key].strip()

            print(requestdata)

            if ((not requestdata['id']) or (not requestdata['user_session_key']) or (not requestdata['history_id'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get items data : ", requestdata)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud):
                            try:


                                if(ud.user_type==0):
                                    cr = ItemOrderHistory.objects.get(serviceprovider_id=ud.id,id=int(requestdata['history_id']))#.order_by("-booked_time")
                                else:
                                    cr = ItemOrderHistory.objects.get(user_id=ud.id,id=int(requestdata['history_id']))#.order_by("-booked_time")

                                scr=ItemOrderHistorySerializer(cr)

                                tdata=scr.data
                                tdata["user_name"]=cr.user_ref.full_name
                                tdata["provider_name"]=cr.serviceprovider_ref.full_name
                                #tdata["item_detail"]=cr.item_request_ref.item_map_ref.item_details
                                tdata["item_name"]=cr.item_request_ref.item_map_ref.item_name

                                responsedata = {"successstatus": "ok", "history":tdata}


                                responsedata = {"successstatus": "ok", "history":tdata}
                                print(responsedata)
                                return Response(responsedata)

                            except ItemOrderHistory.DoesNotExist:
                                responsedata = {"successstatus": "error","messsage": 'No history availabe for you with given details'}
                                print(responsedata)
                                return Response(responsedata)

                    except Exception as e:
                        responsedata = {"successstatus": "error", "message": "Unknown error occured"}
                        print(responsedata)
                        print("Error occured : ", e)
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(True, exc_type, fname, exc_tb.tb_lineno)
                        return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except Exception as e:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in get order history : outer except : ", responsedata)
            print("Error : ", e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)



class GetMySingleHistory(APIView):
    def post(self,request):
        responsedata = {}
        requestdata = {}
        try:

            for key in request.POST:
                requestdata[key] = request.POST[key].strip()

            print(requestdata)

            if ((not requestdata['id']) or (not requestdata['user_session_key']) or (not requestdata['history_id'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get items data : ", requestdata)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud):
                            try:


                                if(ud.user_type==0):
                                    cr = OrderHistory.objects.get(serviceprovider_id=ud.id,id=int(requestdata['history_id']))#.order_by("-booked_time")
                                else:
                                    cr = OrderHistory.objects.get(user_id=ud.id,id=int(requestdata['history_id']))#.order_by("-booked_time")

                                scr=OrderHistorySerializer(cr)

                                tdata=scr.data
                                tdata["user_name"]=cr.user_ref.full_name
                                tdata["provider_name"]=cr.serviceprovider_ref.full_name
                                tdata["userrequest_detail"]=cr.service_request_ref.request_detail
                                tdata["service_name"]=cr.service_request_ref.service_map_ref.service_name

                                responsedata = {"successstatus": "ok", "history":tdata}
                                print(responsedata)
                                return Response(responsedata)

                            except OrderHistory.DoesNotExist:
                                responsedata = {"successstatus": "error","messsage": 'No history availabe for you with given details'}
                                print(responsedata)
                                return Response(responsedata)

                    except Exception as e:
                        responsedata = {"successstatus": "error", "message": "Unknown error occured"}
                        print(responsedata)
                        print("Error occured : ", e)
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(True, exc_type, fname, exc_tb.tb_lineno)
                        return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except Exception as e:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in get order history : outer except : ", responsedata)
            print("Error : ", e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)





class SetItemBudget(APIView):

    def post(self, request):

        responsedata = {}
        getservice_data = {}

        try:

            for key in request.POST:
                getservice_data[key] = request.POST[key].strip()

            print("get my single request : ", getservice_data)

            if ((not getservice_data['id']) or (not getservice_data['user_session_key']) or (not getservice_data['request_id']) or (not getservice_data['budget'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get services data : ", getservice_data)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud):
                            try:
                                print("ud id : ", ud.id)
                                print("request id : ", getservice_data['request_id'])
                                if (ud.user_type == 0):
                                    sr = ItemRequest.objects.get(serviceprovider_id=ud.id,id=int(getservice_data['request_id']))#.order_by("-request_time")
                                else:
                                    sr = ItemRequest.objects.get(user_id=ud.id,id=int(getservice_data['request_id']))#.order_by("-request_time")



                                if (sr):
                                    sr.final_budget=float(getservice_data['budget'])

                                    sr.save()
                                    # try:
                                    #     rud = UserDetail.objects.get(id=sr.user_id)
                                    # except Exception as e:
                                    #     responsedata={"successstatus":"error","messgae":"could not get requester's details"}
                                    #     print("response data : ",responsedata)
                                    #     print("Error occured : ",e)
                                    #     return Response(responsedata)


                                    # print("sm : ",sm)
                                    #print("final data : ",tdata)

                                    responsedata = {"successstatus": "ok", "message": "budget has been set"}

                                    return Response(responsedata)

                                else:
                                    responsedata = {"successstatus": "error", "message": "No request Available"}
                                    print(responsedata)
                                    return Response(responsedata)



                            # except ServiceMap.DoesNotExist:
                            #     responsedata = {"successstatus": "error", "message": "No request Available"}
                            #     print(responsedata)
                            #     return Response(responsedata)
                            except ItemRequest.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "No request Available"}
                                print(responsedata)
                                return Response(responsedata)


                        else:
                            responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                            print(responsedata)
                            return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except Exception as e:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in outer except : ", responsedata)
            print("Error : ", e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)



















class SetItemPaid(APIView):

    def post(self, request):

        responsedata = {}
        getservice_data = {}

        try:

            for key in request.POST:
                getservice_data[key] = request.POST[key].strip()

            print("get my single request : ", getservice_data)

            if ((not getservice_data['id']) or (not getservice_data['user_session_key']) or (not getservice_data['request_id']) or (not getservice_data['payment_state']) or (not getservice_data['payment_id']) or (not getservice_data['payment_time'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            print("get services data : ", getservice_data)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us):

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud):
                            try:
                                print("ud id : ", ud.id)
                                print("request id : ", getservice_data['request_id'])
                                # if (ud.user_type == 0):
                                #     sr = ItemRequest.objects.get(serviceprovider_id=ud.id,id=int(getservice_data['request_id']))#.order_by("-request_time")
                                # else:
                                #     sr = ItemRequest.objects.get(user_id=ud.id,id=int(getservice_data['request_id']))#.order_by("-request_time")
                                sr = ItemRequest.objects.get(user_id=ud.id, id=int(getservice_data['request_id']))  # .order_by("-request_time")


                                if (sr):
                                    sr.payment_state=getservice_data['payment_state']
                                    sr.payment_id=getservice_data['payment_id']
                                    sr.payment_time=getservice_data['payment_time']
                                    sr.service_status=2
                                    sr.paid=True


                                    sr.save()

                                else:
                                    responsedata = {"successstatus": "error", "message": "No request Available"}
                                    print(responsedata)
                                    return Response(responsedata)

                                sh = ItemOrderHistory.objects.get(user_id=ud.id, item_request_id=int(getservice_data['request_id']))  # .order_by("-request_time")

                                if (sh):
                                    sh.payment_state = getservice_data['payment_state']
                                    sh.payment_id = getservice_data['payment_id']
                                    sh.payment_time = getservice_data['payment_time']
                                    sh.service_status=2
                                    sh.paid = True

                                    sh.save()

                                else:
                                    responsedata = {"successstatus": "error", "message": "No History Available"}
                                    print(responsedata)
                                    return Response(responsedata)

                                responsedata={"successstatus":"ok","message":"payment details updated successfully"}
                                print(responsedata)
                                return  Response(responsedata)




                            # except ServiceMap.DoesNotExist:
                            #     responsedata = {"successstatus": "error", "message": "No request Available"}
                            #     print(responsedata)
                            #     return Response(responsedata)
                            except ItemRequest.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "No request Available"}
                                print(responsedata)
                                return Response(responsedata)
                            except ItemOrderHistory.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "No history Available"}
                                print(responsedata)
                                return Response(responsedata)


                        else:
                            responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                            print(responsedata)
                            return Response(responsedata)

                    except UserDetail.DoesNotExist:

                        responsedata = {"successstatus": "error", "message": "User Does Not Exist"}
                        print(responsedata)
                        return Response(responsedata)


            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
                except:
                    pass
                responsedata = {"successstatus": "error", "message": "You are not logged in"}
                return Response(responsedata)


        except Exception as e:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in outer except : ", responsedata)
            print("Error : ", e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(True, exc_type, fname, exc_tb.tb_lineno)
            return Response(responsedata)





