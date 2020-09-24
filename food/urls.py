from django.urls import path, include
from . import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register("", views.AkatsukiViewSet)
# router.register("<int:year>/<int:month>/<int:day>", views.AkatsukiView, base_name="inoutreports")

app_name = "food"
urlpatterns = [
    path("", views.index, name="index"),
    path("form/", views.form, name="form"),
    path("api/", views.AkatsukiViewSet.as_view({"get": "list"}), name="api"),
    path("api/<int:year>/<int:month>/<int:day>/", views.AkatsukiYearMonthDay.as_view(), name="api-year-month-day"),
    path("api/<int:year>/<int:month>/", views.AkatsukiYearMonth.as_view(), name="api-year-month"),
    path("api/<int:year>/", views.AkatsukiYear.as_view(), name="api-year")
]

# urlpatterns += router.urls
