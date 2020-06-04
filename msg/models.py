from django.db import models

# Create your models here.

class Message(models.Model):
	msg = models.CharField(max_length=60)
	timestamp = models.DateTimeField(auto_now_add=True)
	status = models.BooleanField(default=False)
	order_id = models.CharField(max_length=15)
	cust_id = models.CharField(max_length=15)
	

	def __str__(self):
		return self.msg

class CounterManager(models.Manager):
	def counter(self,views):
		return self.get_queryset().filter(id=1).update(counter=views+1)

class Counter(models.Model):
	counter = models.PositiveIntegerField(default=1)
	objects = CounterManager()
