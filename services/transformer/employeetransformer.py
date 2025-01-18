"""
Data Transformer - Employee

Source: Employee
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Table:Employee')
class EmployeeTransformer(TransformerService):
    """
    Transformer for employee data

    Used by: Front - Employee data
    """

    def transform(self, data, *args, **kwargs):
        person_transformer = TransformerService.get_transformer('Table:Person')
        role_transformer = TransformerService.get_transformer('Table:Role')
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
