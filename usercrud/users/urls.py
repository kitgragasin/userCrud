from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.render_list),
    path('ajax_view/', views.ajax_view),
    path('ajax_log/', views.ajax_log_view)
    # other URL patterns
]