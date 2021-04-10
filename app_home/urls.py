from django.urls import path




from . import views
app_name = 'Home'

urlpatterns = [
    path('', views.IndexView, name="IndexView"),
    path('about-us/', views.AboutusView, name="AboutusView"),
    path('contact-us/', views.ContactView, name="ContactView"),
    path('category/<int:id>/<slug:slug>', views.CategoryView, name="CategoryView"),
    path('search/', views.SearchView, name="SearchView"),
    path('search_auto/', views.SearchAutoView, name="SearchAutoView"),
    path('faq/', views.faqView, name="faqView"),
]
