from django.shortcuts import render, redirect
from .models import Products, ViewImage
from .models import ProdComment
from .models import Contact
from .models import Orders
from .models import OrderUpdate
from .models import Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from math import ceil
import json
from shop.templatetags import extras
from PayTm import Checksum
from django.http import HttpResponse
from django.core.mail import send_mail
# To allow other post request in our app
from django.views.decorators.csrf import csrf_exempt
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'
from django.conf import settings
# this is used for email 
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from marketing.models import MarketingMessage
from shop.filters import ProductFilter
from .forms import ProductSearchForm
# for rest framework
from .myserializer import ProductSerializer, OrderSerializer, UserSerializer
from rest_framework import viewsets


class ProductViewSet(viewsets.ModelViewSet):
	queryset = Products.objects.all().order_by("pub_date")
	serializer_class = ProductSerializer
	def get_queryset(self):
		si = self.request.GET.get('si')
		if si ==None:
			si = ""
		return Products.objects.filter(product_name__icontains = si)

class OrderViewSet(viewsets.ModelViewSet):
	queryset = Orders.objects.all()
	serializer_class = OrderSerializer

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer



def index(request):
	allProds = []
	marketing_message = request.marketing_message

	catprods=Products.objects.values('category','id')
	cats = {item['category'] for item in catprods}
	for cat in cats:
		prod = Products.objects.filter(category=cat).order_by('-pub_date')[:8]
		n = len(prod)
		nSlides = n//4 + ceil((n/4) - (n//4))	
		allProds.append([prod, range(1, nSlides), nSlides])

	params = {'allProds':allProds,'marketing_message':marketing_message}
	return render(request, 'shop/index.html', params)

def allproducts(request):
	form = ProductSearchForm(request.POST or None)
	if request.method == "POST":

		allcollection=Products.objects.filter(category__icontains=form['category'].value(),
		product_name__icontains=form['product_name'].value())
		
		# shortno = request.POST.get('shortno'," ")
		# print(shortno)
		# if shortno == 1:
		# 	shorting = 'price'
		# if shortno == 2:
		# 	shorting = '-price'
		# allcollection = Products.objects.all().order_by(shorting)

	else:
		allcollection = Products.objects.all()	
	
	# filtered_product = ProductFilter(request.GET,queryset=allcollection)

	paginator = Paginator(allcollection, 12)
	page = request.GET.get('page')
	try:
		allcollections = paginator.page(page)
	except PageNotAnInteger:
		allcollections = paginator.page(1)
	except EmptyPage:
		allcollections = paginator.page(paginator.num_pages)

	params = {'allcollections':allcollections,"form": form,
			}
	return render(request, 'shop/all-products.html', params) 

def searchMatch(query,item):
	'''return True only if query matches requirement'''
	query1 = query.lower()
	if query1 in item.desc.lower() or query1 in item.product_name.lower() or query1 in item.category.lower() or query1 in item.subcategory.lower():
		return True
	return False

def search(request):
	marketing_message = request.marketing_message
	query = request.GET.get('search')
	allProds = []
	catprods=Products.objects.values('category','id')
	cats = {item['category'] for item in catprods}
	for cat in cats:
		prodtemp = Products.objects.filter(category=cat)
		prod = [item for item in prodtemp if searchMatch(query, item)]
		n = len(prod)
		nSlides = n//4 + ceil((n/4) - (n//4))
		if len(prod) != 0:
			allProds.append([prod, range(1, nSlides), nSlides])
	params = {'allProds':allProds,"msz": 'Match','query':query}
	if len(allProds) == 0 or len(query)<4:
		params = {'msz':"No match, Re try with another key words", 'query':query,'marketing_message':marketing_message}
	return render(request, 'shop/search.html', params)



def about(request):
	return render(request,'shop/about.html')

def terms_of_service(request):
	return render(request,'shop/terms_of_service.html')

def privacy_policy(request):
	return render(request,'shop/privacy_policy.html')

def shipping_policy(request):
	return render(request,'shop/shipping_policy.html')

def return_policy(request):
	return render(request,'shop/return_policy.html')


def contact(request):
	if request.method == "POST":
		name = request.POST.get('name'," ")
		email = request.POST.get('email'," ")
		phone = request.POST.get('phone'," ")
		desc = request.POST.get('desc'," ")
		# print(name, email, phone, desc)
		contact = Contact(name=name, email=email, phone=phone, desc=desc)
		contact.save()
		name = contact.name
		thank = True
		return render(request,'shop/contact.html',{"name":name,"thank":thank})
	return render(request,'shop/contact.html')

