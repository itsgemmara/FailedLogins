
def activate_user_account( user, main_code, verify_code):
    if main_code.code == verify_code:
        user.is_locked, user.is_active = False, True
        main_code.is_expired, main_code.used = True, True
        main_code.save()
        user.save()
    else:
        raise Exception('invalid code')


