from django.contrib import admin
from django.db import models
from functools import reduce

# Declaring raw_id_fields in your python model's admin class is a good practice because:
# 1. it makes your admin more usable, because, if you don't foreign keys and many to many relations 
#        will be displayed in a HUGE dropdown which is kinda annoying to find what you're looking for, and instead, 
#        if you do put the raw id fields it will put a magnifying glass next to the field so you can search for the instance
#        you may be trying to associate with.
# 2. it makes your admin MUCH MORE performatic so it doesn't have to query over all possible entities to populate the dropdown
#        on your instance page load, instead, it will only query for those other options if you click on the magnifying glass

# given the models

class MyClass1(models.Model):
    pass

class MyClass2(models.Model):
    my_fk_field = models.ForeignKey(MyClass1)

# instead of doing it the conventional way:
    

class MyClassAdmin(admin.ModelAdmin):
    raw_id_fields = ['my_fk_field']

# admin.site.register(MyClass2, MyClassAdmin)

# you will probably wanna replicate it over most of your models, so the best practice is define a super class to do it for you

class RawIdAdminModel(admin.ModelAdmin):
    def __init__(self, model, admin_site, *args, **kwargs):
        self.raw_id_fields = [field.name for field in model._meta.concrete_fields if self.is_fk_or_m2m(field)]
        super(RawIdAdminModel, self).__init__(model, admin_site, *args, **kwargs)
        
    def is_fk_or_m2m(self, field):
        return reduce((lambda x, y: x or isinstance(field, y)), [models.ForeignKey, models.OneToOneField, models.ManyToManyField], False)
        
# now instead of doing: admin.site.register(MyClass2, MyClassAdmin), this will have the same effect:
admin.site.register(MyClass2, RawIdAdminModel)

# and if you still wanna do more stuff then just declaring the raw_id_fields of all external keys of your model:
# you may inherit it while, declaring another admin class, instead of inheriting from admin.ModelAdmin, like this:

class MyClassAdmin2(RawIdAdminModel):
    pass
    # do more stuff
