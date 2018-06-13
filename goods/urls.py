from django.urls import path

from goods.twviews import GoodListView, GoodDetailView, GoodCreate, GoodUpdate, GoodDelete
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('<int:cat_id>/', views.index, name='index'),
    # path('good/<int:good_id>/', views.good, name='good'),
    path('<int:cat_id>/', GoodListView.as_view(), name='index'),
    path('good/<int:good_id>/', GoodDetailView.as_view(), name='good'),
    path('<int:cat_id>/add/', GoodCreate.as_view(), name='good_add'),
    path('good/<int:good_id>/edit/', GoodUpdate.as_view(), name='good_edit'),
    path('good/<int:good_id>/delete/', GoodDelete.as_view(), name='good_delete'),

]
