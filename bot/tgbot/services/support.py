from typing import List

class Support:
    """Support abstraction layer"""
    def __init__(self, bot, support_channel_id, bot_signature):
        self.bot = bot
        self.support_channel_id = support_channel_id
        self.bot_signature = bot_signature

    async def log_fallback(self, user_id, text):
        response = f'❗️ Сообщение от #id{user_id}:\n\n"{text}"\n\nне распознано, внесите изменения в модель Rasa'
        await self.bot.send_message(self.channel_id, response)
    
    async def start_issue(self, m, text):
        username = m.from_user.username
        user_id = m.from_user.id
        link = self._get_student_link(user_id, username)
        issue_text = f'Проблема у {link} #id{user_id}:\n{text}'
        await self.bot.send_message(self.support_channel_id, issue_text)
        
    async def answer_issue(self, m):
        answer = m.text
        forward_signature = m.reply_to_message.forward_signature
        if forward_signature == self.bot_signature:
            reply_text = m.reply_to_message.text
            title = reply_text.split('\n')[0]
            after_id = title.split('#id')[1]
            user_id = int(after_id[:-1])
        await self.bot.send_message(user_id, answer)
        
    def _get_student_link(self, user_id, username):
        return f'<a href="tg://user?id={user_id}">{username}</a>'
