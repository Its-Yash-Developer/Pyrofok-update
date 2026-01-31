import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from pyrogram import Client, raw
from pyrogram.file_id import FileType

@pytest.mark.asyncio
async def test_send_video_cover_with_file_id():
    api_id = 12345
    api_hash = "test_hash"
    client = Client("test_session", api_id=api_id, api_hash=api_hash, in_memory=True)

    # Mocking client methods
    client.invoke = AsyncMock()
    # Mocking Update object to be returned by invoke if needed, but the method handles return values from updates
    # We can mock invoke to return an object with updates
    mock_response = MagicMock()
    mock_response.updates = []
    client.invoke.return_value = mock_response

    client.resolve_peer = AsyncMock(return_value=raw.types.InputPeerUser(user_id=123, access_hash=456))
    client.save_file = AsyncMock()
    client.rnd_id = MagicMock(return_value=123456789)
    client.guess_mime_type = MagicMock(return_value="video/mp4")

    # Mocking utils
    with patch("pyrogram.utils.get_input_media_from_file_id") as mock_get_input_media:
        with patch("pyrogram.utils.get_reply_to", new_callable=AsyncMock) as mock_get_reply_to:
            with patch("pyrogram.utils.parse_text_entities", new_callable=AsyncMock) as mock_parse_text:
                with patch("pyrogram.utils.datetime_to_timestamp") as mock_dt_ts:

                    mock_parse_text.return_value = {"message": "", "entities": None}
                    mock_dt_ts.return_value = None
                    mock_get_reply_to.return_value = None

                    # Setup mocks for media objects
                    mock_cover_media = MagicMock(spec=raw.types.InputMediaPhoto)
                    mock_cover_media.id = MagicMock(spec=raw.types.InputPhoto) # This is the vidcover_file

                    mock_video_media = MagicMock(spec=raw.types.InputMediaDocument)
                    # Initialize video_cover as None to ensure it gets set
                    mock_video_media.video_cover = None

                    def side_effect(file_id, file_type, **kwargs):
                        if file_type == FileType.PHOTO:
                            return mock_cover_media
                        elif file_type == FileType.VIDEO:
                            return mock_video_media
                        return MagicMock()

                    mock_get_input_media.side_effect = side_effect

                    video_file_id = "video_file_id_123"
                    cover_file_id = "photo_file_id_456"
                    chat_id = "me"

                    await client.send_video(chat_id, video=video_file_id, cover=cover_file_id)

                    assert client.invoke.called
                    call_args = client.invoke.call_args[0][0]
                    assert isinstance(call_args, raw.functions.messages.SendMedia)

                    # Verify that video_cover was set on the video media object
                    assert mock_video_media.video_cover == mock_cover_media.id
