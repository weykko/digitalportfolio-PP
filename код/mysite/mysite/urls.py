from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search.views import *

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path('', include('allauth.urls')),
    path('create_profile/',CreateProfilePageView.as_view(), name='create_user_profile'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='user_profile'),
    path('edit_profile/<int:pk>/', EditProfilePageView.as_view(), name='edit_user_profile'),
    path('', HomeView.as_view(), name="home_view"),
    path('post', PostView.as_view(), name="post_view"),
    path('post-comment/', PostCommentView.as_view()),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
