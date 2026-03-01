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
            filename = getattr(audio, 'name', 'audio.mp3') if hasattr(audio, 'name') else 'audio.mp3'
            files = {'audio': (filename, audio, 'audio/mpeg')}
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
                if isinstance(thumb, bytes):
                    files['thumb'] = ('thumb.jpg', thumb, 'image/jpeg')
                else:
                    data['thumb'] = thumb
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
            filename = getattr(video, 'name', 'video.mp4') if hasattr(video, 'name') else 'video.mp4'
            files = {'video': (filename, video, 'video/mp4')}
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
                if isinstance(thumb, bytes):
                    files['thumb'] = ('thumb.jpg', thumb, 'image/jpeg')
                else:
                    data['thumb'] = thumb
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
            filename = getattr(voice, 'name', 'voice.ogg') if hasattr(voice, 'name') else 'voice.ogg'
            files = {'voice': (filename, voice, 'audio/ogg')}
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
            filename = getattr(video_note, 'name', 'video_note.mp4') if hasattr(video_note, 'name') else 'video_note.mp4'
            files = {'video_note': (filename, video_note, 'video/mp4')}
            if duration:
                data['duration'] = str(duration)
            if length:
                data['length'] = str(length)
            if thumb:
                if isinstance(thumb, bytes):
                    files['thumb'] = ('thumb.jpg', thumb, 'image/jpeg')
                else:
                    data['thumb'] = thumb
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