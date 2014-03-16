from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView


from jsonrpc import jsonrpc_site
import dd_auth.views

# Uncomment the next line for overwriting templates
#from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #Admin Urls
    #url(r'^dd_auth_admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^dd_auth_admin/dd_invitation/token/make$', 'dd_invitation.admin_views.make_tokens'),
    url(r'^dd_auth_admin/', include(admin.site.urls)),

    url(r'^accounts/i18n/', include('django.conf.urls.i18n'), name="set_language"),
    url(r'^accounts/lang/$', TemplateView.as_view(template_name='account/setlang.html')),
    url(r'^accounts/remote/access_denied/$', TemplateView.as_view(template_name='account/access_denied.html')),

    # JSON-RPC URLs
#    url(r'^authapi/browse/', 'jsonrpc.views.browse', name="jsonrpc_browser"),
    url(r'^authapi/$', jsonrpc_site.dispatch, name="jsonrpc_mountpoint"),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/remote/sign_in/$', 'dd_auth.views.sign_in', {'template_name': 'account/sign_in.html'}, name='remote_sign_in'),
    url(r'^accounts/remote/sign_up/$', 'dd_auth.views.sign_up', {'template_name': 'account/sign_up.html'}, name='remote_sign_up'),
    url(r'^accounts/remote/reset/$', 'dd_auth.views.reset_password', {'template_name': 'account/reset.html'}, name='remote_reset_password'),
    url(r'^accounts/remote/sign_out/$', 'dd_auth.views.sign_out', name='remote_sign_out'),
    url(r'^accounts/remote/set_email/$', 'dd_auth.views.set_email', name='remote_set_email')
)

if getattr(settings, 'DD_SERVE_STATIC', False):
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
