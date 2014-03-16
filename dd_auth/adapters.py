from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponse
from django.conf import settings

class DDAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        if getattr(settings, 'INVITATION_REQUIRED', False) is False:
            # invitation checks deactivated
            return True
        token = request.session.get('invitation_token', None)
        if token is None:
            response = HttpResponse()
            if request.is_ajax():
                response.status_code = 278
            else:
                response.status_code = 302
            url = getattr(settings, 'INVITATION_FAILED', '#access_denied')
            response['Location'] = url
            raise ImmediateHttpResponse(response)
        else:
            return True
        return False
