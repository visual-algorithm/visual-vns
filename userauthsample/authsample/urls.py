from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesmanViewSet, CityViewSet, RouteViewSet, SolutionViewSet, UserRegistrationView,  send_result_for_ios, send_result
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register("salesmen", SalesmanViewSet)
router.register("cities", CityViewSet)
router.register("routes", RouteViewSet)
router.register("solutions", SolutionViewSet)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("", include(router.urls)),
    path("res/<uuid:route_id>/", send_result, name="send_result"),
    path("result/<uuid:route_id>/", send_result_for_ios, name="send_result_for_ios")
]
#東京都多摩市落合1-39