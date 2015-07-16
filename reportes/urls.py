from django.conf.urls import patterns, include, url
from django.contrib import admin
from reports.views import ApiReporte, getDay, getReports, getMonth, getDistance
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Examples:
    url(r'^day$', getDay),
    url(r'^month$', getMonth),
    url(r'^distance$', getDistance),
    url(r'^api$', ApiReporte),
    url(r'^$', getReports),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()