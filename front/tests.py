from django.test import TestCase
from models import Employee

employee_data = Employee.objects.all()

print(list(employee_data.values()))
