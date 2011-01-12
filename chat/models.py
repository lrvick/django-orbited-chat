from django.db import models

class Message(models.Model):
    user = models.CharField(max_length=100)
    body = models.TextField();
    time = models.DateTimeField();

    def __unitcode__(self):
        return user + " says: " + body

