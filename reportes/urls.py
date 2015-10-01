from django.conf.urls import patterns, include, url
from django.contrib import admin
from reports.views import getDay, getReports, getMonth
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Examples:
    url(r'^day$', getDay),
    url(r'^month$', getMonth),
    url(r'^$', getReports),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()