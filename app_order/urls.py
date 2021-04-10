from django.urls import path


from . import views
app_name = 'Order'

urlpatterns = [
    path('add-to-cart/<int:id>/', views.AddtoCartView, name="AddtoCartView"),
    path('add-to-wishlist/<int:id>/',
         views.AddtoWishlistView, name="AddtoWishlistView"),
    path('view-cart/', views.CartListView, name="CartListView"),
    path('view-wishlist/', views.WishlistListView, name="WishlistListView"),
    path('delete-cart-item/<int:id>/',
         views.DeleteCartView, name="DeleteCartView"),
    path('delete-full-cart',
         views.DeleteFullCartView, name="DeleteFullCartView"),
    path('delete-wishlist-item/<int:id>/',
         views.DeleteWishlistView, name="DeleteWishlistView"),
    path('delete-full-wishlist',
         views.DeleteFullWishlistView, name="DeleteFullWishlistView"),
    path('checkout/', views.CheckoutView, name="CheckoutView"),
    path('payment/', views.PaymentView, name="PaymentView"),
    path('payment-status/', views.Order_PaymentComplete, name="Order_PaymentComplete"),
]
