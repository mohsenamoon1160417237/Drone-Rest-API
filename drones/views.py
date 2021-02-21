from django.shortcuts import render
from .serializers import (DroneCategorySerializer,
						  DroneSerializer,
						  CompetitionSerializer,
						  PilotSerializer,
						  PilotDroneSerializer
						  )
from rest_framework import generics , permissions
from rest_framework.response import Response
from .models import (DroneCategory,
				     Drone,
				     Pilot,
				     Competition
				     )
from rest_framework.reverse import reverse
from django_filters import AllValuesFilter , DateTimeFilter , NumberFilter , FilterSet
from . import custompermission
from rest_framework.permissions import IsAuthenticated , IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import ScopedRateThrottle , AnonRateThrottle , UserRateThrottle





class DroneCategoryList(generics.ListCreateAPIView):

	name = 'dronecategory-list'
	serializer_class = DroneCategorySerializer
	queryset = DroneCategory.objects.all()

	filter_fields = ['name']
	search_fields  = ['^name']
	ordering_fields = ['name']




class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView):

	name = 'dronecategory-detail'
	serializer_class = DroneCategorySerializer
	queryset = DroneCategory.objects.all()




class DroneList(generics.ListCreateAPIView):

	name = 'drone-list'
	serializer_class = DroneSerializer
	queryset = Drone.objects.all()

	filter_fields = [

		'name',
		'category',
		'has_it_competed',
		'insert_time'
	]

	search_fields = [

		'^name'
	]

	ordering_fields = [

		'name',
		'insert_time'
	]

	permission_classes = [IsAuthenticatedOrReadOnly,
						  custompermission.IsValidUser]


	throttle_scope = 'drones'
	throttle_classes = [ScopedRateThrottle , AnonRateThrottle]


	def perform_create(self , serializer):

		serializer.save(owner=self.request.user)




class DroneDetail(generics.RetrieveUpdateDestroyAPIView):

	name = 'drone-detail'
	serializer_class = DroneSerializer
	queryset = Drone.objects.all()

	
	permission_classes = [IsAuthenticatedOrReadOnly,
						  custompermission.IsCurrentUserOwnerOrReadOnly]

	throttle_scope = 'drones'
	throttle_classes = [ScopedRateThrottle , AnonRateThrottle]



class PilotList(generics.ListCreateAPIView):

	name = 'pilot-list'
	serializer_class = PilotSerializer
	queryset = Pilot.objects.all()

	filter_fields = [

		'name',
		'gender'
	]

	search_fields = [

		'^name'
	]

	ordering_fields = [

		'name'
	]

	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	throttle_scope = 'pilots'
	throttle_classes = [ScopedRateThrottle , AnonRateThrottle]




class PilotDetail(generics.RetrieveUpdateDestroyAPIView):

	name = 'pilot-detail'
	serializer_class = PilotSerializer
	queryset = Pilot.objects.all()

	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	throttle_scope = 'pilots'
	throttle_classes = [ScopedRateThrottle , AnonRateThrottle]




class CompetitionFilters(FilterSet):

	from_achievement_date = DateTimeFilter(field_name='achievement_date' , lookup_expr='gte')
	to_achievement_date   = DateTimeFilter(field_name='distance_achievement_date' , lookup_expr='lte')
	min_distance_in_feet  = NumberFilter(field_name='distance_in_feet' , lookup_expr='gte')
	max_distance_in_feet  = NumberFilter(field_name='distance_in_feet' , lookup_expr='lte')
	drone_name            = AllValuesFilter(field_name='drone__name')
	pilot_name            = AllValuesFilter(field_name='pilot__name')


	class Meta:

		model = Competition
		fields = [

			'min_distance_in_feet',
			'max_distance_in_feet',
			'from_achievement_date',
			'to_achievement_date',
			'drone_name',
			'pilot_name'
		]





class CompetitionList(generics.ListCreateAPIView):

	name = 'competition-list'
	serializer_class = PilotDroneSerializer
	queryset = Competition.objects.all()
	filter_class = CompetitionFilters
	ordering_fields = [
		'achievement_date',
		'distance_in_feet'
	]





class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):

	name = 'competition-detail'
	serializer_class = PilotDroneSerializer
	queryset = Competition.objects.all() 




class ApiRoot(generics.GenericAPIView):

	name = 'api-root'

	def get(self , request , *args , **kwargs):
		return Response({

			'drone-categories' : reverse(DroneCategoryList.name , request=request),
			'drones' : reverse(DroneList.name , request=request),
			'pilots' : reverse(PilotList.name , request=request),
			'competitions' : reverse(CompetitionList.name , request=request)
			})




