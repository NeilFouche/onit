"""
Data Transformer - Employee

Source: Employee
"""

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor('Get:Employee')
class EmployeeProcessor(Processor):
    """
    Transformer for employee data

    Purpose: Formatting
    Context: Getting data from the database table: Employee
    """

    def transform(self, data, *args, **kwargs):
        person_transformer = TransformationService.get_processor('Get:Person')
        role_transformer = TransformationService.get_processor('Get:Role')
        employee_data = []
        for employee in data:
            employee_data.append({
                "id": employee.id,
                "key": employee.key,
                "email": employee.email,
                "phone": employee.phone,
                "person": person_transformer.transform([employee.person])[0],
                "role": role_transformer.transform([employee.role])[-1]
            })

        return employee_data
