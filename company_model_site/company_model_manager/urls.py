from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('insert_root/', views.insert_root, name='insert_root'),
    # TODO replace above with nodes/root/ POST
    path('nodes/<node_id>/', views.get_node, name='get_node'),
    #TODO PUT with parent_id in body modifies parent
    path('nodes/<node_id>/descendants/', views.get_descendants, name='get_descendants'),
    #path('insert_node/<parent_id>/', views.insert_node, name='insert_node'),
    #TODO replace line above with nodes/ POST with parent_id - creates new node with chosen parent
    path('set_parent/<node_id>/<new_parent_id>/', views.set_parent, name='set_parent'),
]