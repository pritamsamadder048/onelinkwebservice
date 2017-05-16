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
    url(r'^login/$', views.Login.as_view(),name="login"),
    url(r'^logout/$', views.Logout.as_view(),name="logout"),
    url(r'^verifyuser/(?P<userid>[0-9]+)/(?P<vkey>[a-zA-Z0-9]+)/$', views.verifyuser,name="verifyuser"),
    url(r'^getsurvicecategory/$', views.GetServiceCategory.as_view(),name="getservicecategory"),
    url(r'^getsurvicesubcategory/(?P<serviceid>[0-9]+)/$', views.GetServiceSubCategory.as_view(),name="getservicesubcategory"),
    url(r'^getmyservices/$', views.GetMyServices.as_view(),name="getmyservices"),
    url(r'^getmysingleservice/$', views.GetMySingleService.as_view(),name="getmysingleservice"),


    url(r'^registerservice/$', views.RegisterService.as_view(),name="registerservice"),
    url(r'^updateservice/$', views.UpdateService.as_view(),name="updateservice"),
    url(r'^deleteservice/$', views.DeleteService.as_view(),name="deleteservice"),

    url(r'^additem/$', views.AddItem.as_view(),name="additem"),
    url(r'^updateitem/$', views.UpdateItem.as_view(),name="updateitem"),


    url(r'^getproviderslist/(?P<serviceid>[0-9]+)/(?P<areapincode>[0-9]+)/$', views.GetProvidersList.as_view(),name="getproviderslist"),
    url(r'^getsingleprovider/(?P<serviceid>[0-9]+)/$', views.GetSingleProvider.as_view(),name="getsingleprovider"),
]

