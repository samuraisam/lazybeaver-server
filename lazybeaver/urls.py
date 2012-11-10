from django.conf.urls import patterns, include, url
import beaver.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lazybeaver.views.home', name='home'),
    # url(r'^lazybeaver/', include('lazybeaver.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/logs/?', beaver.views.Logs.as_view())
)
