from rest_framework.test import APITestCase
from rest_framework import status
from .models import DroneCategory , Pilot
from . import views
from django.utils.http import urlencode
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User






class DroneCategoryTests(APITestCase):

	def post_drone_category(self , name):

		url = reverse(views.DroneCategoryList.name)
		data = {'name' : name}
		response = self.client.post(url , data , format='json')
		return response


	def test_post_drone_category(self):

		drone_category_name = 'name'
		response = self.post_drone_category(drone_category_name)

		assert response.status_code == status.HTTP_201_CREATED
		assert DroneCategory.objects.count() == 1
		assert DroneCategory.objects.get().name == drone_category_name


	def test_post_existing_drone_category(self):

		drone_category_name = 'name'
		response1 = self.post_drone_category(drone_category_name)

		assert response1.status_code == status.HTTP_201_CREATED

		response2 = self.post_drone_category(drone_category_name)

		assert response2.status_code == status.HTTP_400_BAD_REQUEST


	def test_filter_drone_category_by_name(self):

		drone_category_name1 = 'name1'
		self.post_drone_category(drone_category_name1)
		drone_category_name2 = 'name2'
		self.post_drone_category(drone_category_name2)

		filter_by_name = {'name' : drone_category_name1}
		url = '{}?{}'.format(reverse(views.DroneCategoryList.name) , urlencode(filter_by_name))

		response = self.client.get(url , format='json')
		assert response.status_code == status.HTTP_200_OK
		assert response.data['count'] == 1
		assert response.data['results'][0]['name'] == drone_category_name1


	def test_update_drone_category(self):

		drone_category_name = 'name'
		response = self.post_drone_category(drone_category_name)

		updated_drone_category_name = 'updated name'
		url = reverse(views.DroneCategoryDetail.name , None , {response.data['pk']})
		data = {'name' : updated_drone_category_name}
		patched_response = self.client.patch(url , data , format='json')

		assert patched_response.status_code == status.HTTP_200_OK
		assert patched_response.data['name'] == updated_drone_category_name


	def test_get_drone_category_collection(self):

		drone_category_name = 'name'
		response = self.post_drone_category(drone_category_name)

		url = reverse(views.DroneCategoryList.name)
		get_response = self.client.get(url , format='json')

		assert get_response.status_code == status.HTTP_200_OK
		assert get_response.data['count'] == 1
		assert get_response.data['results'][0]['name'] == drone_category_name


	def test_get_one_drone_category(self):

		drone_category_name = 'name'
		response = self.post_drone_category(drone_category_name)

		url = reverse(views.DroneCategoryDetail.name , None , {response.data['pk']})

		get_response = self.client.get(url , format='json')

		assert get_response.status_code == status.HTTP_200_OK
		assert get_response.data['name'] == drone_category_name





class PilotTests(APITestCase):

	def post_pilot(self , name , gender):

		url = reverse(views.PilotList.name)
		data = {'name' : name,
				'gender' : gender}


		response = self.client.post(url , data , format='json')
		return response


	def create_user_and_set_token(self):

		user = User.objects.create(username='username',
								   email='dramatic225@gmail.com',
								   password='mohsen1160417237')

		token = Token.objects.create(user=user)
		self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))


	def test_post_and_get_pilot(self):

		pilot_name = 'mohsen'
		pilot_gender = Pilot.Male

		self.create_user_and_set_token()
		response = self.post_pilot(pilot_name , pilot_gender)
	
		assert response.status_code == status.HTTP_201_CREATED
		assert Pilot.objects.count() == 1

		saved_pilot = Pilot.objects.get()

		assert saved_pilot.name == pilot_name
		assert saved_pilot.gender == pilot_gender

		url = reverse(views.PilotDetail.name , None , {saved_pilot.pk})
		authorized_response = self.client.get(url , format='json')
		assert authorized_response.status_code == status.HTTP_200_OK
		assert authorized_response.data['name'] == pilot_name

		self.client.credentials()
		unauthorized_response = self.client.get(url , format='json')
		assert unauthorized_response.status_code == status.HTTP_401_UNAUTHORIZED


	def test_try_to_post_unauthorized(self):

		pilot_name = 'mohsen'
		pilot_gender = Pilot.Male

		response = self.post_pilot(pilot_name , pilot_gender)

		assert response.status_code == status.HTTP_401_UNAUTHORIZED
		assert Pilot.objects.count() == 0
