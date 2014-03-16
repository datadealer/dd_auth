from django.db.models.signals import post_save, post_delete

from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from allauth.account.models import EmailAddress

from django.conf import settings

from allauth.account.signals import user_signed_up, email_confirmed, email_changed, email_added
from django.contrib.auth.signals import user_logged_in

from utils import user_mapper

import pymongo
import bson

mongoconf = getattr(settings, 'DD_MONGO_DB')

class MongoConnector(object):

    def __init__(self, host=mongoconf.get('host', 'localhost'),
                 port=mongoconf.get('port', 27017),
                 max_pool_size=mongoconf.get('max_pool_size', 10),
                 tz_aware=True,
                 db_name=mongoconf.get('db'),
                 users_collection=mongoconf.get('users_collection')):
        self.host = host
        self.port = port
        self.max_pool_size = max_pool_size
        self.tz_aware=tz_aware
        self.db_name=db_name
        self.users_collection=users_collection

    @property
    def connection(self):
        if getattr(self, '_connection', None) is None:
            self._connection = pymongo.mongo_client.MongoClient(host=self.host,
                                                                port=self.port,
                                                                max_pool_size=self.max_pool_size,
                                                                tz_aware=self.tz_aware)
        return self._connection

    @property
    def db_users(self):
        if getattr(self, '_collection', None) is None:
            self._collection = self.connection[self.db_name][self.users_collection]
        return self._collection

    def upsert_user(self, user):
        if user is None:
            raise Exception('No user passed')
        self.db_users.ensure_index('auth_uid', unique=True)
        self.db_users.ensure_index('auth_username', unique=True)
        self.db_users.ensure_index('auth_is_removed', unique=False)
        self.db_users.ensure_index('display_name', unique=False)
        self.db_users.ensure_index([('auth_uid', pymongo.ASCENDING), ('auth_is_active', pymongo.ASCENDING)])
        # generate default display name
        oid = unicode(bson.ObjectId())
        dispname = "Data Dealer %s" % ''.join((oid[:9], oid[-4:]))
        self.db_users.update({'auth_uid': user.id}, {"$set": user_mapper(user), "$inc": {'version': 1}, '$setOnInsert': {'display_name': dispname }}, upsert=True)

    def remove_user(self, user):
        # mark user inactive and/or removed
        if user is None:
            raise Exception('No user passed')
        self.db_users.ensure_index('auth_uid', unique=True)
        self.db_users.ensure_index('auth_username', unique=True)
        self.db_users.ensure_index('auth_is_removed', unique=False)
        self.db_users.ensure_index([('auth_uid', pymongo.ASCENDING), ('auth_is_active', pymongo.ASCENDING)])
        self.db_users.update({'auth_uid': user.id}, {"$set": {'auth_is_active': False, 'auth_is_removed': True}, "$inc": {'version': 1}})

    def upsert_related_user(self, instance):
        try:
            user = instance.user
        except:
            # whoops, user is gone...
            user = None
        if user is not None:
            self.upsert_user(user)


mongo = MongoConnector()

def update_user_handler(sender, **kwargs):
    mongo.upsert_user(kwargs.get('user'))

def update_related_user_handler(sender, **kwargs):
    mongo.upsert_related_user(kwargs.get('instance'))

def update_emailrelated_handler(sender, **kwargs):
    mongo.upsert_related_user(kwargs.get('email_address'))

def user_delete_handler(sender, **kwargs):
    mongo.remove_user(kwargs.get('instance'))

user_signed_up.connect(update_user_handler, dispatch_uid='dd_user_signed_up')
user_logged_in.connect(update_user_handler, dispatch_uid='dd_user_logged_in')
email_changed.connect(update_user_handler, dispatch_uid='dd_email_changed')
email_added.connect(update_user_handler, dispatch_uid='dd_email_added')
email_confirmed.connect(update_emailrelated_handler, dispatch_uid='dd_email_donfirmed')
post_delete.connect(user_delete_handler, sender=User, dispatch_uid='dd_user_delete')
post_delete.connect(update_related_user_handler, sender=EmailAddress, dispatch_uid='dd_email_delete')
post_delete.connect(update_related_user_handler, sender=SocialAccount, dispatch_uid='dd_social_delete')
post_save.connect(update_related_user_handler, sender=SocialAccount, dispatch_uid='dd_social_save')