def tracker(request):
	if request.method == "POST":
		orderId = request.POST.get('orderId'," ")
		email = request.POST.get('email'," ")
		try:
			order = Orders.objects.filter(order_id=orderId, email=email)
			
			if len(order)>0:
				update = OrderUpdate.objects.filter(order_id=orderId)
				updates = []
				for item in update:
					updates.append({'text': item.update_desc, 'time': item.timestamp})
					response = json.dumps({"status":"success","updates":updates,"itemsjson":order[0].item_json}, default=str)
				return HttpResponse(response)
			else:
				return HttpResponse('{"status":"noitem"}')
		except Exception as e:
			return HttpResponse('{"status":"error"}')

	return render(request,'shop/tracker.html')


def productView(request,myid):
	# fetch The product using the Id
	product = Products.objects.filter(id=myid)
	comments = ProdComment.objects.filter(product=product[0], parent=None)
	replies = ProdComment.objects.filter(product=product[0]).exclude(parent=None)
	replyDict={}
	for reply in replies:
		if reply.parent.sno not in replyDict.keys():
			replyDict[reply.parent.sno] = [reply]
		else:
			replyDict[reply.parent.sno].append(reply)

	return render(request,'shop/prodView.html',{"product":product[0],"comments":comments, "user":request.user, "replyDict":replyDict})

# For posting Comments
def prodComment(request):
	if request.method == "POST":
		comment = request.POST.get("comment")
		user = request.user
		productId = request.POST.get("productId") 
		product = Products.objects.get(id=productId)
		parentSno = request.POST.get("parentSno")
		if parentSno == "":
			comment = ProdComment(comment=comment, user=user, product=product)	
			messages.success(request,"Thankyou for your valuable comment.. Have a Good day")
		else:
			parent = ProdComment.objects.get(sno=parentSno)
			comment = ProdComment(comment=comment, user=user, product=product, parent=parent)
			messages.success(request,"Your replie have been Successfully recorded.. Have a Good day")
		comment.save()
	return redirect(f"/shop/products/{productId}")

def cart(request):
	data =1
	context = {'data':data}
	return render(request,'shop/cart.html',context)


def checkout(request):
	if request.method == "POST":
		item_json = request.POST.get('itemsJson', '')
		name = request.POST.get('name','')
		amount = request.POST.get('amount','')
		email = request.POST.get('email','')
		address = request.POST.get('address1','')
		address2 = request.POST.get('address2','')
		city = request.POST.get('city','')
		state = request.POST.get('state','')
		zip_code = request.POST.get('zip_code','')
		phone = request.POST.get('phone','')
		special = request.POST.get('special')
		user = request.user 
		if not amount ==str("0"):
			order = Orders(item_json=item_json, user=user, name=name, amount=amount, email=email, address=address, address2=address2, city=city, state=state, zip_code=zip_code, phone=phone, special=special)
			order.save()
			id = order.order_id 
			param_dict = {
			'MID':'WorldP64425807474247',
			'ORDER_ID':str(id),
			'TXN_AMOUNT':str(amount),
			'CUST_ID': email,
			'INDUSTRY_TYPE_ID':'Retail',
			'WEBSITE':'WEBSTAGING',
			'CHANNEL_ID':'WEB',
			'CALLBACK_URL':'https://mymart.pythonanywhere.com/shop/handlerequest/',
			}
			param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
			return render(request,'shop/paytm.html',{'param_dict':param_dict})
		else:
			messages.error(request,"You haven't choosen any item.....!! Please add item in your cart")
	return render(request,'shop/checkout.html')

