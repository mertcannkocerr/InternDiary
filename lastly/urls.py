from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from accounts.views import LoginRedirectionView

urlpatterns = [
    path('', LoginRedirectionView.as_view(), name='login_redirect'),
    path('accounts/', include('accounts.urls')),
    path('diaryRecords/', include('diaryRecords.urls')),
    path('projects/', include('projects.urls')),
    path('admin/', admin.site.urls),
    path('error/', include('error.urls')),
    #url(r'^.*$', Error404View.as_view(), name="404Error")
]

urlpatterns += static(
   settings.STATIC_URL,
   document_root=settings.STATIC_ROOT
)

urlpatterns += static(
   settings.MEDIA_URL,
   document_root=settings.MEDIA_ROOT
)

# handler404 = 'error.views.error404'
# handler500 = 'error.views.error500'
