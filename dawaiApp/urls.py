from django.urls import path

from schema_graph.views import Schema

from . import views

urlpatterns = [
	path('', views.home),
	path('blogs', views.blogsView),
	path('blog', views.blogsMore),
	path('products', views.products),
	path('product', views.productsMore),
	path('about', views.aboutUs),
	path('handv', views.HandV),
	path('calculator', views.calculator),
	path('drugstores', views.drugStores),



	#drugs
	path('searchdrugs', views.drugsSearch),



	#drug store

	path('getratings', views.getRatings),
	path('rate', views.rate),

	#user related
	path('signup', views.signup),
	path('signin', views.signin),
	path('activate', views.activateAccount),
	path('logout', views.logout),


	#pharmacies
	path('pharmacy/signin', views.pharmacyLogin),

	#pharmacy logout 
	path('pharmacy/logout', views.logoutPharmacy),

	#pharmacies
	path('pharmacy', views.pharmacyLogin),

	#Questions
	path('pharmacy/questions', views.questions),
	
	#Help 
	path('help', views.help),

	#Answers
	path('answers', views.answers),

	#Profile
	path('profile', views.profile),

	#Edit F Name
	path('edit/firstname', views.editfname),

	
	#Edit L Name
	path('edit/lastname', views.editlname),

	
	#Edit Password
	path('edit/password', views.editpassword),

	#Delete Profile
	path('delete', views.deleteprofile),

	#Send Mail Delete
	path('deleteaccount', views.senddelete)
]
urlpatterns += [path("schema/" , Schema.as_view())]