from django.contrib.auth import User
from django.core import signing

MY_HASH_SALT = 'my_hash_salt'  # any string, given it is the same one on creating and receiving
THREE_DAYS = 3600 * 24 * 3

def send_reset_password_email(username):
	user = User.objects.get(username=username)
	unique_token = signing.dumps(user.username, salt=MY_HASH_SALT)
	# call_my_email_provider(user.email, unique_token, 'reset_password_template')

def reset_password_with_token(new_password, token):
    username = _check_token(token)
    user = User.objects.get(username=username)
    user.set_password(new_password)
    user.save()

def _check_token(token):
    try:
        username = signing.loads(token, salt=MY_HASH_SALT, max_age=THREE_DAYS)
    except signing.SignatureExpired:
        raise Exception('token_expired', more_info={'error': 'expired'})
    except signing.BadSignature:
        raise Exception('token_invalid', more_info={'error': 'invalid'})
    else:
        return username
