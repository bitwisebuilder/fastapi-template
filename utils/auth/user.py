import bcrypt


def hash_password(password):
    # Generate a salt
    salt = bcrypt.gensalt(rounds=12)
    # Generate a hash
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed


def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode("utf-8"), hashed_password)


def valid_password(user, password):
    if not check_password(user.password.encode("utf-8"), password):
        return False
    return True
