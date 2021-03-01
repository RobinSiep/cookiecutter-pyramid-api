from marshmallow import (fields, post_load, Schema, validate, validates,
                         validates_schema, ValidationError)

from {{cookiecutter.project_slug}}.lib.hash import compare_plaintext_to_hash, hash_plaintext
from {{cookiecutter.project_slug}}.models.user import User, get_user_by_email_address

MIN_PASSWORD_LENGTH = 8


class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    email_address = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True,
                          validate=validate.Length(min=MIN_PASSWORD_LENGTH))

    @validates('email_address')
    def check_if_email_unique(self, value):
        if get_user_by_email_address(value):
            raise ValidationError(
                "A user with this email address already exists."
            )

    def hash_password(self, data, **kwargs):
        data['password_hash'], data['password_salt'] = hash_plaintext(
            data.pop('password')
        )
        return data


class CreateUserSchema(UserSchema):
    @post_load
    def create_user(self, data, **kwargs):
        return User(**self.hash_password(data))


class UpdateUserSchema(UserSchema):
    current_password = fields.Str(load_only=True)

    def __init__(self, user: User = None,
                 requires_current_password: bool = True,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context['user'] = user
        self.context['requires_current_password'] = requires_current_password

    @validates_schema
    def validate_current_password_if_required(self, data, **kwargs):
        if (not data.get('password') or
                not self.context['requires_current_password']):
            return

        try:
            current_password = data['current_password']
        except KeyError:
            raise ValidationError(
                "This field is required when setting a new password",
                'current_password'
            )

        self.validate_current_password(current_password)

    def validate_current_password(self, current_password):
        context_user = self.context['user']

        if not compare_plaintext_to_hash(
            current_password,
            context_user.password_hash,
            context_user.password_salt
        ):
            raise ValidationError(
                "Given password is incorrect",
                'current_password'
            )

    @post_load
    def hash_password(self, data, **kwargs):
        try:
            return super().hash_password(data)
        except KeyError:
            # No password, which is fine since it's not required.
            pass
