from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djangoServer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^app/', include('app.urls', namespace="app")),
	url(r'^rankService/', include('rankService.urls', namespace="rankService")),
	#url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),
)
