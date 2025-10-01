from django.db import models

# Create your models here.
class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    school = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    states = (("Lead", "Lead"),("Prospect", "Prospect"), ("Customer", "Customer"))
    state = models.CharField(choices=states, max_length=10)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-created_at"]
    