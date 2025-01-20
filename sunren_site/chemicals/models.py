from django.db import models
class Chemical(models.Model):
    name = models.CharField(max_length=255)
    group = models.CharField(max_length=255)  # e.g., High-Purity Solvents
    un_no = models.CharField(max_length=20, blank=True, null=True)  # UN No.
    imco_code = models.CharField(max_length=20, blank=True, null=True)  # IMCO Code
    cas_no = models.CharField(max_length=20, blank=True, null=True)  # CAS No.
    msds = models.FileField(upload_to='msds/', blank=True, null=True)  # MSDS file
    coa = models.FileField(upload_to='coa/', blank=True, null=True)  # COA file
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
