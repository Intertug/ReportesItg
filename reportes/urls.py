from django.conf.urls import patterns, include, url
from django.contrib import admin
from prints.views import getReportes

urlpatterns = patterns('',
    # Examples:
    url(r'^$', getReportes),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
