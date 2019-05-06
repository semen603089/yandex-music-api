import logging

from yandex_music import YandexMusicObject, Account
from yandex_music.utils.request import Request
from yandex_music.error import InvalidToken


class Client(YandexMusicObject):
    def __init__(self, token, base_url=None, request=None):
        self.token = token
        self.account = None
        self._request = request or Request(token)
        self.logger = logging.getLogger(__name__)

        if base_url is None:
            base_url = 'https://api.music.yandex.net'

        self.base_url = base_url

    @staticmethod
    def _validate_token(token):
        if any(x.isspace() for x in token):
            raise InvalidToken()

        if len(token) != 39:
            raise InvalidToken()

        return token

    @property
    def request(self):
        return self._request

    def account_status(self, timeout=None, **kwargs):
        url = f'{self.base_url}/account/status'

        result = self._request.get(url, timeout=timeout)

        self.account = Account.de_json(result, self)

        return self.account