# encoding: utf-8

from sso_edx_npoed.backends.npoed import NpoedBackend


def get_username(strategy, details, user=None, backend=None, *args, **kwargs):
    """
    Идём в sso/users/me и получаем логин пользователя.
    """
    user_data = backend.user_data(access_token=details['access_token'])
    username = user_data['username']
    r = {'username': username,
         'first_name': user_data['firstname'],
         'last_name': user_data['lastname']}
    existing_user = backend.strategy.storage.user.get_user(username=username)
    if existing_user:
        r['user'] = existing_user
    return r


def update_user(strategy, details, user=None, backend=None, *args, **kwargs):
    data = kwargs['response']
    if user:
        user.email = data['email']
        user.username = data['username']
        user.first_name = data['firstname']
        user.last_name = data['lastname']
        # user.second_name = data.get('secondname', '')
        user.save()


class CustomNpoedBackend(NpoedBackend):

    name = 'npoedsso'

    PIPELINE = (
        # Get the information we can about the user and return it in a simple
        # format to create the user instance later. On some cases the details are
        # already part of the auth response from the provider, but sometimes this
        # could hit a provider API.
        'social.pipeline.social_auth.social_details',

        # Get the social uid from whichever service we're authing thru. The uid is
        # the unique identifier of the given user in the provider.
        'social.pipeline.social_auth.social_uid',

        # Verifies that the current auth process is valid within the current
        # project, this is were emails and domains whitelists are applied (if
        # defined).
        'social.pipeline.social_auth.auth_allowed',

        # Checks if the current social-account is already associated in the site.
        'social.pipeline.social_auth.social_user',

        # Make up a username for this person, appends a random string at the end if
        # there's any collision.
        #'social.pipeline.user.get_username',
        'authentication.auth.get_username',

        # For updating user data
        'authentication.auth.update_user',

        # Send a validation email to the user to verify its email address.
        # 'social.pipeline.mail.mail_validation',

        # Associates the current social details with another user account with
        # a similar email address.
        # 'social.pipeline.social_auth.associate_by_email',

        # Create a user account if we haven't found one yet.
        'social.pipeline.user.create_user',

        # Create the record that associated the social account with this user.
        'social.pipeline.social_auth.associate_user',

        # Populate the extra_data field in the social record with the values
        # specified by settings (and the default ones like access_token, etc).
        'social.pipeline.social_auth.load_extra_data',

        # Update the user record with any changed info from the auth service.
        'social.pipeline.user.user_details'
    )

