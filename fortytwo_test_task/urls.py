from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'hello.views.home', name='home'),
    url(r'^requests/$', 'hello.views.requests', name='requests'),
    url(r'^get_requests/$', 'hello.views.get_requests', name='get_requests'),
    url(r'^contact_form/$', 'hello.views.contact_form', name='contact_form'),
    url(r'^team_form/$', 'hello.views.team_form', name='team_form'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': 'home'}, name='logout'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'contact.html'}, name='login'),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
