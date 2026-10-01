#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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

from typing import List, Union

import pyrogram
from pyrogram import raw, enums
from pyrogram import types
from ..object import Object


class ChatPreview(Object):
    """A chat preview.

    Parameters:
        title (``str``):
            Title of the chat.

        type (:obj:`~pyrogram.enums.ChatType` | ``str``):
            Type of chat, can be either GROUP, SUPERGROUP or CHANNEL.

        members_count (``int``):
            Chat members count.

        photo (:obj:`~pyrogram.types.Photo`, *optional*):
            Chat photo.

        members (List of :obj:`~pyrogram.types.User`, *optional*):
            Preview of some of the chat members.

        request_needed (``bool``, *optional*):
            True, if admin approval is required to join this chat.

        is_join_request (``bool``, *optional*):
            Alias to request_needed. True, if admin approval is required to join this chat.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        title: str,
        type: Union[str, "enums.ChatType"],
        members_count: int,
        photo: "types.Photo" = None,
        members: List["types.User"] = None,
        request_needed: bool = False,
        is_join_request: bool = False
    ):
        super().__init__(client)

        if isinstance(type, str):
            type_str = type.upper()
            if hasattr(enums.ChatType, type_str):
                type = getattr(enums.ChatType, type_str)

        self.title = title
        self.type = type
        self.members_count = members_count
        self.photo = photo
        self.members = members
        self.request_needed = bool(request_needed or is_join_request)
        self.is_join_request = self.request_needed

    @staticmethod
    def _parse(client, chat_invite: "raw.types.ChatInvite") -> "ChatPreview":
        chat_type = (
            enums.ChatType.GROUP if not chat_invite.channel else
            enums.ChatType.CHANNEL if chat_invite.broadcast else
            enums.ChatType.SUPERGROUP
        )
        req_needed = bool(getattr(chat_invite, "request_needed", False))
        return ChatPreview(
            title=chat_invite.title,
            type=chat_type,
            members_count=chat_invite.participants_count,
            photo=types.Photo._parse(client, chat_invite.photo),
            members=[types.User._parse(client, user) for user in chat_invite.participants] or None,
            request_needed=req_needed,
            is_join_request=req_needed,
            client=client
        )

    # TODO: Maybe just merge this object into Chat itself by adding the "members" field.
    #  get_chat can be used as well instead of get_chat_preview
