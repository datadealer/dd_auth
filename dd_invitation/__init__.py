from allauth.account.signals import user_signed_up
from dd_invitation import admin_views as invitation


def consume_invite_token(sender, **kwargs):
    request = kwargs.get('request', None)
    user = kwargs.get('user', None)
    if request is not None:
        token = request.session.get('invitation_token', None)
        if token is not None:
            request.session['invitation_token'] = None
            invitation.consume_token(request, token, extra_user=user)

user_signed_up.connect(consume_invite_token, dispatch_uid='dd_user_signed_up_consume_token')
