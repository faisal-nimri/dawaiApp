from .models import blog, product, category, user, drugStore, review, drug, question
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator  
from django.utils import six
from random import choice
import re
from haversine import haversine

def home(request):
	return render(request, "home.html")

def aboutUs(request):
			return render(request, "aboutus.html")

def HandV(request):
			return render(request,"handv.html")

def calculator(request):
	 			
			return render(request, "calculator.html")

def drugStores(request):
			data = {"drugStores": drugStore.objects.all()}
			return render(request, "drugstores.html", data)

#blogs
def blogsView(request):
	allBlogs = blog.objects.all()
	blogsList = []
	for i in allBlogs:
				blogsList.append({ 
			'body' : i.body[:200],
			'image': str(i.image)[8:],#remove /dawaiApp
			'id' : i.id
			})
	data = {'blogs' : blogsList}
	return render(request, "blogs.html",data)

def blogsMore(request):
	id = request.GET["id"]
	blogList = blog.objects.filter(id=id)
	if len(blogList) == 0:
		return render(request, "message.html", {"error" : "404 Page not found"})
	blogs = blogList[0]
	data = {
		'title': blogs.title,
		'contents': blogs.body,
		'image': str(blogs.image)[8:],
	}
	return render(request,"more.html",data)



#products
def products(request):
	productList = product.objects.all()
	title = "Herbs & Vitamins"
	if 'category' in request.GET:
		categories = request.GET["category"]
		title = categories
		categories = category.objects.filter(title = categories)
		if len(categories) == 0:
			return render(request, "message.html", {"error" : "No products found"})
		productList = productList.filter(category=categories[0])
		if len(productList) == 0:
			return render(request, "message.html", {"error" : "No products found"})
	if 'problem' in request.GET and 'purpose' in request.GET:
		problem = request.GET['problem']
		purpose = request.GET['purpose']
		filter1 = productList.filter(description__contains = problem)
		filter2 = productList.filter(name__contains = problem)
		filter3 = productList.filter(description__contains = purpose)
		filter4 = productList.filter(name__contains = purpose)
		productList = (filter1 | filter2 | filter3 | filter4)
	
	productList = productList.distinct()
	

			
	products = []

	for i in productList:
				products.append({
				"name" : i.name,
				"image" : str(i.image)[8:],
				"id" : i.id 
			})
	data = {
		"title" : title,
		"products" : products
	}
	return render(request, "products.html", data)

def productsMore(request):
	id = request.GET["id"]
	productList = product.objects.filter(id=id)
	if len(productList) == 0:
		return render(request, "message.html", {"error" : "404 Page not found"})
	products = productList[0]
	data = {
		'name': products.name,
		'contents': products.description,
		'image': str(products.image)[8:],
		"categories" : category.objects.all()
	}
	return render(request,"more.html",data)


#user related
def randomString():
		letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+'
		return ''.join(choice(letters) for i in range(15))


class TokenGenerator(PasswordResetTokenGenerator):
		def _make_hash_value(self, user, timestamp):
				return ( six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.validated) )

accountActivationToken = TokenGenerator()

def signup(request):
	if request.method == "POST":
		if request.POST["password"] != request.POST["passwordConf"]:
			return render(request, 'signup.html', {"message" : "Your passwords don't match", "color" : "red" })
		if user.objects.filter(email=request.POST["email"]).count() > 0:
			return render(request, 'signup.html', {"message" : "Email already in use", "color" : "red" })
		newUser = user()
		newUser.firstName = request.POST["firstName"]
		newUser.lastName = request.POST["lastName"]
		newUser.email = request.POST["email"]
		newUser.password = make_password(request.POST["password"])
		newUser.save()
		message = "Activate your Account using the url http://127.0.0.1:8000/activate?email={}&token={}".format(newUser.pk,accountActivationToken.make_token(newUser))
		msg = EmailMessage("Dawai Acccount Activation", message, to=[request.POST["email"]])
		msg.send()
		return render(request, 'signup.html', {"message" : "Please check your email to activate your account", "color" : "green" })		
	else:
		return render(request, "signup.html")

def activateAccount(request):
		users = user.objects.filter(email=request.GET["email"])
		if users.count() == 0:
				return render(request,"message.html" , {"error": "The user doesn't exist"})
		users = users[0]
		if accountActivationToken.check_token(users, request.GET["token"]):
				users.validated = True
				users.save()
				return render(request,"message.html" , {"message" : "Your account has been activated successfuly"})
		return render(request,"message.html" , {"error": "Failed to activate your email"})

def signin(request):
		if request.method == "POST":
				users = user.objects.filter(email=request.POST["email"])
				if users.count() == 0:
						return render(request, "signin.html",{"wrongPass":"wrongPass", "action":"/signin"})
				users = users[0]
				if check_password(request.POST["password"],users.password):
						request.session["id"] = users.pk
						return redirect("/")
				return render(request, "signin.html",{"wrongPass":"wrongPass", "action":"/signin"})
		else:
				return render(request, "signin.html", {"action":"/signin"})

