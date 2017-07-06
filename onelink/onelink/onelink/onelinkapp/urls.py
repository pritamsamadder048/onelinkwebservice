"""onelink URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . import views


#from rest_framework.urlpatterns import format_suffix_patterns




urlpatterns = [



    url(r'^stock/$', views.StockList.as_view(),name="stocklist"),

    url(r'^registeruser/$', views.RegisterUser.as_view(),name="registeruser"),
    url(r'^updateuser/$', views.UpdateUser.as_view(),name="updateuser"),
    url(r'^login/$', views.Login.as_view(),name="login"),
    url(r'^logout/$', views.Logout.as_view(),name="logout"),
    url(r'^verifyuser/(?P<userid>[0-9]+)/(?P<vkey>[a-zA-Z0-9]+)/$', views.verifyuser,name="verifyuser"),
    url(r'^getsurvicecategory/$', views.GetServiceCategory.as_view(),name="getservicecategory"),
    url(r'^getproductcategory/$', views.GetProductCategory.as_view(),name="getproductcategory"),
    url(r'^getsurvicesubcategory/(?P<serviceid>[0-9]+)/$', views.GetServiceSubCategory.as_view(),name="getservicesubcategory"),

    url(r'^getmyservices/$', views.GetMyServices.as_view(),name="getmyservices"),
    url(r'^getmysingleservice/$', views.GetMySingleService.as_view(),name="getmysingleservice"),



    url(r'^registerservice/$', views.RegisterService.as_view(),name="registerservice"),
    url(r'^updateservice/$', views.UpdateService.as_view(),name="updateservice"),
    url(r'^deleteservice/$', views.DeleteService.as_view(),name="deleteservice"),


    url(r'^getmyrequests/$', views.GetMyRequests.as_view(),name="getmyrequests"),
    url(r'^getmyquickrequests/$', views.GetMyQuickRequests.as_view(),name="getmyquickrequests"),
    url(r'^getmysinglerequest/$', views.GetMySingleRequest.as_view(),name="getmysinglerequest"),
    url(r'^getmyitemrequests/$', views.GetMyItemRequests.as_view(),name="getmyitemrequests"),
    url(r'^getmysingleitemrequest/$', views.GetMySingleItemRequest.as_view(),name="getmysingleitemrequest"),


    url(r'^additem/$', views.AddItem.as_view(),name="additem"),
    url(r'^updateitem/$', views.UpdateItem.as_view(),name="updateitem"),
    url(r'^deleteitem/$', views.DeleteItem.as_view(),name="deleteitem"),
    url(r'^getmyitems/$', views.GetMyItems.as_view(),name="getmyitems"),
    url(r'^getitembycategory/(?P<catid>[0-9]+)/$', views.GetItemByCategory.as_view(),name="getitembycategory"),
    url(r'^getitembyid/(?P<itemid>[0-9]+)/$', views.GetItemById.as_view(),name="getitembyid"),



    url(r'^getproviderslist/(?P<serviceid>[0-9]+)/(?P<areapincodes>.+)/$', views.GetProvidersList.as_view(),name="getproviderslist"),
    url(r'^getsingleservice/(?P<serviceid>[0-9]+)/$', views.GetSingleService.as_view(),name="getsingleservice"),

    url(r'^requestservice/$', views.RequestService.as_view(),name="requestservice"),

    url(r'^requestquickservice/$', views.RequestQuickService.as_view(),name="requestquickservice"),

    url(r'^getmynotifications/$', views.GetMyNotifications.as_view(),name="getmynotifications"),

    url(r'^addtofavouriteservice/$', views.AddToFavouriteService.as_view(),name="addtofavouriteservice"),
    url(r'^getfavouriteservices/$', views.GetFavouriteServices.as_view(),name="getfavouriteservices"),
    url(r'^removefavouriteservice/$', views.RemoveFavouriteService.as_view(),name="removefavouriteservice"),
    url(r'^isinfavourite/$', views.IsInFavourite.as_view(),name="isinfavourite"),


    url(r'^getpincode/(?P<lan>\d+\.\d+)/(?P<lat>\d+\.\d+)/$', views.GetPincode.as_view(),name="getpincode"),

    url(r'^confirmrequest/$', views.ConfirmRequest.as_view(),name="confirmrequest"),
    url(r'^confirmitemrequest/$', views.ConfirmItemRequest.as_view(),name="confirmitemrequest"),
    url(r'^getmyhistory/$', views.GetMyHistory.as_view(),name="getmyhistory"),
    url(r'^getmysinglehistory/$', views.GetMySingleHistory.as_view(),name="getmysinglehistory"),

    url(r'^getmyitemhistory/$', views.GetMyItemHistory.as_view(),name="getmyitemhistory"),
    url(r'^getmysingleitemhistory/$', views.GetMySingleItemHistory.as_view(),name="getmysingleitemhistory"),



    url(r'^requestproduct/$', views.RequestProduct.as_view(),name="requestproduct"),
    url(r'^sendmessage/$', views.SendMessage.as_view(),name="sendmessage"),
    url(r'^getmessages/$', views.GetMessages.as_view(),name="getmessages"),



    url(r'^writereview/$', views.WriteReview.as_view(),name="writereview"),
    url(r'^setitembudget/$', views.SetItemBudget.as_view(),name="setitembudget"),




    url(r'^setitempaid/$', views.SetItemPaid.as_view(),name="setitempaid"),
    url(r'^updatestatus/$', views.UpdateStatus.as_view(),name="updatestatus"),








    #url(r'^GetMyReviews/$', views.GetMyReviews.as_view(),name="getmyreviews"),






]

