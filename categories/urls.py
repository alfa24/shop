from django.urls import path

from categories.views import CategoriesEdit

urlpatterns = [
    path('', CategoriesEdit.as_view(), name='categories_edit'),
]
