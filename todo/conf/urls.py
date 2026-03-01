from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns, set_language

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/setlang/", set_language, name="set_language"),
]
urlpatterns += i18n_patterns(
    path("", include("core.urls", namespace="core")),
)

urlpatterns += [
    path("ckeditor5/", include("django_ckeditor_5.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Панель керування сайтом"
admin.site.index_title = "Панель завдань"
admin.site.site_title = "Проект ToDo"
