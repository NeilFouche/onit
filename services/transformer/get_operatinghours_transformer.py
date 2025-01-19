"""
Data Transformer - OperatingHours

Source: OperatingHours
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Get:OperatingHours')
class OperatingHoursTransformer(TransformerService):
    """
    Transformer for operating_hours data

    Purpose: Formatting
    Context: Getting data from the database table: OperatingHours
    """

    def transform(self, data, *args, **kwargs):
        weekdays_map = {
            "MON": "Monday",
            "TUE": "Tuesday",
            "WED": "Wednesday",
            "THU": "Thursday",
            "FRI": "Friday",
            "SAT": "Saturday",
            "SUN": "Sunday"
        }

        office_transformer = TransformerService.get_transformer("Get:Office")

        operating_hours_data = []
        for operating_hours in data:
            operating_hours_data.append({
                "id": operating_hours.id,
                "day_of_week": weekdays_map[operating_hours.day_of_week],
                "office": office_transformer.transform([operating_hours.office]),
                "open_time": operating_hours.open_time,
                "close_time": operating_hours.close_time,
                "closed": operating_hours.closed
            })

        return operating_hours_data
