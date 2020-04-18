from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.shortcuts import reverse

COUNTRY_CHOICES = (
    ('M', 'Mexique'),
    ('C', 'Cuba'),
    ('RP', 'République dominicaine')
)

class Destination(models.Model):
    hotel_name = models.CharField(max_length=200)
    country = models.CharField(choices=COUNTRY_CHOICES, max_length=2)
    picture = models.ImageField(upload_to='pictures/destinations/', blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.hotel_name

class Travel(models.Model):
    name = models.CharField(max_length=200)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    start_day = models.DateField()
    end_day = models.DateField()
    slug = models.SlugField()

    """def get_absolute_url(self, slug):
        return reverse('travels', kwargs={'slug': self.slug})"""

    def __str__(self):
        return self.name

    def generate_slug(self): #FIXME: Valider qu'il n'y aura pas de doublon d'adresse
        return slugify(self.destination.name)

    """ Génère automatiquement un slug
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Travel, self).save(*args, **kwargs)
    """

class OrderTravel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} de {self.travel.name}"

    def get_total_travel_price(self):
        return self.quantity * self.travel.price


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    travels = models.ManyToManyField(OrderTravel)
    ordered = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = 0
        for travel in self.travels.all():
            total += travel.get_total_travel_price()
        return total