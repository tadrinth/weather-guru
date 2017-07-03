from django.conf.urls import include, url

from django.contrib import admin
from django.contrib.auth import views as auth_views

admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
	url(r'^cities/$', hello.views.cities, name='cities'),
	url(r'^cities/subscribe/(?P<id>[0-9]*)$', hello.views.subscribe, name='subscribe'),
	url(r'^cities.unsubscribe/(?P<id>[0-9]*)$', hello.views.unsubscribe, name='unsubscribe'),
    url(r'^db', hello.views.db, name='db'),
	url(r'^signup/$', hello.views.signup, name='signup'),
	url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
]
