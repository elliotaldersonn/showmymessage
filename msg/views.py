from django.shortcuts import render, redirect, get_object_or_404
from .models import Message, Counter
from django.conf import settings
import random
import string
from paytm.checksum import generate_checksum
# Create your views here.

def random_string_generator(text,size=6, chars=string.ascii_lowercase + string.digits):
    return text + ''.join(random.choice(chars) for _ in range(size))

def homepage(request):
	if request.method == 'POST':
		msg = request.POST.get('msg')
		order_id = random_string_generator('ORDER_')
		cust_id = random_string_generator('CUST_')
		obj = Message.objects.create(msg=msg,order_id=order_id,cust_id=cust_id)
		#return redirect('payment') harie same data filld by user send to paytm..sssn main.tn.
		#redirect hvto grab orderid from topedb..diff user
		#return redirect(successview)

		#request to paytm
		data_dict = {
            'MID': settings.MID,
            'ORDER_ID': order_id,
            'TXN_AMOUNT': settings.TXN_AMOUNT,
            'CUST_ID': cust_id,
            'INDUSTRY_TYPE_ID': settings.INDUSTRY_TYPE_ID, 
            'WEBSITE': settings.WEBSITE,
            'CHANNEL_ID': settings.CHANNEL_ID,
	    	'CALLBACK_URL': 'http://127.0.0.1:8000'+str(settings.CALLBACK_URL),
        }
		data_dict['CHECKSUMHASH'] = generate_checksum(data_dict, settings.MKEY)
		return render(request,'payment.html', { 'param_dict' : data_dict,'endpoint':settings.ENDPOINT })
	else:
		object = Message.objects.filter(status=True).last()
		obj2 = get_object_or_404(Counter, id=1)
		Counter.objects.counter(obj2.counter)
		#print(type(request.get_host())) --> str
		#print(type(settings.CALLBACK_URL)) --> proxy
	context = {'object': object,'obj2': obj2,}
	return render(request,'msg/index.html',context)
