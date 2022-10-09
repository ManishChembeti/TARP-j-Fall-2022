from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('Login.html', views.Login, name="Login"), 
	       path('UserLogin', views.UserLogin, name="UserLogin"),
	       path('AddEquipment.html', views.AddEquipment, name="AddEquipment"), 
	       path('AddEquipmentAction', views.AddEquipmentAction, name="AddEquipmentAction"),
	       path('AddLogistic.html', views.AddLogistic, name="AddLogistic"), 
	       path('AddLogisticAction', views.AddLogisticAction, name="AddLogisticAction"),
	       path('ViewEquipmentDetails.html', views.ViewEquipmentDetails, name="ViewEquipmentDetails"),
	       path('ViewLogisticDetails.html', views.ViewLogisticDetails, name="ViewLogisticDetails"),
	       path('ViewDistributionDetails.html', views.ViewDistributionDetails, name="ViewDistributionDetails"),
	       path('AddDistribution.html', views.AddDistribution, name="AddDistribution"), 
	       path('AddDistributionAction', views.AddDistributionAction, name="AddDistributionAction"),
	       path('ViewSupervisionDetails.html', views.ViewSupervisionDetails, name="ViewSupervisionDetails"),
	       path('AddSupervision.html', views.AddSupervision, name="AddSupervision"), 
	       path('AddSupervisionAction', views.AddSupervisionAction, name="AddSupervisionAction"),
	       
]