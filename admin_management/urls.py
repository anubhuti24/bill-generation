from django.contrib import admin
from django.urls import path
from .views import (
    AddItem,
    UpdateItem,
    RemoveItem,
    BillGeneration,
    UserRegistration,
    UserLogin,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", UserRegistration.as_view()),
    path("login/", UserLogin.as_view()),
    path("add-item/", AddItem.as_view()),
    path("edit-item/<int:pk>/", UpdateItem.as_view()),
    path("remove-item/<int:pk>/", RemoveItem.as_view()),
    path("bill-generation/", BillGeneration.as_view()),
]
