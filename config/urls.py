
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('pages.urls',namespace='pages')),
    path('listings/', include('listings.urls',namespace='listings')),
    path('applies/', include('applies.urls',namespace='applies')),
    path('companies/', include('companies.urls',namespace='companies')),
    path('accounts/', include('accounts.urls',namespace='accounts')),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
