from django.contrib import admin
from website.models import Subscribe, ContactUs, PersonProfile, PersonChildren, PersonPhotos

from django.forms import ModelForm
from django import forms

from django.db.models import Q

class SubscribeAdmin(admin.ModelAdmin):
	model = Subscribe
	list_display = ['email', 'added_on']

class ContactUsAdmin(admin.ModelAdmin):
	model = ContactUs
	list_display = ['name', 'email', 'subject', 'message']



class CourseForm(forms.ModelForm):
	class Meta:
		model = PersonProfile
		fields = ['name','nickname','mobile','fathers_name','mothers_name','dob','sex','education','occupation','address','marital_status','spouse_name','place_of_married','general_note','bio']

	def clean_teacher_id(self):
		if not self.cleaned_data['created_by']:
			return User()
		return self.cleaned_data['created_by']




class PersonChildrenAdmin(admin.TabularInline):
	model = PersonChildren
	list_display = ['parent', 'child']
	fk_name = 'parent'


class PersonPhotosAdmin(admin.TabularInline):
	model = PersonPhotos
	list_display = ['person', 'pic']
	fk_name = 'person'


class PersonProfileAdmin(admin.ModelAdmin):
	model = PersonProfile
	list_display = ['id', 'name','nickname','mobile','email','fathers_name','mothers_name','dob','sex','education','occupation','address','marital_status','spouse_name','place_of_married', 'created_by', ]
	fieldsets = ((None, {'fields': ('name','nickname','photo','mobile','email','fathers_name','mothers_name','dob','sex','education','occupation','address','marital_status','spouse_name','place_of_married','general_note','bio')}), )
	search_fields = ['name', 'nickname']
	inlines = [PersonChildrenAdmin, PersonPhotosAdmin]

	def save_model(self, request, obj, form, change):
		obj.created_by = request.user
		obj.save()

	ob = PersonProfile.objects.all()


	def get_queryset(self, request):
		qs = super(PersonProfileAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		else:
			ob = PersonProfile.objects.filter(~Q(created_by=request.user))
			return qs.filter(created_by = request.user)


	# def has_delete_permission(self, request, obj=None):
	# 	self.obj = PersonProfile.objects.filter(~Q(created_by=request.user))
	# 	if request.user.is_superuser:
	# 		# return qs
	# 		return True
	# 	else:
	# 		# return qs.filter(created_by = request.user)
	# 		return False

	# def has_change_permission(self, request, obj=None):
	# 	self.obj = PersonProfile.objects.filter(~Q(created_by=request.user))
	# 	if request.user.is_superuser:
	# 		# return qs
	# 		return True
	# 	else:
	# 		# return qs.filter(created_by = request.user)
	# 		return False




# admin.site.register(Subscribe, SubscribeAdmin)
# admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(PersonProfile, PersonProfileAdmin)