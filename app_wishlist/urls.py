from django.urls import path
from .views import wishlist_view, wishlist_add_view_json, wishlist_del_view_json, wishlist_view_json, wishlist_del_view


app_name = 'app_wishlist'

urlpatterns = [
    path('wishlist/', wishlist_view, name='wishlist_view'),
    path('wishlist/api/add/<id_product>', wishlist_add_view_json),
    path('wishlist/api/del/<id_product>', wishlist_del_view_json),
    path('wishlist/api/', wishlist_view_json),
    path('wishlist/remove/<str:id_product>', wishlist_del_view, name='wishlist_remove')
]