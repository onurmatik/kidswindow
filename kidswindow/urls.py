from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.utils.translation import ugettext as _
from django.contrib.auth.views import LoginView
from kidswindow.meetings.views import meeting_list, meeting_detail, meeting_create
from kidswindow.profiles.views import signup, AuthForm, activate
from kidswindow.views import IndexView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=AuthForm
    ), name='auth'),
    path('accounts/login/', RedirectView.as_view(pattern_name='auth', permanent=True)),  # redirect to reCAPTCHA login
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),

    path('', IndexView.as_view(), name='index'),

    path('meetings/form/', meeting_create, name='meeting_create'),
    path('meetings/<slug:meeting_slug>/', meeting_detail, name='meeting_detail'),
    path('meetings/', meeting_list, name='meeting_list'),

    path('docs/about/', TemplateView.as_view(template_name='docs/details.html'), name='docs_details'),
]


admin.site.index_title = _('Kids Window')
admin.site.site_header = _('Kids Window Administration')
admin.site.site_title = _('Kids Window Management')
