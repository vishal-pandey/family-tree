from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class Subscribe(models.Model):
	email = models.EmailField(blank=False)
	added_on = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.email


class ContactUs(models.Model):
	name = models.CharField(blank=True, max_length=255)
	email = models.CharField(blank=True, max_length=255)
	subject = models.CharField(blank=True, max_length=255)
	message = models.TextField(blank=True)

	class Meta:
		verbose_name = "Contact Us"
		verbose_name_plural = "Contact Us"


class PersonProfile(models.Model):

	created_by = models.ForeignKey(User, on_delete=models.CASCADE)

	name = models.CharField(blank=False, max_length=255)
	nickname = models.CharField(blank=True, max_length=255)
	mobile = models.CharField(blank=True, max_length=20)

	photo = models.ImageField(upload_to='profile_pic', blank=True)

	fathers_name = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='father_name')
	mothers_name = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='mother_name') 

	dob = models.DateTimeField(auto_now_add=False, blank=True)
	sex = models.CharField(blank=True, max_length=1, choices=[('M', 'Male'), ('F', 'Female')], default='M')
	education = models.TextField(blank=True)
	occupation = models.TextField(blank=True)
	address = models.TextField(blank=True)

	marital_status = models.CharField(blank=True, max_length=50, choices=[('Married', 'Married'), ('Un-Married', 'Un-Married')], default='Un-Married')
	spouse_name = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='sp_name')
	place_of_married = models.TextField(blank=True)

	general_note = HTMLField(blank=True)
	bio = HTMLField(blank=True)

	email = models.EmailField(blank=True)

	def __str__(self):
		return self.name


class PersonChildren(models.Model):
	parent = models.ForeignKey(PersonProfile, blank=True, null=True, on_delete=models.SET_NULL, related_name='parent')
	child = models.ForeignKey(PersonProfile, blank=True, null=True, on_delete=models.SET_NULL, related_name='child')

class PersonPhotos(models.Model):
	person = models.ForeignKey(PersonProfile, blank=True, null=True, on_delete=models.SET_NULL, related_name='person')
	pic = models.ImageField(upload_to='person_pic', blank=True)

