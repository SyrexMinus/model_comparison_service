from django.urls import path
from . import views

urlpatterns = [
    path("", views.panel),    
    path("uploadModel/", views.upload_model),
    path("createDataset/", views.create_dataset),
    path("createExperiment/", views.create_experiment),
    path("experiment/<int:experiment_id>/", views.show_experiment),
    path("updateDataset/<str:dataset_group>/", views.update_dataset),
]
