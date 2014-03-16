def user_mapper(user):
    udoc = {
        'auth_uid': user.id,
        'auth_username': user.username,
        'auth_email': user.email,
        'auth_fullname': user.get_full_name(),
        'auth_date_joined': user.date_joined,
        'auth_last_login': user.last_login,
        'auth_is_active': user.is_active,
        'mail': tuple(user.emailaddress_set.values('verified', 'primary', 'email')),
    }
    socialaccounts = user.socialaccount_set.all()
    social_data = {}
    for sa in socialaccounts:
        spa = sa.get_provider_account()
        social_data.update({sa.provider: {  'avatar_url': sa.get_avatar_url(),
                                            'profile_url': sa.get_profile_url(),
                                            'screen_name': unicode(spa),
                                            'provider_name': spa.get_brand().get('name', ''),
                                            'extra_data': sa.extra_data
                                         }
                            })
    udoc.update({'social_data': social_data})
    return udoc
