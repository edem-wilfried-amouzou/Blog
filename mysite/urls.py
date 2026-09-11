from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.http import Http404

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from blog.models import BlogIndexPage


def serve_blog_index(request):
    """Serve BlogIndexPage as the homepage"""
    try:
        blog_index = BlogIndexPage.objects.first()
        if blog_index and blog_index.live:
            return blog_index.serve(request)
    except BlogIndexPage.DoesNotExist:
        pass
    raise Http404("BlogIndexPage not found")


urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # Serve BlogIndexPage as homepage
    # path("", serve_blog_index, name="blog_index_homepage"),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
