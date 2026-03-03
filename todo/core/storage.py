from django.core.files.storage import FileSystemStorage
from datetime import datetime
import os


class DateBasedStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        today = datetime.now().strftime("%Y/%m/%d")
        name = os.path.join(today, name)
        return super().get_available_name(name, max_length)