def handleSignup(request):
	if request.method == "POST":
		# Get the Post parameters
		fnameUP = request.POST['fnameUP']
		lnameUP = request.POST['lnameUP']
		userUP = request.POST['userUP']
		emailUP = request.POST['emailUP']
		passwordUP = request.POST['passwordUP']
		rpasswordUP = request.POST['rpasswordUP']
		
		# check for enuromus input
		if not userUP.isalnum():
			messages.error(request, 'Username must contain number and letters.')
			return redirect('/shop/')
		if len(userUP) > 10:
			messages.error(request, 'Username must be under 10 character.')
			return redirect('/shop/')
		if passwordUP != rpasswordUP:
			messages.error(request, 'Password mismatch.')
			return redirect('/shop/')
		if User.objects.filter(username=userUP):
			messages.error(request, 'Username must be Unique, Choose another username. ')
			return redirect('/shop/')
		# sending mail 
			# sending mail 
			send_mail(
			'Your have successfully setup account on Indra cart',
			'Thanks for signing up with Indra cart! Have fun, and dont hesitate to contact us with your feedback.',
			settings.EMAIL_HOST_USER,
			[f"{emailUP}"],
			fail_silently=True,
			)
		# created Phone number as user "Hear i have use phone as a user name for aunth. you can use unique user name"
		myuser = User.objects.create_user(userUP, emailUP, passwordUP)
		myuser.first_name = fnameUP
		myuser.last_name = lnameUP
		myuser.save()
		messages.success(request,"Your have successfully created IE Cart account, Now login in to continue.")
		return redirect('/shop/')
	else:
		return HttpResponse("404- Not Found")

def handleLogin(request):
	if request.method == "POST":
		# Get the Post parameter
		userIN = request.POST['userIN']
		passwordIN = request.POST['passwordIN']

		user = authenticate(username=userIN, password=passwordIN)
		if user is not None:
			login(request, user)

			# adding for sessions
			request.session['message'] = f"{user.username}"
			messages.success(request,"Successfully Logged In")
			return redirect('/shop/profile')
		else:
			messages.info(request,"Invalid credentials, Please try again")
			return redirect('/')

	return HttpResponse('404- NOT FOUND')	

def handleLogout(request):
	logout(request)
	messages.success(request, "Successfully Log Out")
	return redirect("/shop/")

# hear we are taking request from other app bypassing csrf
@csrf_exempt
def handlerequest(request): 
	# Paytm will send you Post request
	if request.method == "POST":
		form = request.POST
		response_dict ={}
		for i in form.keys():
			response_dict[i] = form[i]
			if i == 'CHECKSUMHASH':
				checksum = form[i]
		verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
		if verify:
			if response_dict['RESPCODE']=='01':
				print('order successfull')
				status = Orders(status="Finished")
			else:
				print("order was not successfull because" + response_dict['RESPMSG'])
				status = Orders(status="Aborted")
	else:	
		return HttpResponse('404- NOT FOUND')
	# status.save()
	update = OrderUpdate(order_id=response_dict['ORDERID'], update_desc=response_dict['RESPMSG'])
	update.save()
	name=Orders.objects.last()
	odid = response_dict['ORDERID']
	temp = render_to_string('shop/email_template.html',{'name':name,'order_id':odid,'amount':response_dict['TXNAMOUNT']})
	try:
		if response_dict['RESPCODE']=='01':
			send_mail(
					f'Confirmation mail for payment on uptodate-Mart successfully done.',
					temp,
					settings.EMAIL_HOST_USER,
					[f"{name.email}"],
					fail_silently=True,
					)
		else:
			send_mail(
						f"{response_dict['RESPMSG']}",
						temp,
						settings.EMAIL_HOST_USER,
						[f"{name.email}"],
						fail_silently=True,
						)
	except:
			pass			
	return render(request, 'shop/paymentstatus.html',{'response':response_dict})
	
def profile(request):
	message = None
	if 'message' in request.session:
		message = request.session.get('message')
	else:
		return HttpResponse('404- NOT FOUND')
		# del request.session['message']
	user= User.objects.filter(username=message)
	u1 = request.user
	try:
		orders = Orders.objects.filter(user=u1).order_by('-order_id')
		
		context = {'message':message, "orders":orders, "itemsjson":orders[0].item_json}
		return render(request, 'shop/profile.html', context)
	except:
		pass
	context = {'message':message}
	return render(request, 'shop/profile.html', context)


def getorderid(request):
	
	if request.method == "POST":
		orderId = request.POST.get('orderId'," ")
		
		try:
			orders = Orders.objects.filter(order_id=orderId)
			if len(orders)>0:
				update = OrderUpdate.objects.filter(order_id=orderId)
				updates = []
				for item in update:
					updates.append({'text': item.update_desc, 'time': item.timestamp})
					response = json.dumps({"status":"success","updates":updates,"itemsjson":orders[0].item_json}, default=str)
				return HttpResponse(response)
			else:
				return HttpResponse('{"status":"noitem"}')
		except Exception as e:
			return HttpResponse('{"status":"error"}')

	return render(request,'shop/profile.html')
