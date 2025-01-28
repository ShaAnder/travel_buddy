from django.contrib import admin
from .models import Recommendation, Comment, Vote, Category

# Register your models here.
admin.site.register(Recommendation)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Vote)
