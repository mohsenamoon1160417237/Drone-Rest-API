from django.urls import path
from . import views


urlpatterns = [

	path('drone-categories/' , views.DroneCategoryList.as_view(),
		 name=views.DroneCategoryList.name),

	path('drone-category/<pk>/' , views.DroneCategoryDetail.as_view(),
		  name=views.DroneCategoryDetail.name),

	path('drones/' , views.DroneList.as_view(),
		  name=views.DroneList.name),

	path('drone/<pk>/' , views.DroneDetail.as_view(),
		  name=views.DroneDetail.name),

	path('pilots/' , views.PilotList.as_view(),
		  name=views.PilotList.name),

	path('pilot/<pk>/' , views.PilotDetail.as_view(),
		  name=views.PilotDetail.name),

	path('competitions/' , views.CompetitionList.as_view(),
		  name=views.CompetitionList.name),

	path('competition/<pk>/' , views.CompetitionDetail.as_view(),
		  name=views.CompetitionDetail.name),

	path('' , views.ApiRoot.as_view(), name=views.ApiRoot.name),


]