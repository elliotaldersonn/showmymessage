from django.db import models
from msg.models import Message
# Create your models here.
class Transaction(models.Model):
	msg = models.OneToOneField(Message, on_delete=models.CASCADE)
	tstatus = models.CharField(max_length=500,null=True,blank=True)
	txnid = models.CharField(max_length=64)
	txnamount = models.CharField(max_length=10)
	order_id = models.CharField(max_length=50)
	bank_name = models.CharField(max_length=100,null=True,blank=True)
	bank_txnid = models.CharField(max_length=50,null=True,blank=True)
	tdate = models.CharField(max_length=100,null=True,blank=True)