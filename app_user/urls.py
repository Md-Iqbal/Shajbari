from django.urls import path


from . import views

app_name = 'App_User'

urlpatterns = [
    path('sign-up/', views.SignUpView, name="SignUpView"),
    path('login/', views.LoginView, name="LoginView"),
    path('logout/', views.LogoutView, name="LogoutView"),
    path('<username>/', views.ProfileView, name="ProfileView"),
    path('-update-info', views.UserInfoUpdateView, name="UserInfoUpdateView"),
    path('update-password', views.UserPasswordUpdateView,
         name="UserPasswordUpdateView"),
    path('my-orders', views.OrderHistoryView, name="OrderHistoryView"),
    path('my-wishlist', views.WishlistHistoryView, name="WishlistHistoryView"),
    path('my-order/<int:id>', views.UserOrderDetailView,
         name="UserOrderDetailView"),
    path('my-comments', views.UserCommentListView,
         name="UserCommentListView"),
    path('delete-comment/<int:id>', views.DeleteCommentView,
         name="DeleteCommentView"),
    # path('<username>/', views.UserUpdateView, name="UserUpdateView"),
]
