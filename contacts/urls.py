from django.urls import path
from . import views
from .views import ContactCreateView
from .views import ContactDetailView
from .views import ContactUpdateView
from .views import ContactDeleteView

urlpatterns = [
    path("", views.contact_list, name="contact_list"),
    path("add/",ContactCreateView.as_view(),name="contact_add",),
    path("<int:pk>/", ContactDetailView.as_view(), name="contact_detail"),
    path("<int:pk>/edit/", ContactUpdateView.as_view(), name="contact_edit"),
    path("<int:pk>/delete/", ContactDeleteView.as_view(), name="contact_delete"),
    path("export/", views.contact_export, name="contact_export"),
    path("import/", views.contact_import, name="contact_import"),
]