from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('insert_root/', views.insert_root, name='insert_root'),
    path('get_descendants/<node_id>/', views.get_descendants, name='get_descendants'),
    path('insert_node/<parent_id>/', views.insert_node, name='insert_node'),
    path('set_parent/<node_id>/<new_parent_id>/', views.set_parent, name='set_parent'),
]