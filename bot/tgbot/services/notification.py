import sys, time, logging, yaml, random
from typing import List

class Notification:
    """Notification abstraction layer"""

    def __init__(self, bot, lobby_channel_id):
        self.bot = bot
        self.lobby_channel_id = lobby_channel_id
        self.logger = logging.getLogger('NOTIFICATION')
        
    async def student_promoted_to_teacher(self, user):
        """Send notification to private chat and to lobby channel"""
        await self.bot.send_message(self.lobby_channel_id, f'Welcome {user.first_name} {user.last_name}!')
        await self.bot.send_message(user.id, 'You are now a teacher!')

    async def teacher_downgraded_to_student(self, user):
        """Send notification to private chat and to lobby channel"""
        await self.bot.send_message(self.lobby_channel_id, f'{user.first_name} {user.last_name} is not a teacher anymore.')
        await self.bot.send_message(user.id, 'You are now a student!')