from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', 'hello.views.home', name='home'),
    url(r'^requests/$', 'hello.views.requests', name='requests'),
    url(r'^get_requests/$', 'hello.views.get_requests', name='get_requests'),
    url(r'^contact_form/$', 'hello.views.contact_form', name='contact_form'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
