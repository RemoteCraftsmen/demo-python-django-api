from django.utils.timezone import make_aware
from datetime import datetime, timedelta


class DateService:
    @staticmethod
    def tomorrow():
        naive_datetime = datetime.now() + timedelta(hours=24)
        aware_datetime = make_aware(naive_datetime)
        return aware_datetime

    @staticmethod
    def yesterday():
        naive_datetime = datetime.now() - timedelta(hours=24)
        aware_datetime = make_aware(naive_datetime)
        return aware_datetime
