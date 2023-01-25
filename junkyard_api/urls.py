from rest_framework import routers


from .viewsets.items import ItemsViewSet
from .viewsets.tenants import TenantsViewSet
from .viewsets.users import UsersViewSet


router = routers.SimpleRouter()

router.register(r'items', ItemsViewSet, basename='items')
router.register(r'tenants', TenantsViewSet, basename='tenants')
router.register(r'users', UsersViewSet, basename='users')

urlpatterns = router.urls
