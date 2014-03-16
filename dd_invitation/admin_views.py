from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect

from dd_invitation import models

from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@staff_member_required
def make_tokens(request):
  default_amount = 10
  amount = int(request.GET['amount']) if 'amount' in request.GET else default_amount
  for i in range(amount or default_amount):
    models.Token().save()
  return HttpResponseRedirect('./')

def is_valid_token(request, token):
  try:
    models.Token.objects.get(value=token, consumed=None)
    return True
  except models.Token.DoesNotExist:
    return False

def consume_token(request, token, extra_user=None):
  tokenobj = models.Token.objects.get(value=token, consumed=None)
  tokenobj.consumed = datetime.now()
  tokenobj.save()
  if extra_user is None:
      extra_user = request.user
  logger.error('Consumed token',
               extra={
                   'token': token,
                   'request': request,
                   'username': extra_user.username
               })

