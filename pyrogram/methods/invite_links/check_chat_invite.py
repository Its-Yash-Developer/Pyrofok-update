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

from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram import utils


class CheckChatInvite:
    async def check_chat_invite(
        self: "pyrogram.Client",
        invite_link: str
    ) -> Union["types.ChatPreview", "types.Chat"]:
        """Check a chat invite link to get information about it before joining.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            invite_link (``str``):
                The invite link (in the format *https://t.me/+AbCdEf0123456789* or *https://t.me/joinchat/AbCdEf0123456789*)
                or the invite hash itself.

        Returns:
            :obj:`~pyrogram.types.ChatPreview` | :obj:`~pyrogram.types.Chat`: On success, if you haven't joined yet,
            a chat preview object is returned. If you are already a participant, a chat object is returned.

        Example:
            .. code-block:: python

                preview = await app.check_chat_invite("https://t.me/+AbCdEf0123456789")
                print(preview.title)
                print(preview.request_needed)
                print(preview.is_join_request)
        """
        match = self.INVITE_LINK_RE.match(str(invite_link))
        invite_hash = match.group(1) if match else str(invite_link).lstrip("+")

        r = await self.invoke(
            raw.functions.messages.CheckChatInvite(
                hash=invite_hash
            )
        )

        if isinstance(r, raw.types.ChatInvite):
            return types.ChatPreview._parse(self, r)

        chat_id = None
        if hasattr(r, "chat") and r.chat:
            await self.fetch_peers([r.chat])
            if isinstance(r.chat, raw.types.Chat):
                chat_id = -r.chat.id
            elif isinstance(r.chat, raw.types.Channel):
                chat_id = utils.get_channel_id(r.chat.id)

        if chat_id:
            try:
                peer = await self.resolve_peer(chat_id)
                if isinstance(peer, raw.types.InputPeerChannel):
                    full = await self.invoke(raw.functions.channels.GetFullChannel(channel=peer))
                elif isinstance(peer, (raw.types.InputPeerUser, raw.types.InputPeerSelf)):
                    full = await self.invoke(raw.functions.users.GetFullUser(id=peer))
                else:
                    full = await self.invoke(raw.functions.messages.GetFullChat(chat_id=peer.chat_id))
                return await types.Chat._parse_full(self, full)
            except Exception:
                if hasattr(r, "chat") and r.chat:
                    return types.Chat._parse_chat(self, r.chat)

        if hasattr(r, "chat") and r.chat:
            return types.Chat._parse_chat(self, r.chat)

        return r
