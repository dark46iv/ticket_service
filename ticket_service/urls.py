from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from tickets.views import TicketAuthToken

schema_view = get_schema_view(title='API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tickets.urls')),
    path('schema/', schema_view),
    path('docs/', include_docs_urls(title='API Documentation')),
    path('token/', TicketAuthToken.as_view()),
    path('api-auth/', include('rest_framework.urls')),
]
