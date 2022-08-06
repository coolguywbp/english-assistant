import sys, time, logging, yaml, random
from typing import List

from aiohttp import ClientSession

class Error(Exception):
    """Base class for other exceptions"""
    pass


class UserIsNotCreated(Error):
    """Raised when User doesn't exist"""
    pass
class Backend:
    """Backend abstraction layer"""

    def __init__(self, host):
        self.host = host
        self.logger = logging.getLogger('BACKEND')
        self.session = ClientSession()

    # users
    async def create_user(self, telegram_id, telegram_username=None, first_name=None, last_name=None) -> None:
        """Создает User, делает его учеником"""
        params = {'telegram_id': telegram_id, 'telegram_username': telegram_username, 'first_name': first_name, 'last_name': last_name}
        async with self.session.post(self.host + f'users/', params=params) as response:
            result = await response.json()
        return result

    async def get_user(self, telegram_id) -> List[int]:
        """Получает User по telegram_id"""
        async with self.session.get(self.host + f'users/{str(telegram_id)}/') as response:
            result = await response.json()
            if response.status == 404 and result['message'] == "User doesn't exists":
                raise UserIsNotCreated
        self.logger.info(result['user_type'])
        return result
