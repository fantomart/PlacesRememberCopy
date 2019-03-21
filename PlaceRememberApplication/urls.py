from .views import RememberListView, RememberDetailView, remember_create, remember_edit
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', RememberListView.as_view(), name='remember-list'),
    path('<int:pk>', RememberDetailView.as_view(), name='remember-detail'),
    path('', include('social_django.urls', namespace='social')),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('add/', remember_create, name = 'remember-create'),
    path('<int:pk>/edit', remember_edit, name='remember-edit'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)