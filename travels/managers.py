from django.db import models

class OrderQuerySet(models.QuerySet):
    def get_user_order(self, username):
        return self.filter(user = username, ordered=False)

class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)
    
    def get_user_order(self, username):
        return self.get_queryset().get_user_order(username)