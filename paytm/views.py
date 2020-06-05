from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .checksum import verify_checksum
from msg.models import Message
from .models import Transaction
from django.http import Http404

# Create your views here.

@csrf_exempt
def handleresponse(request):
	#paytm will send response here
	try:
		form = request.POST
		response_dict = {}
		for i in form.keys():
			response_dict[i] = form[i]
			if i == 'CHECKSUMHASH':
				checksum = form[i]
		verify = verify_checksum(response_dict, settings.MKEY ,checksum)
	#returns 404 if user tries to directly access '/transaction/'
	except:
		raise Http404
	if verify:
		if response_dict['RESPCODE'] == '01':
			#transaction success
			#Message.objects.filter(order_id=response_dict['ORDERID']).update(status=True)
			msg = Message.objects.get(order_id=response_dict['ORDERID'])
			#avoid data re-insertion if page gets refreshed
			if msg.status == False:
				msg.status = True
				msg.save()
			#avoid data re-insertion if page gets refreshed
			refreshcheck = Transaction.objects.filter(msg=msg)
			if not refreshcheck.exists():
				Transaction.objects.create(msg=msg,
				 tstatus=response_dict['RESPMSG'],txnid=response_dict['TXNID'],
				 txnamount=response_dict['TXNAMOUNT'],order_id=response_dict['ORDERID'],
				 bank_name=response_dict['BANKNAME'],bank_txnid=response_dict['BANKTXNID'],
				 tdate=response_dict['TXNDATE'],)
			return render(request,'paytm/success.html',{'response':response_dict})


	msg = Message.objects.get(order_id=response_dict['ORDERID'])
	#avoid data re-insertion if page gets refreshed
	refreshcheck = Transaction.objects.filter(msg=msg)
	if not refreshcheck.exists():
		Transaction.objects.create(msg=msg,
				 tstatus=response_dict['RESPMSG'],txnid=response_dict['TXNID'],
				 txnamount=response_dict['TXNAMOUNT'],order_id=response_dict['ORDERID'],)
			 
	return render(request,'paytm/failure.html',{'response':response_dict})
