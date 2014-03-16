from django.core.management.base import BaseCommand
#from optparse import make_option
from django.conf import settings
from dd_auth.dd_user_sync.utils import user_mapper

# FIXME probably totally obsolete

class Command(BaseCommand):
    """This is for debugging purposes ONLY; produces a horrible amount of db hits to stay consistent"""
    args = ''
    help = """Sync userdata to mongodb"""
    option_list = BaseCommand.option_list + (
#        make_option('-r', '--remove', action='store_true', dest='remove', default=False, help='remove stale userdata'),
    )

    def handle(self, *args, **options):
        import pymongo
        from django.contrib.auth.models import User

        mongoconf = getattr(settings, 'DD_MONGO_DB')

        users = User.objects.filter(is_superuser=False)

        connection = pymongo.Connection(mongoconf.get('host', 'localhost'),
                                        mongoconf.get('port', 27017),
                                        mongoconf.get('max_pool_size', 10),
                                        network_timeout=None,
                                        tz_aware=True)
        db = connection[mongoconf.get('db')]
        mongousers = db[mongoconf.get('users_collection')]
        # ensure index
        mongousers.ensure_index('auth_uid', unique=True)
        mongousers.ensure_index('auth_username', unique=True)

        def get_auth_uids(result):
            return (r.get('auth_uid') for r in result if r.get('auth_uid', None) is not None)

        def get_userdoc_by_uid(myuid):
            userdocs = [user_mapper(user) for user in users if user.id==myuid]
            if userdocs:
                return userdocs[0]
            else:
                print "Failed getting user data for %s" % myuid

        auth_uids = set(users.values_list('id', flat=True))

        for uid in auth_uids:
            if uid in get_auth_uids(mongousers.find()):
                # update
                userdoc = get_userdoc_by_uid(uid)
                if userdoc:
                    mongousers.update({'auth_uid': uid}, {"$set": userdoc, "$inc": {'version': 1}}, safe=True)
                    print "Updated %s" % uid
            else:
                # insert
                newdoc = get_userdoc_by_uid(uid)
                newdoc.update({'version':0})
                mongousers.insert(newdoc, safe=True)
                print "Added %s" % uid
        for uid in get_auth_uids(mongousers.find({'auth_is_active': True})):
            if uid not in auth_uids:
                # remove
                #mongousers.remove({'auth_uid': uid}, safe=True)
                mongousers.update({'auth_uid': uid, "auth_is_active": True}, {"$set": {"auth_is_active": False, 'auth_is_removed': True}}, safe=True)
                print "Removing %s" % uid

        connection.close()
