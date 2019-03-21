from django.db import models
from django.contrib.auth.models import User

class Remember(models.Model):
    name = models.CharField(max_length = 100, verbose_name="Название воспоминания")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField("Фото", upload_to="PlaceRememberApplication/photos", default="", blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    latitude = models.CharField(max_length = 100)
    longitude = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Воспоминание"
        verbose_name_plural = "Воспоминания"

    def __str__(self):
        return self.name

    def get_short_description(self):
        if len(self.description)>35:
            return self.description[:35] + "..."
        else:
            return self.description

    def get_short_name(self):
        if len(self.name) > 20:
            return self.name[:20] + "..."
        else:
            return self.name