def logout(request):
		if 'id' in request.session:
				del request.session["id"]
		return redirect("/")

def logoutPharmacy(request):
		if 'pharmacy' in request.session:
				del request.session["pharmacy"]
		
		return redirect("/pharmacy")

def checkUser(request):
		'''
				Return value:
						email => logged in and validated
						1 => not validated
						2 => not logged in
						3 => account doesn't exist(This error might never exist)
		'''
		if 'id' not in request.session:
				return 2
		email = request.session['id']
		userObject = user.objects.filter(pk = email)
		if len(userObject) == 0:
				return 3
		userObject = userObject[0]
		if userObject.validated:
				return email
		return 1

#drugs

def getDistance(url, userLocation):
	location = re.findall("@([\d-]\d+\.\d+,[\d-]\d+\.\d+)" , url)[0].split(",")
	latitude, longitude = float(location[0]), float(location[1])
	storeLocation = (latitude, longitude)
	distance = haversine(userLocation, storeLocation)		
	return distance


def drugsSearch(request):
	if request.method == "POST":
		allDrugsList = []
		allDrugs = drug.objects.all()
		
		if 'syndromes' in request.POST and 'name' in request.POST and len(request.POST['syndromes'])>0:
			filter1 = allDrugs.filter(description__contains = request.POST['syndromes'])
			filter2 = allDrugs.filter(name__contains = request.POST['name'])
			allDrugs = (filter1 | filter2)
		else:
			if 'name' in request.POST:
				allDrugs = allDrugs.filter(name__contains = request.POST['name'])
		
		allDrugs = allDrugs.distinct()
		userLocation = (float(request.POST["latitude"]), float(request.POST["longitude"]))
		for drugi in allDrugs:
			url = drugi.drugStore.location
			allDrugsList.append({
				'name': drugi.name,
				'store': drugi.drugStore.name,
				'distance': getDistance(url,userLocation),
				'location': drugi.drugStore.location
			})
		return render(request, 'drugsfound.html', {"allDrugs":allDrugsList})

	
	return render(request, "drugsearch.html")



#drug stores
def getRatings(request):
	store = drugStore.objects.get(pk = request.GET["pk"])
	data = []
	data.append("{} Stars".format(str(round(store.rating,2))))
	data.append("------")
	reviews = review.objects.filter(store = store)
	for i in reviews:
		data.append("<sup style='color:#12BBAD'><i> {} {} </i></sup>".format(i.user.firstName,i.user.lastName))
		data.append(i.body)
		data.append("------")
	
	data = "<br>".join(data)
	return HttpResponse(data)


def rate(request):
	userState = checkUser(request)
	if userState == 1:
				return render(request, "message.html", {"error":"You need to validate your email first"})
	if userState == 2:
				return redirect("/signin")
	owner = user.objects.get(pk = userState)

	if request.method == "POST":
		storeName = request.POST["pk"]
		store = drugStore.objects.get(pk = storeName)

		if review.objects.filter(store = store).filter(user = owner).count() > 0:
			return render(request, "message.html", {"error":"you cant make more than one review"})

		newReview = review()
		newReview.body = request.POST["comment"]
		newReview.store = store
		newReview.user = owner
		newReview.save()

		rating = int(request.POST["rating"])
		if rating <= 5 and rating >= 0:
			newNoOfRatings = store.noOfRatings + 1
			store.noOfRatings = newNoOfRatings
			store.rating = (store.rating + rating) / newNoOfRatings
			store.save()
	return redirect("/drugstores")

def pharmacyLogin(request):
	if 'id' in request.session:
		del request.session["id"]
	if request.method == "POST":
		userName = request.POST["email"] 
		password = request.POST["password"]
		store = drugStore.objects.filter(name = userName)
		if len(store) == 0:
			return render(request, "signin.html",{"wrongPass":"wrongPass", "action":"/pharmacy/signin"})
		store = store[0]
		if password == store.password:
			request.session["pharmacy"] = userName 
			return redirect("/pharmacy/questions")
		return render(request, "signin.html",{"wrongPass":"wrongPass", "action":"/pharmacy/signin"}) 
	return render(request, "signin.html", {"title":"Pharmacy", "placeholder":"Enter pharmacy name", "action":"/pharmacy/signin"})


