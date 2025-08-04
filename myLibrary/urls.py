from django.urls import path
from .views import *

urlpatterns = [
    path('',home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('books/', books_view, name='books'),
    path('members/', members_view, name='members'),
    path('issue/', issue_book, name='issue_book'),
    path('return/<int:issue_id>/', return_book, name='return_book'),
]
