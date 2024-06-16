from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.conf.urls.static import static

from search.views import *

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path('', HomeView.as_view(), name="home_view"),
    path('post', PostView.as_view(), name="post_view"),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', RegisterView.as_view(), name="signup"),
    path('profile/<int:pk>/', ProfileView.as_view(), name="profile"),
    path('profile/<int:pk>/edit/', EditProfileView.as_view(), name="edit_profile"),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('posts/delete/<int:post_id>/', DeletePostView.as_view(), name='delete_post'),
    path('support/', SupportView.as_view(), name="support"),
    path('about/', AboutUs.as_view(), name="about"),
    path('reviews/', Reviews.as_view(), name="reviews"),
    path('support_creators/', SupportCreators.as_view(), name="support_creators"),
    path('user/follow/<int:pk>/', ProfileFollowingCreateView.as_view(), name='follow'),
    path('posts/', post_list, name='post_list')

    # path('', include('allauth.urls')),
    # path('create_profile/',CreateProfilePageView.as_view(), name='create_user_profile'),
    # path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='user_profile'),
    # path('edit_profile/<int:pk>/', EditProfilePageView.as_view(), name='edit_user_profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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
