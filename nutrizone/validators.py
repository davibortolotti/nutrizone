from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _, ungettext

class MyPassValidator(object):
    """
    Validate whether the password is of a minimum length.
    """
    def __init__(self, min_length=6):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ungettext(
                    "A senha é muito curta. Deve conter %(min_length)d caracter.",
                    "A senha é muito curta. Deve conter %(min_length)d caracteres.",
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ungettext(
            "Your password must contain at least %(min_length)d character.",
            "Your password must contain at least %(min_length)d characters.",
            self.min_length
        ) % {'min_length': self.min_length}