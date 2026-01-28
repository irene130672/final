from django.urls import path
from . import views

app_name = "applies"

urlpatterns = [
    path("<int:listing_id>", views.apply, name="apply"),
    path("withdraw/<int:listing_id>", views.withdraw_application, name="withdraw"),
]