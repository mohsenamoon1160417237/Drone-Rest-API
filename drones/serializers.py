from rest_framework import serializers
from .models import (DroneCategory,
					 Drone,
					 Pilot,
					 Competition
					 )
from django.contrib.auth.models import User





class DroneCategorySerializer(serializers.HyperlinkedModelSerializer):

	drones = serializers.HyperlinkedRelatedField(many=True , read_only=True , view_name='drone-detail')


	class Meta:

		model = DroneCategory
		fields = ['url' , 'pk' , 'drones' , 'name']




class DroneSerializer(serializers.HyperlinkedModelSerializer):

	category = serializers.SlugRelatedField(queryset=DroneCategory.objects.all() , slug_field='name')
	owner = serializers.ReadOnlyField(source='owner.username')


	class Meta:

		model = Drone
		fields = ['url' , 'pk' , 'category' , 'name' , 'has_it_competed' , 'insert_time' , 'owner']





class CompetitionSerializer(serializers.HyperlinkedModelSerializer):

	drone = DroneSerializer()

	class Meta:

		model = Competition
		fields = ['url' , 'pk' , 'pilot' , 'drone' ]




class PilotSerializer(serializers.HyperlinkedModelSerializer):


	gender = serializers.ChoiceField(choices=Pilot.GENDER)
	competitions = CompetitionSerializer(many=True , read_only=True)


	class Meta:

		model = Pilot
		fields = ['url' , 'pk' , 'gender' , 'name' , 'competitions']




class PilotDroneSerializer(serializers.HyperlinkedModelSerializer):

	pilot = serializers.SlugRelatedField(queryset=Pilot.objects.all() , slug_field='name')
	drone = serializers.SlugRelatedField(queryset=Drone.objects.all() , slug_field='name')

	class Meta:

		model = Competition
		fields = ['url' , 'pk' , 'drone' , 'pilot']




class UserDroneSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:

		model = Drone
		fields = ['url' , 'name']





class UserSerializer(serializers.HyperlinkedModelSerializer):

	drones = UserDroneSerializer(many=True , read_only=True)

	class Meta:

		model = User
		fields = ['url' , 'pk' , 'drones' , 'username']











