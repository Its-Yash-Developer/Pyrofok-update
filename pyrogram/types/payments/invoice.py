#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union

from pyrogram import raw
from ..object import Object


class Invoice(Object):
    """Contains information about an Invoice.

    Parameters:
        title (``str``):
            Product name.

        description (``str``):
            Product description.

        currency (``str``):
            Currency code.

        total_amount (``int``):
            Total price in the smallest units of the currency.

        start_parameter (``str``):
            Unique bot deep-linking parameter that can be used to generate this invoice.

        shipping_address_requested (``bool``, *optional*):
            True, if the the shipping address is requested.

        test (``bool``, *optional*):
            True, if the invoice is a test invoice.

        receipt_message_id (``int``, *optional*):
            The message_id of the message sent to the chat when the invoice is paid.
    """

    def __init__(
        self,
        *,
        currency: str,
        total_amount: int,
        title: str = None,
        description :  str = None,
        start_parameter: str = None,
        shipping_address_requested: bool = None,
        test: bool = None,
        receipt_message_id: int = None,
        # TODO: Implement photo, extended_media parameters
    ):
        super().__init__()

        self.title = title
        self.description = description
        self.currency = currency
        self.total_amount = total_amount
        self.start_parameter = start_parameter
        self.shipping_address_requested = shipping_address_requested
        self.test = test
        self.receipt_message_id = receipt_message_id

    @staticmethod
    def _parse(
        invoice: Union["raw.types.MessageMediaInvoice", "raw.types.Invoice"]
    ) -> "Invoice":
        if isinstance(invoice, raw.types.MessageMediaInvoice):
            return Invoice(
                title=invoice.title,
                description=invoice.description,
                currency=invoice.currency,
                total_amount=invoice.total_amount,
                start_parameter=invoice.start_param,
                shipping_address_requested=getattr(invoice, 'shipping_address_requested', None),
                test=getattr(invoice, 'test', None),
                receipt_message_id=getattr(invoice, 'receipt_msg_id', None)
            )

        total_amount = sum(p.amount for p in invoice.prices)

        return Invoice(
            currency=invoice.currency,
            total_amount=total_amount,
            shipping_address_requested=getattr(invoice, 'shipping_address_requested', None),
            test=getattr(invoice, 'test', None)
        )
