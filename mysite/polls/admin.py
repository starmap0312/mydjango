from django.contrib import admin
from .models import Question

# Register your models here.
admin.site.register(Question)     # need to add this to make the poll app modifiable in the admin
