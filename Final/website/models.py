from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField(max_length=100, unique=True)
	USER_TYPE_CHOICES = (
		(0, 'Private'),
		(1, 'Corporation')
	)
	user_type = models.SmallIntegerField(default=0, choices=USER_TYPE_CHOICES)
	location = models.CharField(max_length=50)
	comp_num = models.PositiveIntegerField(blank=True, null=True)
	points = models.PositiveIntegerField(default=0)
	

	class Meta:
		app_label = 'website'
		verbose_name = 'User'
		verbose_name_plural = 'Users'


class products(models.Model):
	product_name = models.CharField(max_length=255)
	Product_type = models.BooleanField(default=False)
	value = models.PositiveIntegerField(default=10)
	BIN_TYPE_CHOICES = (
		('כתום', 'כתום'),
		('כחול', 'כחול'),
		('חום', 'חום'),
		('ירוק', 'ירוק'),
		('סגול', 'סגול'),
		('אפור', 'אפור'),
		('מיחזורית- בקבוקי שתייה בנפח של מעל 1.5 ליטר ', 'מיחזורית- בקבוקי שתייה בנפח של מעל 1.5 ליטר '),
		('קרטוניה', 'קרטוניה'),
	)
	bin_type = models.CharField(max_length=255, choices=BIN_TYPE_CHOICES, null=True, blank=True)

	def __str__(self):
		return f"{self.product_name}, {self.bin_type}"
	

class usersContacts(models.Model):
	creationDT = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	status = models.BooleanField(default=False)


class usersrecycling(models.Model):
	creationDT = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(products, on_delete=models.CASCADE)
	userImg = models.ImageField(upload_to="usersImgs/")
	STATUS_CHOICES = (
		(0, 'ממתין לאישור'),
		(1, 'אושר'),
		(2, 'נדחה'),
	)
	status = models.IntegerField(choices=STATUS_CHOICES, default=0)

   
class quizForm(models.Model):
    question = models.CharField(max_length=255)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)

    def __str__(self):
        return self.question


class mapsForm(models.Model):
    name = models.CharField(max_length=100)
 

    def __str__(self):
        return self.name
	
class ShopForm(models.Model):
    product_name = models.CharField(max_length=255)
    product_type = models.BooleanField(default=True)
    value = models.PositiveIntegerField()

    def __str__(self):
        return self.product_name
