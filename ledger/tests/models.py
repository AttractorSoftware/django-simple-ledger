from django.db import models

class TestClient(models.Model):
    name = models.CharField(max_length=50)


class TestService(models.Model):
    name = models.CharField(max_length=50)

class TestReason(models.Model):
    description = models.TextField()
