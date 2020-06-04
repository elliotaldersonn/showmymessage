from django.contrib import admin
from .models import Message , Counter
from paytm.models import Transaction
# Register your models here.


class TransactionInline(admin.StackedInline):
	model = Transaction

class MessageAdmin(admin.ModelAdmin):
	list_display = ('msg','timestamp','status','order_id','cust_id',)
	inlines = [TransactionInline]
	search_fields = ['order_id','msg','status','cust_id',]

admin.site.register(Message,MessageAdmin)
admin.site.register(Counter)