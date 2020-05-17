from django.db import models

class blog(models.Model):
	title = models.CharField(max_length = 150)
	body = models.TextField()
	image = models.ImageField(upload_to = 'dawaiApp/static/images/blogs', blank = True)
	def __str__(self):
		return self.title
	class Meta:
		db_table = "blogs"
		verbose_name = "blog"
		verbose_name_plural = "blogs"

class category(models.Model):
	title = models.CharField(max_length = 50)
	def __str__(self):
		return self.title
	class Meta:
		db_table = "categories"
		verbose_name = "category"
		verbose_name_plural = "categories"
	
class product(models.Model):
	name = models.CharField(max_length = 50)
	description = models.TextField()
	image = models.ImageField(upload_to = 'dawaiApp/static/images/products', blank = True)
	category = models.ForeignKey('category', on_delete = models.CASCADE)
	def __str__(self):
		return  "{} : {}".format(self.category, self.name)
	class Meta:
		db_table = "products"
		verbose_name = "product"
		verbose_name_plural = "Products"

class user (models.Model):
	firstName = models.CharField(max_length=50)
	lastName = models.CharField(max_length=50)
	password = models.CharField(max_length=100)
	email = models.CharField(max_length=100, primary_key = True)
	validated = models.BooleanField(default=False)
	def __str__(self):
		return  "{} {}".format(self.firstName, self.lastName)

class drugStore(models.Model):
	name = models.CharField(max_length = 100, primary_key = True)
	password = models.CharField(max_length = 100)
	location = models.CharField(max_length = 1000)
	contacts = models.TextField(max_length = 1000)
	rating = models.FloatField(default = 5)
	noOfRatings = models.IntegerField(default = 1)


class drug(models.Model):
	name = models.CharField(max_length = 50)
	description = models.TextField(max_length = 100)
	drugStore = models.ForeignKey('drugStore', on_delete = models.CASCADE)

class review(models.Model):
	body = models.TextField(max_length = 1000)
	user = models.ForeignKey('user', on_delete = models.CASCADE)
	store = models.ForeignKey('drugStore', on_delete = models.CASCADE)

class question(models.Model):
	body = models.TextField(max_length = 1000)
	image = models.ImageField(upload_to = 'dawaiApp/static/images/Questions', blank = True) 
	info = models.TextField(max_length = 1000, blank=True)
	owner = models.ForeignKey('user', on_delete = models.CASCADE)
	answered = models.BooleanField(default=False)
	answer = models.TextField(default = " ")
	
