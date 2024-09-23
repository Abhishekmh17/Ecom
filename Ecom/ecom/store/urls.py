from django.urls import path
from store import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='About'),
    path('login/',LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('signup/',views.signup, name='signup'),
    path('product/<int:id>',views.product_view,name='product'),
    path('category/<str:name>',views.category,name='category'),
    #path('product/cart',views.add_cart,name='cart'),
    #path('cart/',views.cart_view,name='cart_summary'),
     path('cart/',views.cart_view, name='cart_view'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/',views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:cart_item_id>/',views.update_cart, name='update_cart'),
    path('search/',views.search_view,name='search_view'),
    path('checkout/',views.checkout,name='checkout'),
    
]
