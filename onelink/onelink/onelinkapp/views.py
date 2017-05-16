from django.shortcuts import render


from django.http import HttpResponse



import datetime





from  django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import  Response
from  rest_framework import  status
from rest_framework import generics
from rest_framework import views



import json
import sys,os


from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
from django.core.mail import EmailMessage

import math

from onelink.settings import GMAIL_DETAIL
from .models import generate_hash
from onelink import settings






from .models import Stock
from .serializers import StockSerializer

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
                if ( (not signup_data['email']) or (not signup_data['name'])  or (not signup_data['password'])or (not signup_data['mobile']) or (not signup_data['pincode']) or (not signup_data['address']) or (not signup_data['user_type'])):

                    #print("not all data",responsedata)

                    print(signup_data)

                    responsedata={"successstatus":"error","message":"please provide all the details necessary"}

                    return Response(responsedata)
            except:

                #print("not all data except ","   ", responsedata)

                print(signup_data)

                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                return Response(responsedata)


            try:
                ud = UserDetail.objects.get(email=signup_data['email'])
                if (ud):
                    responsedata={"successstatus":"error","message":"the email id is already registered.Please login ."}
                    return Response(responsedata)

            except UserDetail.DoesNotExist:

                pass


            try:


                print("in block")

                ud = UserDetail()
                print("init")
                ud.full_name = signup_data['name']

                ud.email = signup_data['email']
                ud.mobile = signup_data['mobile']
                ud.pincode=signup_data["pincode"]
                ud.address=signup_data["address"]
                ud.user_type = signup_data['user_type']

                ud.set_password(signup_data['password'])

                print("trying to save data")

                ud.save()

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
                    ud = UserDetail.objects.get(
                        id=us.UserDetail_ref.id)  # also can b done like##### ud = us.UserDetail_ref
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
                        del request.session['username']
                    except:
                        pass
                    try:
                        us.delete()
                    except:
                        pass
            except UserSession.DoesNotExist:
                try:
                    del request.session['username']
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
            if((not login_data['email']) or (not login_data['password'])):


                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print("if not data",responsedata)
                return Response(responsedata)

        except:

            responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
            print("except not data", responsedata)
            return Response(responsedata)

        try:
            ud = UserDetail.objects.get(email=login_data['email'])
            # bodytext+="<p>user data available</p>"

            correctpassword = ud.check_password(login_data['password'])
            # bodytext+="<p>"+str(correctpassword)+"</p>"

            if (correctpassword):

                try:
                    print("correct password")
                    us = UserSession.objects.get(email=ud.email)
                    uskey = us.UserSession_key
                    request.session['user_session_key'] = uskey

                    responsedata={"userid":ud.id,"user_type":ud.user_type,"areapincode":ud.pincode,'user_session_key':us.UserSession_key}
                    print("after correct ",responsedata)

                    return Response(responsedata)

                except:
                    try:
                        us.delete()
                    except:
                        pass

                us = UserSession()
                us.full_name = ud.full_name
                us.email = ud.email
                us.User_Type=ud.user_type
                us.set_sessionkey()
                uskey = us.UserSession_key  # session key for the user
                us.UserDetail_id = ud.id
                us.UserDetail_ref = ud
                us.save()
                request.session['user_session_key'] = uskey

                responsedata = {"userid": ud.id,"user_type":ud.user_type,"areapincode":ud.pincode , 'user_session_key': us.UserSession_key}
                print("New Login : ",responsedata)
                return Response(responsedata)
            else:
                responsedata={"successsatus":"error","message":"User name and password does not match"}
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


            if((not registerservice_data['service_category_id']) or (not registerservice_data['serviceprovider_id']) or (not registerservice_data['service_name']) or (not registerservice_data['service_details']) or (not registerservice_data['areapincode'])):
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
                                print("service_details : ",sm.service_details)
                                sm.serviceprovider_email=ud.email
                                sm.service_category_id=registerservice_data['service_category_id']
                                sm.service_ref = sc
                                sm.areapincode=registerservice_data['areapincode']

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



            if((not updateservice_data['serviceprovider_id']) or (not updateservice_data['service_name']) or (not updateservice_data['areapincode']) or (not updateservice_data['servicemapid']) or (not updateservice_data['service_details']) ):
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
                                sm.serviceprovider_id=updateservice_data['serviceprovider_id']
                                sm.service_name=updateservice_data['service_name']
                                sm.service_details = updateservice_data['service_details']
                                sm.serviceprovider_email=ud.email
                                #sm.service_category_id=updateservice_data['service_category_id']
                                #sm.service_ref = sc
                                sm.areapincode=updateservice_data['areapincode']

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

                        ud=UserDetail(id=us.UserDetail_id)
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

                        ud=UserDetail(id=us.UserDetail_id)
                        if(ud):
                            try:
                                sm = ServiceMap.objects.filter(serviceprovider_id=int(getservice_data['id']))

                                if (sm):
                                    ssm = ServiceMapSerializer(sm, many=True)
                                    print(Response(ssm.data))
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

                        ud = UserDetail(id=us.UserDetail_id)
                        if (ud):
                            try:
                                sm = ServiceMap.objects.get(id=int(getservice_data["service_id"]))

                                if (sm):
                                    ssm = ServiceMapSerializer(sm)
                                    print(ssm.data)
                                    return Response(ssm.data)

                                else:
                                    responsedata = {"successstatus": "error",
                                                    "message": "No Services Available"}
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


