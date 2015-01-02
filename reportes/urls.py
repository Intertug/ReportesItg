from django.conf.urls import patterns, include, url
from django.contrib import admin
from reports.views import getReportes, getDia

urlpatterns = patterns('',
    # Examples:
    url(r'^$', getReportes),
    url(r'^dia$', getDia),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
