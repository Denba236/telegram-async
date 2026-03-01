from typing import Optional, Dict, Any, Union, List
import json
import aiohttp

from ..exceptions import TelegramAPIError, NetworkError


class TelegramMethods:
    """Wszystkie metody API Telegram"""

    async def get_updates(
            self,
            offset: Optional[int] = None,
            limit: int = 100,
            timeout: int = 0,
            allowed_updates: Optional[List[str]] = None
    ) -> List[Dict]:
        """Pobiera aktualizacje z Telegram API"""
        data = {
            'offset': offset,
            'limit': limit,
            'timeout': timeout,
            'allowed_updates': allowed_updates
        }
        return await self._request('getUpdates', data)

    async def send_message(
            self,
            chat_id: Union[int, str],
            text: str,
            parse_mode: Optional[str] = None,
            reply_markup: Optional[Dict] = None,
            disable_web_page_preview: bool = False,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None
    ) -> Dict:
        """Wysyła wiadomość"""
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup,
            'disable_web_page_preview': disable_web_page_preview,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        return await self._request('sendMessage', data)

    async def send_photo(
            self,
            chat_id: Union[int, str],
            photo: Union[str, bytes],
            caption: Optional[str] = None,
            parse_mode: Optional[str] = None,
            reply_markup: Optional[Dict] = None,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None
    ) -> Dict:
        """Wysyła zdjęcie"""
        data = {'chat_id': chat_id}

        if isinstance(photo, str):
            data['photo'] = photo
            if caption:
                data['caption'] = caption
            if parse_mode:
                data['parse_mode'] = parse_mode
            if reply_markup:
                data['reply_markup'] = reply_markup
            if disable_notification:
                data['disable_notification'] = disable_notification
            if reply_to_message_id:
                data['reply_to_message_id'] = reply_to_message_id
            return await self._request('sendPhoto', data)
        else:
            files = {'photo': ('photo.jpg', photo, 'image/jpeg')}
            if caption:
                data['caption'] = caption
            if parse_mode:
                data['parse_mode'] = parse_mode
            if reply_markup:
                data['reply_markup'] = json.dumps(reply_markup)
            if disable_notification:
                data['disable_notification'] = str(disable_notification)
            if reply_to_message_id:
                data['reply_to_message_id'] = str(reply_to_message_id)
            return await self._request('sendPhoto', data, files)

    async def send_document(
            self,
            chat_id: Union[int, str],
            document: Union[str, bytes],
            filename: Optional[str] = None,
            caption: Optional[str] = None,
            parse_mode: Optional[str] = None,
            reply_markup: Optional[Dict] = None,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None
    ) -> Dict:
        """Wysyła dokument"""
        data = {'chat_id': chat_id}

        if isinstance(document, str):
            data['document'] = document
            if caption:
                data['caption'] = caption
            if parse_mode:
                data['parse_mode'] = parse_mode
            if reply_markup:
                data['reply_markup'] = reply_markup
            if disable_notification:
                data['disable_notification'] = disable_notification
            if reply_to_message_id:
                data['reply_to_message_id'] = reply_to_message_id
            return await self._request('sendDocument', data)
        else:
            files = {'document': (filename or 'document.bin', document, 'application/octet-stream')}
            if caption:
                data['caption'] = caption
            if parse_mode:
                data['parse_mode'] = parse_mode
            if reply_markup:
                data['reply_markup'] = json.dumps(reply_markup)
            if disable_notification:
                data['disable_notification'] = str(disable_notification)
            if reply_to_message_id:
                data['reply_to_message_id'] = str(reply_to_message_id)
            return await self._request('sendDocument', data, files)

    async def send_audio(
            self,
            chat_id: Union[int, str],
            audio: Union[str, bytes],
            caption: Optional[str] = None,
            parse_mode: Optional[str] = None,
            duration: Optional[int] = None,
            performer: Optional[str] = None,
            title: Optional[str] = None,
            thumb: Optional[Union[str, bytes]] = None,
            reply_markup: Optional[Dict] = None,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None
    ) -> Dict:
        """Wysyła plik audio"""
        data = {'chat_id': chat_id}

        if isinstance(audio, str):
            data['audio'] = audio
            if caption:
                data['caption'] = caption
            if parse_mode:
                data['parse_mode'] = parse_mode
            if duration:
                data['duration'] = duration
            if performer:
                data['performer'] = performer
            if title:
                data['title'] = title
            if thumb:
                data['thumb'] = thumb
            if reply_markup:
                data['reply_markup'] = reply_markup
            if disable_notification:
                data['disable_notification'] = disable_notification
            if reply_to_message_id:
                data['reply_to_message_id'] = reply_to_message_id
            return await self._request('sendAudio', data)
        else:
            files = {'audio': (filename or 'audio.mp3', audio, 'audio/mpeg')}
            if caption:
                data['caption'] = caption
            if parse_mode:
                data['parse_mode'] = parse_mode
            if duration:
                data['duration'] = str(duration)
            if performer:
                data['performer'] = performer
            if title:
                data['title'] = title
            if thumb:
                files['thumb'] = ('thumb.jpg', thumb, 'image/jpeg')
            if reply_markup:
                data['reply_markup'] = json.dumps(reply_markup)
            if disable_notification:
                data['disable_notification'] = str(disable_notification)
            if reply_to_message_id:
                data['reply_to_message_id'] = str(reply_to_message_id)
            return await self._request('sendAudio', data, files)

    async def send_video(
            self,
            chat_id: Union[int, str],
            video: Union[str, bytes],
            caption: Optional[str] = None,
            parse_mode: Optional[str] = None,
            duration: Optional[int] = None,
            width: Optional[int] = None,
            height: Optional[int] = None,
            thumb: Optional[Union[str, bytes]] = None,
            supports_streaming: bool = False,
            reply_markup: Optional[Dict] = None,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None
    ) -> Dict:
        """Wysyła wideo"""
        data = {'chat_id': chat_id}

        if isinstance(video, str):
            data['video'] = video
            if caption:
                data['caption'] = caption
            if parse_mode:
                data['parse_mode'] = parse_mode
            if duration:
                data['duration'] = duration
            if width:
                data['width'] = width
            if height:
                data['height'] = height
            if thumb:
                data['thumb'] = thumb
            data['supports_streaming'] = supports_streaming
            if reply_markup:
                data['reply_markup'] = reply_markup
            if disable_notification:
                data['disable_notification'] = disable_notification
            if reply_to_message_id:
                data['reply_to_message_id'] = reply_to_message_id
            return await self._request('sendVideo', data)
        else:
            files = {'video': ('video.mp4', video, 'video/mp4')}
            if caption:
                data['caption'] = caption
            if parse_mode:
                data['parse_mode'] = parse_mode
            if duration:
                data['duration'] = str(duration)
            if width:
                data['width'] = str(width)
            if height:
                data['height'] = str(height)
            if thumb:
                files['thumb'] = ('thumb.jpg', thumb, 'image/jpeg')
            data['supports_streaming'] = str(supports_streaming)
            if reply_markup:
                data['reply_markup'] = json.dumps(reply_markup)
            if disable_notification:
                data['disable_notification'] = str(disable_notification)
            if reply_to_message_id:
                data['reply_to_message_id'] = str(reply_to_message_id)
            return await self._request('sendVideo', data, files)

    async def send_voice(
            self,
            chat_id: Union[int, str],
            voice: Union[str, bytes],
            caption: Optional[str] = None,
            parse_mode: Optional[str] = None,
            duration: Optional[int] = None,
            reply_markup: Optional[Dict] = None,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None
    ) -> Dict:
        """Wysyła wiadomość głosową"""
        data = {'chat_id': chat_id}

        if isinstance(voice, str):
            data['voice'] = voice
            if caption:
                data['caption'] = caption
            if parse_mode:
                data['parse_mode'] = parse_mode
            if duration:
                data['duration'] = duration
            if reply_markup:
                data['reply_markup'] = reply_markup
            if disable_notification:
                data['disable_notification'] = disable_notification
            if reply_to_message_id:
                data['reply_to_message_id'] = reply_to_message_id
            return await self._request('sendVoice', data)
        else:
            files = {'voice': ('voice.ogg', voice, 'audio/ogg')}
            if caption:
                data['caption'] = caption
            if parse_mode:
                data['parse_mode'] = parse_mode
            if duration:
                data['duration'] = str(duration)
            if reply_markup:
                data['reply_markup'] = json.dumps(reply_markup)
            if disable_notification:
                data['disable_notification'] = str(disable_notification)
            if reply_to_message_id:
                data['reply_to_message_id'] = str(reply_to_message_id)
            return await self._request('sendVoice', data, files)

    async def send_video_note(
            self,
            chat_id: Union[int, str],
            video_note: Union[str, bytes],
            duration: Optional[int] = None,
            length: Optional[int] = None,
            thumb: Optional[Union[str, bytes]] = None,
            reply_markup: Optional[Dict] = None,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None
    ) -> Dict:
        """Wysyła okrągłe wideo"""
        data = {'chat_id': chat_id}

        if isinstance(video_note, str):
            data['video_note'] = video_note
            if duration:
                data['duration'] = duration
            if length:
                data['length'] = length
            if thumb:
                data['thumb'] = thumb
            if reply_markup:
                data['reply_markup'] = reply_markup
            if disable_notification:
                data['disable_notification'] = disable_notification
            if reply_to_message_id:
                data['reply_to_message_id'] = reply_to_message_id
            return await self._request('sendVideoNote', data)
        else:
            files = {'video_note': ('video_note.mp4', video_note, 'video/mp4')}
            if duration:
                data['duration'] = str(duration)
            if length:
                data['length'] = str(length)
            if thumb:
                files['thumb'] = ('thumb.jpg', thumb, 'image/jpeg')
            if reply_markup:
                data['reply_markup'] = json.dumps(reply_markup)
            if disable_notification:
                data['disable_notification'] = str(disable_notification)
            if reply_to_message_id:
                data['reply_to_message_id'] = str(reply_to_message_id)
            return await self._request('sendVideoNote', data, files)

    async def send_media_group(
            self,
            chat_id: Union[int, str],
            media: List[Dict],
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None
    ) -> List[Dict]:
        """Wysyła grupę mediów"""
        data = {
            'chat_id': chat_id,
            'media': json.dumps(media),
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        return await self._request('sendMediaGroup', data)

    async def send_location(
            self,
            chat_id: Union[int, str],
            latitude: float,
            longitude: float,
            horizontal_accuracy: Optional[float] = None,
            live_period: Optional[int] = None,
            heading: Optional[int] = None,
            proximity_alert_radius: Optional[int] = None,
            reply_markup: Optional[Dict] = None,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None
    ) -> Dict:
        """Wysyła lokalizację"""
        data = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude,
            'horizontal_accuracy': horizontal_accuracy,
            'live_period': live_period,
            'heading': heading,
            'proximity_alert_radius': proximity_alert_radius,
            'reply_markup': reply_markup,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        return await self._request('sendLocation', data)

    async def send_venue(
            self,
            chat_id: Union[int, str],
            latitude: float,
            longitude: float,
            title: str,
            address: str,
            foursquare_id: Optional[str] = None,
            foursquare_type: Optional[str] = None,
            google_place_id: Optional[str] = None,
            google_place_type: Optional[str] = None,
            reply_markup: Optional[Dict] = None,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None
    ) -> Dict:
        """Wysyła miejsce"""
        data = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude,
            'title': title,
            'address': address,
            'foursquare_id': foursquare_id,
            'foursquare_type': foursquare_type,
            'google_place_id': google_place_id,
            'google_place_type': google_place_type,
            'reply_markup': reply_markup,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        return await self._request('sendVenue', data)

    async def send_contact(
            self,
            chat_id: Union[int, str],
            phone_number: str,
            first_name: str,
            last_name: Optional[str] = None,
            vcard: Optional[str] = None,
            reply_markup: Optional[Dict] = None,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None
    ) -> Dict:
        """Wysyła kontakt"""
        data = {
            'chat_id': chat_id,
            'phone_number': phone_number,
            'first_name': first_name,
            'last_name': last_name,
            'vcard': vcard,
            'reply_markup': reply_markup,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        return await self._request('sendContact', data)

    async def send_poll(
            self,
            chat_id: Union[int, str],
            question: str,
            options: List[str],
            is_anonymous: bool = True,
            type: str = 'regular',
            allows_multiple_answers: bool = False,
            correct_option_id: Optional[int] = None,
            explanation: Optional[str] = None,
            explanation_parse_mode: Optional[str] = None,
            open_period: Optional[int] = None,
            close_date: Optional[int] = None,
            is_closed: bool = False,
            reply_markup: Optional[Dict] = None,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None
    ) -> Dict:
        """Wysyła ankietę"""
        data = {
            'chat_id': chat_id,
            'question': question,
            'options': json.dumps(options),
            'is_anonymous': is_anonymous,
            'type': type,
            'allows_multiple_answers': allows_multiple_answers,
            'correct_option_id': correct_option_id,
            'explanation': explanation,
            'explanation_parse_mode': explanation_parse_mode,
            'open_period': open_period,
            'close_date': close_date,
            'is_closed': is_closed,
            'reply_markup': reply_markup,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        return await self._request('sendPoll', data)

    async def send_dice(
            self,
            chat_id: Union[int, str],
            emoji: str = '🎲',
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Dict] = None
    ) -> Dict:
        """Wysyła kość do gry"""
        data = {
            'chat_id': chat_id,
            'emoji': emoji,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': reply_markup
        }
        return await self._request('sendDice', data)

    async def send_chat_action(
            self,
            chat_id: Union[int, str],
            action: str
    ) -> bool:
        """Wysyła akcję czatu (pisanie, wysyłanie pliku itp.)"""
        data = {'chat_id': chat_id, 'action': action}
        return await self._request('sendChatAction', data)

    async def get_file(self, file_id: str) -> Dict:
        """Pobiera informacje o pliku"""
        return await self._request('getFile', {'file_id': file_id})

    async def download_file(self, file_path: str) -> bytes:
        """Pobiera plik z serwera Telegram"""
        session = await self._get_session()
        url = f"{self.file_url}/{file_path}"

        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.read()
                raise TelegramAPIError(f"Failed to download file: {resp.status}")
        except aiohttp.ClientError as e:
            raise NetworkError(f"Download failed: {e}")

    async def answer_callback_query(
            self,
            callback_query_id: str,
            text: Optional[str] = None,
            show_alert: bool = False,
            url: Optional[str] = None,
            cache_time: int = 0
    ) -> Dict:
        """Odpowiada na callback query"""
        data = {
            'callback_query_id': callback_query_id,
            'text': text,
            'show_alert': show_alert,
            'url': url,
            'cache_time': cache_time
        }
        return await self._request('answerCallbackQuery', data)

    async def edit_message_text(
            self,
            text: str,
            chat_id: Optional[Union[int, str]] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None,
            parse_mode: Optional[str] = None,
            reply_markup: Optional[Dict] = None,
            disable_web_page_preview: bool = False
    ) -> Dict:
        """Edytuje wiadomość tekstową"""
        data = {
            'text': text,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup,
            'disable_web_page_preview': disable_web_page_preview
        }

        if chat_id and message_id:
            data['chat_id'] = chat_id
            data['message_id'] = message_id
        elif inline_message_id:
            data['inline_message_id'] = inline_message_id
        else:
            raise ValueError("Either (chat_id and message_id) or inline_message_id must be provided")

        return await self._request('editMessageText', data)

    async def edit_message_caption(
            self,
            chat_id: Optional[Union[int, str]] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None,
            caption: Optional[str] = None,
            parse_mode: Optional[str] = None,
            reply_markup: Optional[Dict] = None
    ) -> Dict:
        """Edytuje podpis wiadomości"""
        data = {
            'caption': caption,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup
        }

        if chat_id and message_id:
            data['chat_id'] = chat_id
            data['message_id'] = message_id
        elif inline_message_id:
            data['inline_message_id'] = inline_message_id
        else:
            raise ValueError("Either (chat_id and message_id) or inline_message_id must be provided")

        return await self._request('editMessageCaption', data)

    async def edit_message_media(
            self,
            media: Dict,
            chat_id: Optional[Union[int, str]] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None,
            reply_markup: Optional[Dict] = None
    ) -> Dict:
        """Edytuje media wiadomości"""
        data = {
            'media': json.dumps(media),
            'reply_markup': reply_markup
        }

        if chat_id and message_id:
            data['chat_id'] = chat_id
            data['message_id'] = message_id
        elif inline_message_id:
            data['inline_message_id'] = inline_message_id
        else:
            raise ValueError("Either (chat_id and message_id) or inline_message_id must be provided")

        return await self._request('editMessageMedia', data)

    async def edit_message_reply_markup(
            self,
            chat_id: Optional[Union[int, str]] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None,
            reply_markup: Optional[Dict] = None
    ) -> Dict:
        """Edytuje przyciski wiadomości"""
        data = {'reply_markup': reply_markup}

        if chat_id and message_id:
            data['chat_id'] = chat_id
            data['message_id'] = message_id
        elif inline_message_id:
            data['inline_message_id'] = inline_message_id
        else:
            raise ValueError("Either (chat_id and message_id) or inline_message_id must be provided")

        return await self._request('editMessageReplyMarkup', data)

    async def stop_poll(
            self,
            chat_id: Union[int, str],
            message_id: int,
            reply_markup: Optional[Dict] = None
    ) -> Dict:
        """Zatrzymuje ankietę"""
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'reply_markup': reply_markup
        }
        return await self._request('stopPoll', data)

    async def delete_message(
            self,
            chat_id: Union[int, str],
            message_id: int
    ) -> bool:
        """Usuwa wiadomość"""
        data = {'chat_id': chat_id, 'message_id': message_id}
        return await self._request('deleteMessage', data)

    async def set_webhook(
            self,
            url: str,
            certificate: Optional[bytes] = None,
            max_connections: int = 40,
            allowed_updates: Optional[List[str]] = None,
            ip_address: Optional[str] = None,
            drop_pending_updates: bool = False,
            secret_token: Optional[str] = None
    ) -> Dict:
        """Ustawia webhook"""
        data = {
            'url': url,
            'max_connections': max_connections,
            'allowed_updates': allowed_updates,
            'ip_address': ip_address,
            'drop_pending_updates': drop_pending_updates,
            'secret_token': secret_token
        }

        if certificate:
            files = {'certificate': ('cert.pem', certificate, 'application/x-pem-file')}
            return await self._request('setWebhook', data, files)

        return await self._request('setWebhook', data)

    async def delete_webhook(self, drop_pending_updates: bool = False) -> Dict:
        """Usuwa webhook"""
        return await self._request('deleteWebhook', {'drop_pending_updates': drop_pending_updates})

    async def get_webhook_info(self) -> Dict:
        """Pobiera informacje o webhooku"""
        return await self._request('getWebhookInfo', {})

    async def get_me(self) -> Dict:
        """Pobiera informacje o bocie"""
        return await self._request('getMe', {})

    async def log_out(self) -> bool:
        """Wylogowuje bota z API"""
        return await self._request('logOut', {})

    async def close_bot(self) -> bool:
        """Zamyka połączenie bota"""
        return await self._request('close', {})

    async def get_chat(self, chat_id: Union[int, str]) -> Dict:
        """Pobiera informacje o czacie"""
        return await self._request('getChat', {'chat_id': chat_id})

    async def get_chat_administrators(self, chat_id: Union[int, str]) -> List[Dict]:
        """Pobiera listę administratorów czatu"""
        return await self._request('getChatAdministrators', {'chat_id': chat_id})

    async def get_chat_member_count(self, chat_id: Union[int, str]) -> int:
        """Pobiera liczbę członków czatu"""
        return await self._request('getChatMemberCount', {'chat_id': chat_id})

    async def get_chat_member(
            self,
            chat_id: Union[int, str],
            user_id: int
    ) -> Dict:
        """Pobiera informacje o członku czatu"""
        return await self._request('getChatMember', {'chat_id': chat_id, 'user_id': user_id})

    async def ban_chat_member(
            self,
            chat_id: Union[int, str],
            user_id: int,
            until_date: Optional[int] = None,
            revoke_messages: bool = False
    ) -> bool:
        """Banuje użytkownika w czacie"""
        data = {
            'chat_id': chat_id,
            'user_id': user_id,
            'until_date': until_date,
            'revoke_messages': revoke_messages
        }
        return await self._request('banChatMember', data)

    async def unban_chat_member(
            self,
            chat_id: Union[int, str],
            user_id: int,
            only_if_banned: bool = False
    ) -> bool:
        """Odbanowuje użytkownika w czacie"""
        data = {'chat_id': chat_id, 'user_id': user_id, 'only_if_banned': only_if_banned}
        return await self._request('unbanChatMember', data)

    async def restrict_chat_member(
            self,
            chat_id: Union[int, str],
            user_id: int,
            permissions: Dict,
            until_date: Optional[int] = None
    ) -> bool:
        """Ogranicza uprawnienia użytkownika w czacie"""
        data = {
            'chat_id': chat_id,
            'user_id': user_id,
            'permissions': json.dumps(permissions),
            'until_date': until_date
        }
        return await self._request('restrictChatMember', data)

    async def promote_chat_member(
            self,
            chat_id: Union[int, str],
            user_id: int,
            can_change_info: Optional[bool] = None,
            can_post_messages: Optional[bool] = None,
            can_edit_messages: Optional[bool] = None,
            can_delete_messages: Optional[bool] = None,
            can_invite_users: Optional[bool] = None,
            can_restrict_members: Optional[bool] = None,
            can_pin_messages: Optional[bool] = None,
            can_promote_members: Optional[bool] = None,
            can_manage_chat: Optional[bool] = None,
            can_manage_video_chats: Optional[bool] = None,
            is_anonymous: Optional[bool] = None
    ) -> bool:
        """Awansuje użytkownika na administratora"""
        data = {
            'chat_id': chat_id,
            'user_id': user_id,
            'can_change_info': can_change_info,
            'can_post_messages': can_post_messages,
            'can_edit_messages': can_edit_messages,
            'can_delete_messages': can_delete_messages,
            'can_invite_users': can_invite_users,
            'can_restrict_members': can_restrict_members,
            'can_pin_messages': can_pin_messages,
            'can_promote_members': can_promote_members,
            'can_manage_chat': can_manage_chat,
            'can_manage_video_chats': can_manage_video_chats,
            'is_anonymous': is_anonymous
        }
        return await self._request('promoteChatMember', data)

    async def set_chat_administrator_custom_title(
            self,
            chat_id: Union[int, str],
            user_id: int,
            custom_title: str
    ) -> bool:
        """Ustawia niestandardowy tytuł administratora"""
        data = {'chat_id': chat_id, 'user_id': user_id, 'custom_title': custom_title}
        return await self._request('setChatAdministratorCustomTitle', data)

    async def ban_chat_sender_chat(
            self,
            chat_id: Union[int, str],
            sender_chat_id: int
    ) -> bool:
        """Banuje kanał w supergrupie"""
        data = {'chat_id': chat_id, 'sender_chat_id': sender_chat_id}
        return await self._request('banChatSenderChat', data)

    async def unban_chat_sender_chat(
            self,
            chat_id: Union[int, str],
            sender_chat_id: int
    ) -> bool:
        """Odbanowuje kanał w supergrupie"""
        data = {'chat_id': chat_id, 'sender_chat_id': sender_chat_id}
        return await self._request('unbanChatSenderChat', data)

    async def set_chat_permissions(
            self,
            chat_id: Union[int, str],
            permissions: Dict
    ) -> bool:
        """Ustawia domyślne uprawnienia czatu"""
        data = {'chat_id': chat_id, 'permissions': json.dumps(permissions)}
        return await self._request('setChatPermissions', data)

    async def export_chat_invite_link(self, chat_id: Union[int, str]) -> str:
        """Eksportuje link zaproszenia do czatu"""
        return await self._request('exportChatInviteLink', {'chat_id': chat_id})

    async def create_chat_invite_link(
            self,
            chat_id: Union[int, str],
            name: Optional[str] = None,
            expire_date: Optional[int] = None,
            member_limit: Optional[int] = None,
            creates_join_request: bool = False
    ) -> Dict:
        """Tworzy link zaproszenia do czatu"""
        data = {
            'chat_id': chat_id,
            'name': name,
            'expire_date': expire_date,
            'member_limit': member_limit,
            'creates_join_request': creates_join_request
        }
        return await self._request('createChatInviteLink', data)

    async def edit_chat_invite_link(
            self,
            chat_id: Union[int, str],
            invite_link: str,
            name: Optional[str] = None,
            expire_date: Optional[int] = None,
            member_limit: Optional[int] = None,
            creates_join_request: bool = False
    ) -> Dict:
        """Edytuje link zaproszenia do czatu"""
        data = {
            'chat_id': chat_id,
            'invite_link': invite_link,
            'name': name,
            'expire_date': expire_date,
            'member_limit': member_limit,
            'creates_join_request': creates_join_request
        }
        return await self._request('editChatInviteLink', data)

    async def revoke_chat_invite_link(
            self,
            chat_id: Union[int, str],
            invite_link: str
    ) -> Dict:
        """Unieważnia link zaproszenia do czatu"""
        data = {'chat_id': chat_id, 'invite_link': invite_link}
        return await self._request('revokeChatInviteLink', data)

    async def approve_chat_join_request(
            self,
            chat_id: Union[int, str],
            user_id: int
    ) -> bool:
        """Zatwierdza prośbę o dołączenie do czatu"""
        data = {'chat_id': chat_id, 'user_id': user_id}
        return await self._request('approveChatJoinRequest', data)

    async def decline_chat_join_request(
            self,
            chat_id: Union[int, str],
            user_id: int
    ) -> bool:
        """Odrzuca prośbę o dołączenie do czatu"""
        data = {'chat_id': chat_id, 'user_id': user_id}
        return await self._request('declineChatJoinRequest', data)

    async def set_chat_photo(
            self,
            chat_id: Union[int, str],
            photo: bytes
    ) -> bool:
        """Ustawia zdjęcie czatu"""
        files = {'photo': ('photo.jpg', photo, 'image/jpeg')}
        return await self._request('setChatPhoto', {'chat_id': chat_id}, files)

    async def delete_chat_photo(self, chat_id: Union[int, str]) -> bool:
        """Usuwa zdjęcie czatu"""
        return await self._request('deleteChatPhoto', {'chat_id': chat_id})

    async def set_chat_title(self, chat_id: Union[int, str], title: str) -> bool:
        """Ustawia tytuł czatu"""
        return await self._request('setChatTitle', {'chat_id': chat_id, 'title': title})

    async def set_chat_description(
            self,
            chat_id: Union[int, str],
            description: Optional[str] = None
    ) -> bool:
        """Ustawia opis czatu"""
        return await self._request('setChatDescription', {'chat_id': chat_id, 'description': description})

    async def pin_chat_message(
            self,
            chat_id: Union[int, str],
            message_id: int,
            disable_notification: bool = False
    ) -> bool:
        """Przypina wiadomość w czacie"""
        data = {'chat_id': chat_id, 'message_id': message_id, 'disable_notification': disable_notification}
        return await self._request('pinChatMessage', data)

    async def unpin_chat_message(
            self,
            chat_id: Union[int, str],
            message_id: Optional[int] = None
    ) -> bool:
        """Odpina wiadomość w czacie"""
        data = {'chat_id': chat_id, 'message_id': message_id}
        return await self._request('unpinChatMessage', data)

    async def unpin_all_chat_messages(self, chat_id: Union[int, str]) -> bool:
        """Odpina wszystkie wiadomości w czacie"""
        return await self._request('unpinAllChatMessages', {'chat_id': chat_id})

    async def leave_chat(self, chat_id: Union[int, str]) -> bool:
        """Opuszcza czat"""
        return await self._request('leaveChat', {'chat_id': chat_id})

    async def get_user_profile_photos(
            self,
            user_id: int,
            offset: Optional[int] = None,
            limit: int = 100
    ) -> Dict:
        """Pobiera zdjęcia profilowe użytkownika"""
        data = {'user_id': user_id, 'offset': offset, 'limit': limit}
        return await self._request('getUserProfilePhotos', data)

    async def set_my_commands(
            self,
            commands: List[Dict],
            scope: Optional[Dict] = None,
            language_code: Optional[str] = None
    ) -> bool:
        """Ustawia komendy bota"""
        data = {
            'commands': json.dumps(commands),
            'scope': json.dumps(scope) if scope else None,
            'language_code': language_code
        }
        return await self._request('setMyCommands', data)

    async def delete_my_commands(
            self,
            scope: Optional[Dict] = None,
            language_code: Optional[str] = None
    ) -> bool:
        """Usuwa komendy bota"""
        data = {
            'scope': json.dumps(scope) if scope else None,
            'language_code': language_code
        }
        return await self._request('deleteMyCommands', data)

    async def get_my_commands(
            self,
            scope: Optional[Dict] = None,
            language_code: Optional[str] = None
    ) -> List[Dict]:
        """Pobiera komendy bota"""
        data = {
            'scope': json.dumps(scope) if scope else None,
            'language_code': language_code
        }
        return await self._request('getMyCommands', data)

    async def set_my_description(
            self,
            description: Optional[str] = None,
            language_code: Optional[str] = None
    ) -> bool:
        """Ustawia opis bota"""
        data = {'description': description, 'language_code': language_code}
        return await self._request('setMyDescription', data)

    async def get_my_description(self, language_code: Optional[str] = None) -> Dict:
        """Pobiera opis bota"""
        return await self._request('getMyDescription', {'language_code': language_code})

    async def set_my_short_description(
            self,
            short_description: Optional[str] = None,
            language_code: Optional[str] = None
    ) -> bool:
        """Ustawia krótki opis bota"""
        data = {'short_description': short_description, 'language_code': language_code}
        return await self._request('setMyShortDescription', data)

    async def get_my_short_description(self, language_code: Optional[str] = None) -> Dict:
        """Pobiera krótki opis bota"""
        return await self._request('getMyShortDescription', {'language_code': language_code})

    async def set_chat_menu_button(
            self,
            chat_id: Optional[int] = None,
            menu_button: Optional[Dict] = None
    ) -> bool:
        """Ustawia przycisk menu"""
        data = {'chat_id': chat_id, 'menu_button': json.dumps(menu_button) if menu_button else None}
        return await self._request('setChatMenuButton', data)

    async def get_chat_menu_button(self, chat_id: Optional[int] = None) -> Dict:
        """Pobiera przycisk menu"""
        return await self._request('getChatMenuButton', {'chat_id': chat_id})

    async def set_my_default_administrator_rights(
            self,
            rights: Optional[Dict] = None,
            for_channels: bool = False
    ) -> bool:
        """Ustawia domyślne uprawnienia administratora"""
        data = {'rights': json.dumps(rights) if rights else None, 'for_channels': for_channels}
        return await self._request('setMyDefaultAdministratorRights', data)

    async def get_my_default_administrator_rights(self, for_channels: bool = False) -> Dict:
        """Pobiera domyślne uprawnienia administratora"""
        return await self._request('getMyDefaultAdministratorRights', {'for_channels': for_channels})

    async def get_sticker_set(self, name: str) -> Dict:
        """Pobiera zestaw naklejek"""
        return await self._request('getStickerSet', {'name': name})

    async def get_custom_emoji_stickers(self, custom_emoji_ids: List[str]) -> List[Dict]:
        """Pobiera niestandardowe emoji jako naklejki"""
        return await self._request('getCustomEmojiStickers', {'custom_emoji_ids': json.dumps(custom_emoji_ids)})

    async def upload_sticker_file(
            self,
            user_id: int,
            sticker: bytes,
            sticker_format: str
    ) -> Dict:
        """Przesyła plik naklejki"""
        files = {'sticker': ('sticker.png', sticker, 'image/png')}
        data = {'user_id': user_id, 'sticker_format': sticker_format}
        return await self._request('uploadStickerFile', data, files)

    async def create_new_sticker_set(
            self,
            user_id: int,
            name: str,
            title: str,
            stickers: List[Dict],
            sticker_format: str,
            sticker_type: Optional[str] = None,
            needs_repainting: Optional[bool] = None
    ) -> bool:
        """Tworzy nowy zestaw naklejek"""
        data = {
            'user_id': user_id,
            'name': name,
            'title': title,
            'stickers': json.dumps(stickers),
            'sticker_format': sticker_format,
            'sticker_type': sticker_type,
            'needs_repainting': needs_repainting
        }
        return await self._request('createNewStickerSet', data)

    async def add_sticker_to_set(
            self,
            user_id: int,
            name: str,
            sticker: Dict
    ) -> bool:
        """Dodaje naklejkę do zestawu"""
        data = {'user_id': user_id, 'name': name, 'sticker': json.dumps(sticker)}
        return await self._request('addStickerToSet', data)

    async def set_sticker_position_in_set(
            self,
            sticker: str,
            position: int
    ) -> bool:
        """Ustawia pozycję naklejki w zestawie"""
        data = {'sticker': sticker, 'position': position}
        return await self._request('setStickerPositionInSet', data)

    async def delete_sticker_from_set(self, sticker: str) -> bool:
        """Usuwa naklejkę z zestawu"""
        return await self._request('deleteStickerFromSet', {'sticker': sticker})

    async def set_sticker_emoji_list(
            self,
            sticker: str,
            emoji_list: List[str]
    ) -> bool:
        """Ustawia listę emoji dla naklejki"""
        data = {'sticker': sticker, 'emoji_list': json.dumps(emoji_list)}
        return await self._request('setStickerEmojiList', data)

    async def set_sticker_keywords(
            self,
            sticker: str,
            keywords: Optional[List[str]] = None
    ) -> bool:
        """Ustawia słowa kluczowe dla naklejki"""
        data = {'sticker': sticker, 'keywords': json.dumps(keywords) if keywords else None}
        return await self._request('setStickerKeywords', data)

    async def set_sticker_mask_position(
            self,
            sticker: str,
            mask_position: Optional[Dict] = None
    ) -> bool:
        """Ustawia pozycję maski dla naklejki"""
        data = {'sticker': sticker, 'mask_position': json.dumps(mask_position) if mask_position else None}
        return await self._request('setStickerMaskPosition', data)

    async def set_sticker_set_title(self, name: str, title: str) -> bool:
        """Ustawia tytuł zestawu naklejek"""
        return await self._request('setStickerSetTitle', {'name': name, 'title': title})

    async def set_sticker_set_thumbnail(
            self,
            name: str,
            user_id: int,
            thumbnail: Optional[Union[str, bytes]] = None
    ) -> bool:
        """Ustawia miniaturę zestawu naklejek"""
        if isinstance(thumbnail, bytes):
            files = {'thumbnail': ('thumb.png', thumbnail, 'image/png')}
            data = {'name': name, 'user_id': user_id}
            return await self._request('setStickerSetThumbnail', data, files)
        else:
            data = {'name': name, 'user_id': user_id, 'thumbnail': thumbnail}
            return await self._request('setStickerSetThumbnail', data)

    async def set_custom_emoji_sticker_set_thumbnail(
            self,
            name: str,
            custom_emoji_id: Optional[str] = None
    ) -> bool:
        """Ustawia miniaturę zestawu niestandardowych emoji"""
        data = {'name': name, 'custom_emoji_id': custom_emoji_id}
        return await self._request('setCustomEmojiStickerSetThumbnail', data)

    async def delete_sticker_set(self, name: str) -> bool:
        """Usuwa zestaw naklejek"""
        return await self._request('deleteStickerSet', {'name': name})

    async def answer_inline_query(
            self,
            inline_query_id: str,
            results: List[Dict],
            cache_time: int = 300,
            is_personal: bool = False,
            next_offset: Optional[str] = None,
            button: Optional[Dict] = None
    ) -> bool:
        """Odpowiada na zapytanie inline"""
        data = {
            'inline_query_id': inline_query_id,
            'results': json.dumps(results),
            'cache_time': cache_time,
            'is_personal': is_personal,
            'next_offset': next_offset,
            'button': json.dumps(button) if button else None
        }
        return await self._request('answerInlineQuery', data)

    async def answer_web_app_query(
            self,
            web_app_query_id: str,
            result: Dict
    ) -> Dict:
        """Odpowiada na zapytanie z Web App"""
        data = {'web_app_query_id': web_app_query_id, 'result': json.dumps(result)}
        return await self._request('answerWebAppQuery', data)

    async def send_invoice(
            self,
            chat_id: int,
            title: str,
            description: str,
            payload: str,
            provider_token: str,
            currency: str,
            prices: List[Dict],
            max_tip_amount: Optional[int] = None,
            suggested_tip_amounts: Optional[List[int]] = None,
            start_parameter: Optional[str] = None,
            provider_data: Optional[str] = None,
            photo_url: Optional[str] = None,
            photo_size: Optional[int] = None,
            photo_width: Optional[int] = None,
            photo_height: Optional[int] = None,
            need_name: bool = False,
            need_phone_number: bool = False,
            need_email: bool = False,
            need_shipping_address: bool = False,
            send_phone_number_to_provider: bool = False,
            send_email_to_provider: bool = False,
            is_flexible: bool = False,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Dict] = None
    ) -> Dict:
        """Wysyła fakturę"""
        data = {
            'chat_id': chat_id,
            'title': title,
            'description': description,
            'payload': payload,
            'provider_token': provider_token,
            'currency': currency,
            'prices': json.dumps(prices),
            'max_tip_amount': max_tip_amount,
            'suggested_tip_amounts': json.dumps(suggested_tip_amounts) if suggested_tip_amounts else None,
            'start_parameter': start_parameter,
            'provider_data': provider_data,
            'photo_url': photo_url,
            'photo_size': photo_size,
            'photo_width': photo_width,
            'photo_height': photo_height,
            'need_name': need_name,
            'need_phone_number': need_phone_number,
            'need_email': need_email,
            'need_shipping_address': need_shipping_address,
            'send_phone_number_to_provider': send_phone_number_to_provider,
            'send_email_to_provider': send_email_to_provider,
            'is_flexible': is_flexible,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': reply_markup
        }
        return await self._request('sendInvoice', data)

    async def answer_shipping_query(
            self,
            shipping_query_id: str,
            ok: bool,
            shipping_options: Optional[List[Dict]] = None,
            error_message: Optional[str] = None
    ) -> bool:
        """Odpowiada na zapytanie o dostawę"""
        data = {
            'shipping_query_id': shipping_query_id,
            'ok': ok,
            'shipping_options': json.dumps(shipping_options) if shipping_options else None,
            'error_message': error_message
        }
        return await self._request('answerShippingQuery', data)

    async def answer_pre_checkout_query(
            self,
            pre_checkout_query_id: str,
            ok: bool,
            error_message: Optional[str] = None
    ) -> bool:
        """Odpowiada na zapytanie przedpłatne"""
        data = {
            'pre_checkout_query_id': pre_checkout_query_id,
            'ok': ok,
            'error_message': error_message
        }
        return await self._request('answerPreCheckoutQuery', data)

    async def send_game(
            self,
            chat_id: int,
            game_short_name: str,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Dict] = None
    ) -> Dict:
        """Wysyła grę"""
        data = {
            'chat_id': chat_id,
            'game_short_name': game_short_name,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': reply_markup
        }
        return await self._request('sendGame', data)

    async def set_game_score(
            self,
            user_id: int,
            score: int,
            force: bool = False,
            disable_edit_message: bool = False,
            chat_id: Optional[int] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None
    ) -> Dict:
        """Ustawia wynik w grze"""
        data = {
            'user_id': user_id,
            'score': score,
            'force': force,
            'disable_edit_message': disable_edit_message
        }
        if chat_id and message_id:
            data['chat_id'] = chat_id
            data['message_id'] = message_id
        elif inline_message_id:
            data['inline_message_id'] = inline_message_id
        else:
            raise ValueError("Either (chat_id and message_id) or inline_message_id must be provided")
        return await self._request('setGameScore', data)

    async def get_game_high_scores(
            self,
            user_id: int,
            chat_id: Optional[int] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None
    ) -> List[Dict]:
        """Pobiera najwyższe wyniki w grze"""
        data = {'user_id': user_id}
        if chat_id and message_id:
            data['chat_id'] = chat_id
            data['message_id'] = message_id
        elif inline_message_id:
            data['inline_message_id'] = inline_message_id
        else:
            raise ValueError("Either (chat_id and message_id) or inline_message_id must be provided")
        return await self._request('getGameHighScores', data)