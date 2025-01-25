from django.db import models

class ChemicalGroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Chemical(models.Model):
    name = models.CharField(max_length=255)  # Product name
    cas_number = models.CharField(max_length=255, blank=True, null=True)
    hs_code = models.CharField(max_length=255, blank=True, null=True)
    uses = models.TextField(blank=True, null=True)
    group = models.ForeignKey(ChemicalGroup, related_name='chemicals', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
