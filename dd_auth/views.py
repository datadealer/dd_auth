from django.contrib.auth.models import User

from jsonrpc import jsonrpc_method
from django.http import HttpResponse
from django.conf import settings
from allauth.account import views as account_views
from allauth.socialaccount import views as socialaccount_views

from dd_invitation import admin_views as invitation

def redirect(url = '', is_ajax=True):
  response = HttpResponse()
  if is_ajax:
    response.status_code = 278
  else:
    response.status_code = 302
  response['Location'] = url
  return response

class DDLoginView(account_views.LoginView):

    def get_context_data(self, **kwargs):
        ret = super(DDLoginView, self).get_context_data(**kwargs)
        ret.update({'invite_required': getattr(settings, 'INVITATION_REQUIRED', False)})
        return ret

class DDSignupView(account_views.SignupView):

    def get_context_data(self, **kwargs):
        ret = super(DDSignupView, self).get_context_data(**kwargs)
        ret.update({'invite_required': getattr(settings, 'INVITATION_REQUIRED', False)})
        return ret

def sign_in(request, **kwargs):
  if request.session.get('django_language') != request.LANGUAGE_CODE:
    request.session['django_language'] = request.LANGUAGE_CODE
  view = DDLoginView.as_view(template_name='account/sign_in.html')
  response = view(request, **kwargs)
  if response.status_code == 302:
    return redirect('#load')
  return response

def sign_up(request, **kwargs):
  token_required = getattr(settings, 'INVITATION_REQUIRED', False)
  if token_required:
    token = request.session.get('invitation_token')
    if not token:
      url = getattr(settings, 'INVITATION_FAILED', '#access_denied')
      return redirect(url, is_ajax = request.is_ajax())
  view = DDSignupView.as_view(template_name='account/sign_up.html')
  response = view(request, **kwargs)
  if response.status_code == 302:
    # token gets consumed by DefaultAccountAdapeter
    return redirect('#load', is_ajax=request.is_ajax())
  return response

def reset_password(request, **kwargs):
  view = account_views.PasswordResetView.as_view(template_name='account/reset.html')
  response = view(request, **kwargs)
  #if (response.status_code == 302):
  #  return redirect('#reset_done')
  return response

def sign_out(request, **kwargs):
  view = account_views.LogoutView.as_view()
  response = view(request, **kwargs)
  if (response.status_code == 302):
    return redirect('#sign_in')
  return response

def set_email(request, **kwargs):
  view = socialaccount_views.SignupView.as_view(template_name='socialaccount/sign_up.html')
  response = view(request, **kwargs)
  if (response.status_code == 302):
    return redirect('#load')
  return response

@jsonrpc_method('checkUsername')
def check_username(request, username, **kwargs):
  try:
    User.objects.get(username=username)
    return True
  except User.DoesNotExist:
    return False

@jsonrpc_method('checkInvitationToken')
def check_invitation_token(request, token):
  result = invitation.is_valid_token(request, token)
  request.session['invitation_token'] = token if result else None
  return result

@jsonrpc_method('consumeInvitationToken')
def consume_invitation_token(request, token):
  request.session['invitation_token'] = None
  return invitation.consume_token(request, token)

@jsonrpc_method('debug')
def debug(request, **kwargs):
  if settings.DEBUG is True:
    return unicode(request.session.items())
