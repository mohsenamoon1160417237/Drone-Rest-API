from rest_framework import permissions
from django.contrib.auth.models import User



class IsCurrentUserOwnerOrReadOnly(permissions.BasePermission):


	def has_object_permission(self , request , view , obj):

		if request.method in permissions.SAFE_METHODS:

			return True

		else:

			return obj.owner == request.user




class IsValidUser(permissions.BasePermission):

	def has_permission(self , request , view):

		if request.method != 'POST':

			return True

		else:

			usernames = ['rasool' , 'admin']
			users = User.objects.filter(username__in=usernames)
			if request.user in users:

				return True