def questions(request):
	if request.method == "POST":
		comment = request.POST ["comment"]
		qid = request.POST ["qid"]
		q = question.objects.get (id = qid)
		q.answer = comment
		q.answered = True
		q.save()
		email = q.owner.email
		message = "Your medical question has been answered, Please check your website account"
		msg = EmailMessage("Dawai Medical Help Notification", message, to=[email])
		msg.send()
		return redirect("/pharmacy/questions")
	else:
		if "pharmacy" not in request.session:
			return redirect("/pharmacy")
		if 'id' in request.session:
			del request.session["id"]
		unanswered = [] 
		for i in question.objects.filter(answered = False):
			q = {"owner" : i.owner, "info" : i.info, "body" : i.body, "image" : str(i.image)[8:], "id" : i.id }
			unanswered.append(q)
		data = {"answered":question.objects.filter(answered = True),
		"unanswered" : unanswered}
		return render(request, "questions.html", data)


def help(request):
	if request.method == "POST":
		userState = checkUser(request)
		if userState == 1:
			return render(request, "message.html", {"error":"You need to validate your email first"})
		if userState == 2 or userState ==3: 
			return redirect("/signin")

		newquestion = question()
		newquestion.body = request.POST["descreption"]
		newquestion.image = request.FILES["img"]
		newquestion.info = request.POST["additional"]
		newquestion.owner = user.objects.get(pk = userState)
		newquestion.save()
		return render(request, "help.html", {"submitted":"submitted"})
	return render(request, "help.html")

def answers(request):
	userstat = checkUser(request)
	if userstat == 1:
		return render(request, "message.html", {"error":"You need to validate your email first"})
	if userstat == 2:
		return redirect("/signin")
	owner = user.objects.get(email = userstat)
	q = question.objects.filter(owner = owner , answered = True)
	data = {"questions" : q}
	return render(request, 'answers.html', data)

def profile(request):
	userstat = checkUser(request)
	if userstat == 1:
		return render(request, "message.html", {"error":"You need to validate your email first"})
	if userstat == 2:
		return redirect("/signin")
	userobject = user.objects.get(email = userstat)
	data = {
		"fname": userobject.firstName,
		"lname": userobject.lastName,
		"email": userstat
	}
	return render(request, 'profile.html', data)

def editfname(request):
	userstat = checkUser(request)
	if userstat == 1:
		return render(request, "message.html", {"error":"You need to validate your email first"})
	if userstat == 2:
		return redirect("/signin")
	if request.method == "POST":
		newfname = request.POST["fname"]
		userobject = user.objects.get(email = userstat)
		userobject.firstName = newfname
		userobject.save()
		return redirect("/profile")
	else:
		return redirect("/profile")

def editlname(request):
	userstat = checkUser(request)
	if userstat == 1:
		return render(request, "message.html", {"error":"You need to validate your email first"})
	if userstat == 2:
		return redirect("/signin")
	if request.method == "POST":
		newlname = request.POST["lname"]
		userobject = user.objects.get(email = userstat)
		userobject.lastName = newlname
		userobject.save()
		return redirect("/profile")
	else:
		return redirect("/profile")

def editpassword(request):
	userstat = checkUser(request)
	if userstat == 1:
		return render(request, "message.html", {"error":"You need to validate your email first"})
	if userstat == 2:
		return redirect("/signin")
	if request.method == "POST":
		oldpass = request.POST["oldpass"]
		newpass1 = request.POST["newpass1"]
		newpass2 = request.POST["newpass2"]
		userobject = user.objects.get(email = userstat)
		if not check_password(oldpass , userobject.password):
			return render(request, "profile.html", {"error":"Wrong Current Password"})
		if newpass1 != newpass2:
			return render(request, "profile.html", {"error":"New Password does not match"})
		userobject.password = make_password(newpass1)
		userobject.save()
		return render(request, "profile.html", {"success":"Password changed Successfully"})
	else:
		return redirect("/profile")

def deleteprofile(request):
	if 'id' in request.session:
		del request.session["id"]
	userobject = user.objects.filter(email=request.GET["email"])
	if userobject.count() == 0:
		return render(request,"message.html" , {"error": "The user doesn't exist"})
	userobject = userobject[0]
	if accountActivationToken.check_token(userobject, request.GET["token"]):
		userobject.delete()
		return render(request,"message.html" , {"message" : "Your account has been deleted successfuly"})
	return render(request,"message.html" , {"error": "Failed to delete your email"})


def senddelete(request):
	userstat = checkUser(request)
	if userstat == 1:
		return render(request, "message.html", {"error":"You need to validate your email first"})
	if userstat == 2:
		return redirect("/signin")
	if request.method == "POST":
		userobject = user.objects.get(email = userstat)
		message = "Please Click on the following link to delete your account http://127.0.0.1:8000/delete?email={}&token={}".format(userobject.pk,accountActivationToken.make_token(userobject))
		msg = EmailMessage("Delete your account", message, to=[userobject.email])
		msg.send()
		return render(request, "profile.html", {"delete":"Please check your email"})
	else:
		return redirect("/profile")