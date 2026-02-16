import uuid
import re
from rest_framework_simplejwt.tokens import RefreshToken
import string
from random import choice


def hex_uuid():
    return uuid.uuid4().hex


def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long"
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one digit"
    if not any(char.isalpha() for char in password):
        return "Password must contain at least one letter"
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter"
    return None


# validate not more than two words
def validate_not_more_than_two_words(text):
    return len(text.split()) > 2


def validate_email(email):
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        return "Invalid email address"
    return None


def get_serializer_errors(serializer):
    first_field, first_error = next(iter(serializer.errors.items()))
    if first_field.lower() in ["password", "first_name", "last_name", "address"]:
        return f"{first_field.title()}: {first_error[0]}".replace("This", "")
    return first_error[0]


# get token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def generate_random_string(length=20):
    characters = string.ascii_letters + string.digits
    random_string = "".join(choice(characters) for _ in range(length))
    return random_string
