from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class ChemicalGroup(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('chemicals_by_group', kwargs={'group_slug': self.slug})

    def __str__(self):
        return self.name

class Chemical(models.Model):
    name = models.CharField(max_length=255)  # Product name
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    cas_number = models.CharField(max_length=255, blank=True, null=True)
    hs_code = models.CharField(max_length=255, blank=True, null=True)
    uses = models.TextField(blank=True, null=True)
    group = models.ForeignKey(ChemicalGroup, related_name='chemicals', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('chemical_detail', kwargs={'chemical_slug': self.slug})

    def __str__(self):
        return self.name
