"""
URL principale du projet Django
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Administration Django
    path('admin/', admin.site.urls),

    # Application bibliotheque
    path('bibliotheque/', include('bibliotheque.urls')),

    # Redirection racine vers bibliotheque
    path('', RedirectView.as_view(url='/bibliotheque/', permanent=False)),
]