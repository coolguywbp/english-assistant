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

    # Users
    async def create_user(self, telegram_id, telegram_username=None, first_name=None, last_name=None):
        """Create User, make him a Student"""
        params = {'telegram_id': telegram_id, 'telegram_username': telegram_username, 'first_name': first_name, 'last_name': last_name}
        async with self.session.post(self.host + 'users/', params=params) as response:
            result = await response.json()
        return result

    async def get_user(self, telegram_id):
        """Get User via telegram_id"""
        async with self.session.get(self.host + f'users/{str(telegram_id)}/') as response:
            result = await response.json()
            if response.status == 404 and result['message'] == "User doesn't exists":
                raise UserIsNotCreated
        return result
    
    # Promotion/downgrading    
    async def student_to_teacher(self, telegram_id) -> None:
        """Student -> Teacher"""
        params = {'telegram_id': telegram_id}
        async with self.session.post(self.host + 'users/student_to_teacher/', params=params) as response:
            result = await response.json()
        return result
    
    async def teacher_to_student(self, telegram_id) -> None:
        """Teacher -> Student"""
        params = {'telegram_id': telegram_id}
        async with self.session.post(self.host + 'users/teacher_to_student/', params=params) as response:
            result = await response.json()
        return result
    
    # Logs
    
    async def save_chatlog(self, telegram_id, action, content) -> None:
        """Save chatlog"""
        params = {'user': telegram_id, 'action': action, 'content': content}
        async with self.session.post(self.host + 'chatlogs/', json=params) as response:
            result = await response.json()
        return result