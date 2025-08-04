from django.contrib import admin
from .models import *

admin.site.register(CategoryModel)
admin.site.register(BookModel)
admin.site.register(MemberModel)
admin.site.register(IssueModel)
