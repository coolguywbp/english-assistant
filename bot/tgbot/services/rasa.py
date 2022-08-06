import sys, time, logging, yaml, random
from typing import List

import langid

from aiohttp import ClientSession

class Rasa:
    """Rasa abstraction layer"""
    def __init__(self, bot, log_channel_id):
        self.bot = bot
        self.logger = logging.getLogger('RASA')

        self.session = ClientSession()        
        self.nlu_server = "http://172.17.0.1:5005/model/parse" if 'docker' in sys.argv[1:] else "http://localhost:5005/model/parse"
        
        self.debug = True if 'rasa-debug' in sys.argv[1:] else False
        self.log_to_channel = True
        self.log_channel_id = log_channel_id

        with open('tgbot/services/responses.yml', 'r', encoding='utf-8') as stream:
            data = yaml.safe_load(stream)
            self.responses = data['responses']
            self.actions = data['actions']

    async def get_intent(self, user_id, text):
        result = await self.get_data(user_id, text)
        intent = result['intent']
        return intent['name']


    async def get_data(self, user_id, text):
        lang = self._detect_language(text)
        params = {'text': text}
        if self.debug:
            start = time.time()
            async with self.session.post(self.nlu_server, json=params) as response:
                result = await response.json()
            end = time.time()
            self.logger.info(f"NLU Server response time: {end - start}")
        else:
            async with self.session.post(self.nlu_server, json=params) as response:
                result = await response.json()
        intent = result['intent']
        result['response'] = await self._get_intent_response(intent['name'], lang)
        if self.log_to_channel: await self._log_to_training_channel(user_id, text, intent['name'], result['response'])
        return result

    async def _log_to_training_channel(self, user_id, text, intent, response):
        log = f'<a href="tg://user?id={user_id}">{user_id}</a>\n\n<b>User:</b> {text}\n<b>Rasa:</b> {response}\n\nIntent: <code>{intent}</code>'
        await self.bot.send_message(self.log_channel_id, log)
    
    async def _get_intent_response(self, intent, lang):
        if intent in self.actions:
            return f'ACTION -> <b>{intent.upper()}</b>'     
        for response in self.responses:
            if response['intent'] == intent:
                responses = response[lang].split('\n')[:-1]
                return random.choice(responses)        
        return f'Response not stated'

    def _detect_language(self, text):
        if self.debug:
            start = time.time()
            data = langid.classify(text)
            end = time.time()
            self.logger.info(f"Language detection: {data} Time: {end - start}")
        else:
            data = langid.classify(text)
        lang = data[0]
        if lang in ['ru', 'en']: return lang
        return 'ru'
