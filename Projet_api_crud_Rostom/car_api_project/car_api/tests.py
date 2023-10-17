from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Car

class CarAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_car(self):
        data = {
            "make": "Toyota",
            "model": "Camry",
            "year": 2023,
            "price": 25000.00
        }

        response = self.client.post('/api/cars/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(Car.objects.get().make, 'Toyota')

    def test_get_car_list(self):
        response = self.client.get('/api/cars/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_car_detail(self):
        car = Car.objects.create(
            make="Honda",
            model="Civic",
            year=2022,
            price=22000.00
        )

        response = self.client.get(f'/api/cars/{car.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_car(self):
        car = Car.objects.create(
            make="Ford",
            model="Mustang",
            year=2022,
            price=35000.00
        )

        updated_data = {
            "price": 38000.00
        }

        response = self.client.patch(f'/api/cars/{car.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        car.refresh_from_db()
        self.assertEqual(car.price, 38000.00)

    def test_delete_car(self):
        car = Car.objects.create(
            make="Chevrolet",
            model="Malibu",
            year=2023,
            price=27000.00
        )

        response = self.client.delete(f'/api/cars/{car.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Car.objects.count(), 0)
