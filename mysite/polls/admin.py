from django.contrib import admin
from .models import Question, Choice

# Register your models here.
# 1) add a line to make the poll app modifiable in the admin 
#admin.site.register(Question)
# then Django was able to construct a default form representation
# 2) customize how the admin form looks and works:
#class QuestionAdmin(admin.ModelAdmin):
#    fields = ['pub_date', 'question_text']
#admin.site.register(Question, QuestionAdmin)

# Adding related objects
# a Question has multiple Choices, there are two ways to display related objects:
# 3.1)
#admin.site.register(Choice)
# Django knows that it has a Qustion ForeignKey
#   when add a Choice item, we see a <select> box to select a Question item to associate with
#   but this is an inefficient way of adding Choice objects to the system
# 3.2)
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_filter = ['pub_date']        # this adds a Filter sidebar (i.e. filter the change list by pub_date field)
    search_fields = ['question_text'] # this adds a search box at the top of the change list (i.e. LIKE query)

admin.site.register(Question, QuestionAdmin)

