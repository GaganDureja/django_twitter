from django.contrib import admin

# Register your models here.


from .models import *
# Register your models here.

admin.site.register(Tweet)

admin.site.register(User)

admin.site.register(T_Media)
admin.site.register(Tags)
admin.site.register(Following)


