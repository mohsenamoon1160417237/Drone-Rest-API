from django.db import models
from django.contrib.auth.models import User



class DroneCategory(models.Model):

	name = models.CharField(max_length=100 , unique=True)

	class Meta:

		ordering = ['name']

	def __str__(self):

		return self.name




class Drone(models.Model):

	name = models.CharField(max_length=100 , unique=True)
	category = models.ForeignKey(DroneCategory , on_delete=models.CASCADE , related_name='drones')
	has_it_competed = models.BooleanField(default=False)
	insert_time = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User , on_delete=models.CASCADE , related_name='drones')

	class Meta:

		ordering = ['name']

	def __str__(self):

		return self.name




class Pilot(models.Model):

	Male = 'M'
	Female = 'F'
	GENDER = [

	(Male , 'Female'),
	(Female , 'Male')
	]

	name = models.CharField(max_length=100 , unique=True)
	gender = models.CharField(choices=GENDER , max_length=100 , default='M')

	class Meta:

		ordering = ['name']

	def __str__(self):

		return self.name




class Competition(models.Model):

	pilot 			 = models.ForeignKey(Pilot , on_delete=models.CASCADE , related_name='competitions')
	drone 			 = models.ForeignKey(Drone , on_delete=models.CASCADE , related_name='competitions')

	def __str__(self):

		return '{} : {}'.format(self.pilot , self.drone)



