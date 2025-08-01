from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class FileSizeValidator:
    def __init__(self, max_size, message=None):
        self.max_size = max_size
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = f"File size must be less than {self.max_size}"

        self.__message = value

    def __call__(self, value):
        if value.size > self.max_size * 1024 * 1024:
            raise ValidationError(self.message)
