from django.urls import include, path
from .views import *

app_name = "libraryapp"

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', home, name='home'),
    path('books/', book_list, name='books'),
    path('librarians/', list_librarians, name='librarians'),
    path('libraries/', list_libraries, name='libraries'),
    path('logout/', logout_user, name='logout'),
]