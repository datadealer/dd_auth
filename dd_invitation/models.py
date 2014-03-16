from random import random
from hashlib import sha256

from django.db import models

def create_hash(len=32):
  hash_value = sha256()
  salt = random()
  hash_value.update(str(salt))
  return hash_value.hexdigest()[:len]

class Token(models.Model):
  value = models.CharField(max_length=255, default=create_hash, unique=True)
  created = models.DateTimeField('Creation date', auto_now_add=True)
  consumed = models.DateTimeField('Consumption date', blank=True, null=True)