############################################################################################################################
###########################################  Item Section ##################################################################



class AddItem(APIView):

    def post(self,request):

        responsedata = {}
        additem_data={}

        try:

            for key in request.POST:
                additem_data[key] = request.POST[key].strip()


            if((not additem_data['serviceprovider_id']) or (not additem_data['item_name']) or (not additem_data['item_details']) or (not additem_data['service_category_id'])    or (not request.FILES['item_image'])  or (not additem_data['item_MRP'])  or (not additem_data['item_SLP'])  or (not additem_data['item_features']) ):
                responsedata={"successstatus":"error","message":"please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)


            additem_data['item_image']=request.FILES['item_image']
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
                                sc = ServiceCategory.objects.get(id=int(additem_data['service_category_id']))

                                im = ItemMap()
                                im.serviceprovider_id=additem_data['serviceprovider_id']
                                im.service_name=additem_data['item_name']
                                im.service_details=additem_data['item_details']
                                im.serviceprovider_email=ud.email
                                im.service_category_id=int(additem_data['service_category_id'])
                                im.service_ref=sc
                                im.item_image=additem_data['item_image']
                                #im.areapincode=additem_data['areapincode']
                                im.item_features=additem_data['item_features']
                                im.item_MRP=additem_data['item_MRP']
                                im.item_SLP=additem_data['item_SLP']


                                im.save()

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


        except:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in outer except : ",responsedata)
            return Response(responsedata)



class UpdateItem(APIView):

    def post(self, request):

        responsedata = {}
        updateitem_data = {}

        try:

            for key in request.POST:
                updateitem_data[key] = request.POST[key].strip()

            if ((not updateitem_data['itemmap_id']) or (not updateitem_data['serviceprovider_id']) or (not updateitem_data['item_name']) or (not updateitem_data['service_category_id']) or (not updateitem_data['item_details'])  or (not request.FILES['item_image']) or (not updateitem_data['item_MRP']) or (not updateitem_data['item_SLP']) or (not updateitem_data['item_features'])):
                responsedata = {"successstatus": "error", "message": "please provide all the details necessary"}
                print(responsedata)
                return Response(responsedata)

            updateitem_data['item_image']=request.FILES['item_image']
            print("Register service data : ", updateitem_data)

            if (request.session.has_key('user_session_key')):
                sesskey = request.session['user_session_key']
            else:
                sesskey = request.POST['user_session_key']
                print("sess key ", sesskey)

            try:
                us = UserSession.objects.get(UserSession_key=sesskey)
                if (us.User_Type == 0):
                    print("correct user")

                    try:

                        ud = UserDetail.objects.get(id=us.UserDetail_id)
                        if (ud):

                            if (not ud.user_type == 0):
                                responsedata = {"successstatus": "error",
                                                "message": "you are not registered as a service provider"}
                                print(responsedata)
                                return Response(responsedata)

                            try:
                                sc = ServiceCategory.objects.get(id=int(updateitem_data['service_category_id']))

                                im = ItemMap.objects.get(id=int(updateitem_data['itemmap_id']))
                                im.serviceprovider_id = updateitem_data['serviceprovider_id']
                                im.service_category_id = int(updateitem_data['service_category_id'])
                                im.service_ref = sc
                                im.service_name = updateitem_data['item_name']
                                im.service_details = updateitem_data['item_details']
                                im.serviceprovider_email = ud.email
                                im.item_image = updateitem_data['item_image']
                                #im.areapincode = updateitem_data['areapincode']
                                im.item_features = updateitem_data['item_features']
                                im.item_MRP = updateitem_data['item_MRP']
                                im.item_SLP = updateitem_data['item_SLP']

                                im.save()

                                responsedata = {"successstatus": "ok",
                                                "message": "You have successfully registered your service"}
                                return Response(responsedata)

                            except ServiceMap.DoesNotExist:
                                responsedata = {"successstatus": "error", "message": "No Services Available"}
                                print(responsedata)
                                return Response(responsedata)

                            except ServiceCategory.DoesNotExist:
                                responsedata = {"successstatus": "error",
                                                "message": "Service category not available"}
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


        except:

            responsedata = {"successstatus": "error", "message": "Unknown Error"}
            print("in outer except : ", responsedata)
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

                        ud = UserDetail(id=us.UserDetail_id)
                        if (ud):
                            try:
                                im = ItemMap.objects.get(id=int(deleteitem_data['item_id']),
                                                            serviceprovider_id=ud.id)

                                if (im):
                                    try:
                                        im.delete()
                                        responsedata = {"successstatus": "ok",
                                                        "message": "successfully deleted the item"}
                                        print(responsedata)
                                        return Response(responsedata)
                                    except:
                                        responsedata = {"successstatus": "error",
                                                        "message": "could not delete service try again later"}
                                        return Response(responsedata)


                                else:
                                    responsedata = {"successstatus": "error",
                                                    "message": "No Services Available"}
                                    print(responsedata)
                                    return Response(responsedata)



                            except ItemMap.DoesNotExist:
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

                        ud = UserDetail(id=us.UserDetail_id)
                        if (ud):
                            try:
                                im = ItemMap.objects.filter(serviceprovider_id=int(getitem_data['id']))

                                if (im):
                                    sim = ItemMapSerializer(im, many=True)
                                    print("Items : ",sim.data)
                                    return Response(sim.data)

                                else:
                                    responsedata = {"successstatus": "error",
                                                    "message": "No Services Available"}
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
            print("in getmyitems : outer except : ", responsedata)
            return Response(responsedata)





##############################################################################################################################
####################################### Normal user section ##################################################################

class GetProvidersList(APIView):
    def get(self,request,serviceid,areapincode):
        responsedata={}

        if((not serviceid) or (not areapincode)):
            print("not all data in getproviderslist")
            responsedata={"successstatus":"error","message":"please procvide all the details necessary"}
            print("in get providers list : ",responsedata)
            return  Response(responsedata)

        try:
            sm = ServiceMap.objects.filter(service_category_id=int(serviceid),areapincode=int(areapincode))
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



class GetSingleProvider(APIView):
    def get(self,request,serviceid):
        responsedata={}

        if((not serviceid)):
            print("not all data in getproviderslist")
            responsedata={"successstatus":"error","message":"please procvide all the details necessary"}
            print("in get providers list : ",responsedata)
            return  Response(responsedata)

        try:

            sm = ServiceMap.objects.get(service_category_id=int(serviceid))
            if (sm):
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
            return  Response(responsedata)



