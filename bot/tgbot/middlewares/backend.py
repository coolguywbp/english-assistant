from argparse import Action
import logging
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from aiogram.types import CallbackQuery, Message, ChatMemberUpdated
from tgbot.models.role import UserRole
from tgbot.services.backend import UserIsNotCreated

class BackendMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.logger = logging.getLogger('BACKEND_MIDDLEWARE')

    async def pre_process(self, obj, data, *args):
        if isinstance(obj, Message):
            text = obj.text or obj.caption or ''
            
            telegram_id = obj.from_user.id
            telegram_username = obj.from_user.username
            first_name = obj.from_user.first_name
            last_name = obj.from_user.last_name
            
            if not text and obj.poll:
                text = obj.poll.question
            
            # Typing imitation
            await self.manager.bot.send_chat_action(telegram_id, action='TYPING')
        elif isinstance(obj, CallbackQuery):
            text = obj.data
            telegram_id = obj.chat.id
            
        data["role"] = None
        data["user"] = None
        data["backend"] = self.backend
        
        """Getting User and setting up Role in private chat"""
        if (obj.chat.type == 'private'):
            try:
                user = await self.backend.get_user(telegram_id)
            except UserIsNotCreated:
                """If user is not created, create new student account (yes, inside middleware)"""
                user = await self.backend.create_user(telegram_id, telegram_username=telegram_username, first_name=first_name, last_name=last_name)
            
            # Saving chatlog
            await self.backend.save_chatlog(telegram_id, 'message', text)
            data["user"] = user
            
            if not getattr(obj, "from_user", None):
                data["role"] = None
            elif user['user_type'] == 'admin':
                data["role"] = UserRole.ADMIN
            elif user['user_type'] == 'teacher':
                data["role"] = UserRole.TEACHER
            elif user['user_type'] == 'student':
                data["role"] = UserRole.STUDENT
        
    async def post_process(self, obj, data, *args):
        del data["role"]
        del data["backend"]
        del data["user"]
