import os, logging
from aiogram import Dispatcher
from aiogram.types import ChatMemberUpdated

from tgbot.services.backend import Backend
from tgbot.services.notification import Notification

LOBBY_CHANNEL_ID = int(os.environ["lobby_channel_id"])

logger = logging.getLogger('CHANNEL_HANDLERS')

# Teachers Lobby
async def handle_lobby_member(chat_member: ChatMemberUpdated, notification: Notification, backend: Backend):
    if chat_member.chat.type == 'channel' and chat_member.chat.id == LOBBY_CHANNEL_ID:
        if chat_member.new_chat_member.status == 'member':
            await backend.student_to_teacher(chat_member.new_chat_member.user.id)
            await notification.student_promoted_to_teacher(chat_member.new_chat_member.user)
        elif chat_member.new_chat_member.status == 'left' or chat_member.new_chat_member.status == 'kicked':
            await backend.teacher_to_student(chat_member.new_chat_member.user.id)
            await notification.teacher_downgraded_to_student(chat_member.new_chat_member.user)
        logger.info(chat_member.new_chat_member.status)

def register_channel(dp: Dispatcher):
    # Teachers Lobby
    dp.register_chat_member_handler(handle_lobby_member)