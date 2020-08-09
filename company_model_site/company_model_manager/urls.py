from django.urls import path

from . import views

app_name = "company_model_manager"
urlpatterns = [
    path("", views.index, name="index"),
    path("api/v1/nodes/<int:node_id>/", views.node_api, name="node_api"),
    path("nodes/<node_id>/", views.node_gui, name="node_gui"),
    path(
        "api/v1/nodes/<int:node_id>/descendants/",
        views.get_descendants_api,
        name="get_descendants_api",
    ),
    path(
        "nodes/<int:node_id>/descendants/",
        views.get_descendants_gui,
        name="get_descendants_gui",
    ),
]
