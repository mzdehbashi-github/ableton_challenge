from rest_framework.exceptions import APIException

from django.utils.translation import gettext_lazy as _


class UnprocessableContent(APIException):
    status_code = 422
    default_detail = _('unable to process the contained instructions.')
    default_code = 'unprocessable_content'
