from typing import List
from aiogram.types import LabeledPrice, ShippingOption

class Payment:
    """Payment abstraction layer"""

    def __init__(self, token, bot, user_id):
        self.token = token
        self.bot = bot
        self.user_id = user_id
        # Setup prices
        self.prices = [
            # LabeledPrice(label='Общий тариф - 5 занятий', amount=1500),
            # LabeledPrice(label='Общий тариф - 15 занятий', amount=45000),
            LabeledPrice(label='Индивидуальный тариф - 5 занятий', amount=25000),
            # LabeledPrice(label='Индивидуальный тариф - 15 занятий', amount=75000)
        ]

        # Setup shipping options
        self.shipping_options = [
            # ShippingOption(id='instant', title='WorldWide Teleporter').add(types.LabeledPrice('Teleporter', 1000)),
            ShippingOption(id='pickup', title='Local pickup').add(LabeledPrice('Pickup', 300)),
        ]

    # invoice
    async def send_invoice(self):
        return await self.bot.send_invoice(
            self.user_id,
            title='Engilsh Assistant Payment',
            description='Занимайся английским уже сегодня!',
            provider_token=self.token,
            currency='rub',
            photo_url='https://play-lh.googleusercontent.com/ua4n3IdS75qg_3zlFPHjnIZaVhXwR-kvULxW5oZDrUTFXdi-3unst4FuE0ac77ECnA',
            photo_height=300,  # !=0/None or picture won't be shown
            photo_width=300,
            photo_size=300,
            is_flexible=False,  # True If you need to set up Shipping Fee
            prices=self.prices,
            start_parameter='english-assistant-example',
            payload='ENGLISH LESSONS'
        )
    async def answer_shipping_query(self, shipping_query_id):
        return await self.bot.answer_shipping_query(shipping_query_id, ok=True, shipping_options=self.shipping_options, error_message="Oh, seems like our Dog couriers are having a lunch right now.\nTry again later!")

    async def answer_pre_checkout_query(self, pre_checkout_query_id):
        return await self.bot.answer_pre_checkout_query(pre_checkout_query_id, ok=True, error_message="Aliens tried to steal your card's CVV,\nbut we successfully protected your credentials,\ntry to pay again in a few minutes, we need a small rest.")
