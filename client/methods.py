from typing import Optional, Dict, Any, Union, List
import json
import aiohttp

from ..exceptions import TelegramAPIError, NetworkError


def _convert_markup(markup: Any) -> Any:
    """Convert markup objects to dict if they have to_dict() method"""
    if hasattr(markup, 'to_dict'):
        return markup.to_dict()
    return markup


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
            'reply_markup': _convert_markup(reply_markup),
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
                data['reply_markup'] = _convert_markup(reply_markup)
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
                data['reply_markup'] = json.dumps(_convert_markup(reply_markup))
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
                data['reply_markup'] = _convert_markup(reply_markup)
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
                data['reply_markup'] = json.dumps(_convert_markup(reply_markup))
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
                data['reply_markup'] = _convert_markup(reply_markup)
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
                data['reply_markup'] = json.dumps(_convert_markup(reply_markup))
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
                data['reply_markup'] = _convert_markup(reply_markup)
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
                data['reply_markup'] = json.dumps(_convert_markup(reply_markup))
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
                data['reply_markup'] = _convert_markup(reply_markup)
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
                data['reply_markup'] = json.dumps(_convert_markup(reply_markup))
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
                data['reply_markup'] = _convert_markup(reply_markup)
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
                data['reply_markup'] = json.dumps(_convert_markup(reply_markup))
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
            'reply_markup': _convert_markup(reply_markup),
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
            'reply_markup': _convert_markup(reply_markup),
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
            'reply_markup': _convert_markup(reply_markup),
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
            poll_type: str = 'regular',
            allows_multiple_answers: bool = False,
            # API 9.6 - replaced correct_option_id with correct_option_ids
            correct_option_id: Optional[int] = None,  # Deprecated, use correct_option_ids
            correct_option_ids: Optional[List[int]] = None,  # API 9.6
            explanation: Optional[str] = None,
            explanation_parse_mode: Optional[str] = None,
            open_period: Optional[int] = None,
            close_date: Optional[int] = None,
            is_closed: bool = False,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Dict] = None,
            # API 9.6 new parameters
            allows_revoting: bool = False,
            description: Optional[str] = None,
            description_parse_mode: Optional[str] = None,
            shuffle_options: bool = False,
            allow_adding_options: bool = False,
            hide_results_until_closes: bool = False
    ) -> Dict:
        """
        Sends a poll.

        Args:
            chat_id: Target chat ID
            question: Poll question
            options: List of answer options
            is_anonymous: True if users' votes are anonymous
            poll_type: 'quiz' or 'regular'
            allows_multiple_answers: True for multiple answers (quiz only)
            correct_option_id: Deprecated, use correct_option_ids
            correct_option_ids: List of correct option IDs (API 9.6, quiz mode)
            explanation: Text shown when user selects answer (quiz)
            explanation_parse_mode: Parse mode for explanation
            open_period: Time in seconds until poll closes
            close_date: Timestamp when poll closes
            is_closed: True if poll is closed
            disable_notification: Sends silently
            reply_to_message_id: Message to reply to
            reply_markup: Reply markup
            allows_revoting: Allow changing vote (API 9.6)
            description: Poll description (API 9.6)
            description_parse_mode: Parse mode for description (API 9.6)
            shuffle_options: Randomize answer order (API 9.6)
            allow_adding_options: Allow adding new options (API 9.6)
            hide_results_until_closes: Hide results until poll closes (API 9.6)

        Returns:
            Poll object as dict

        Documentation:
            https://core.telegram.org/bots/api#sendpoll
        """
        data = {
            'chat_id': chat_id,
            'question': question,
            'options': json.dumps(options),  # IMPORTANT: must be JSON-serialized
            'is_anonymous': is_anonymous,
            'type': poll_type,
            'allows_multiple_answers': allows_multiple_answers,
            'allows_revoting': allows_revoting,
            'shuffle_options': shuffle_options,
            'allow_adding_options': allow_adding_options,
            'hide_results_until_closes': hide_results_until_closes,
            'is_closed': is_closed,
            'disable_notification': disable_notification
        }

        # API 9.6: prefer correct_option_ids over correct_option_id
        if correct_option_ids is not None:
            data['correct_option_ids'] = correct_option_ids
        elif correct_option_id is not None:
            data['correct_option_id'] = correct_option_id

        # API 9.6: description
        if description:
            data['description'] = description
            if description_parse_mode:
                data['description_parse_mode'] = description_parse_mode

        if explanation:
            data['explanation'] = explanation
            if explanation_parse_mode:
                data['explanation_parse_mode'] = explanation_parse_mode
        if open_period:
            data['open_period'] = open_period
        if close_date:
            data['close_date'] = close_date
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            data['reply_markup'] = _convert_markup(reply_markup)

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
            'reply_markup': _convert_markup(reply_markup)
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
            'reply_markup': _convert_markup(reply_markup),
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
            'reply_markup': _convert_markup(reply_markup)
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
            'reply_markup': _convert_markup(reply_markup)
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
        data = {'reply_markup': _convert_markup(reply_markup)}

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
            'reply_markup': _convert_markup(reply_markup)
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

    # === NOWE METODY API 9.5 ===

    async def send_message_draft(
            self,
            chat_id: Union[int, str],
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None,
            text: Optional[str] = None,
            parse_mode: Optional[str] = None,
            entities: Optional[List[Dict]] = None,
            streaming_mode: Optional[str] = None
    ) -> bool:
        """
        Wysyła szkic wiadomości do czatu - pozwala na strumieniowe przesyłanie
        częściowej treści wiadomości podczas jej generowania (API 9.5).
        
        Tworzy natywny wskaźnik "pisania" i dynamicznie aktualizuje wyświetlany tekst.
        Dostępne dla wszystkich botów od API 9.5.
        
        Args:
            chat_id: Identifier czatu lub nazwa użytkownika
            message_id: ID wiadomości do edycji (opcjonalne)
            inline_message_id: ID wiadomości inline (opcjonalne)
            text: Tekst szkicu wiadomości
            parse_mode: Tryb parsowania (Markdown, MarkdownV2, HTML)
            entities: Lista encji formatowania tekstu
            streaming_mode: Tryb strumieniowania: 'partial', 'block', lub 'progress' (domyślnie 'partial')
        
        Returns:
            True po sukcesie
        
        Documentation:
            https://core.telegram.org/bots/api#sendmessagedraft
        """
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'inline_message_id': inline_message_id,
            'text': text,
            'parse_mode': parse_mode,
            'entities': entities,
            'streaming_mode': streaming_mode
        }
        # Usuń None values
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('sendMessageDraft', data)

    async def set_chat_member_tag(
            self,
            chat_id: Union[int, str],
            user_id: int,
            tag: Optional[str] = None
    ) -> bool:
        """
        Ustawia tag dla członka grupy lub supergrupy (API 9.5).
        
        Bot musi być administratorem z uprawnieniem can_manage_tags.
        
        Args:
            chat_id: Identifier czatu lub nazwa użytkownika supergrupy
            user_id: ID użytkownika
            tag: Nowy tag dla członka (0-16 znaków, emoji niedozwolone)
        
        Returns:
            True po sukcesie
        
        Documentation:
            https://core.telegram.org/bots/api#setchatmembertag
        """
        data = {
            'chat_id': chat_id,
            'user_id': user_id,
            'tag': tag
        }
        # Usuń None values
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('setChatMemberTag', data)

    async def promote_chat_member(
            self,
            chat_id: Union[int, str],
            user_id: int,
            is_anonymous: Optional[bool] = None,
            can_manage_chat: Optional[bool] = None,
            can_change_info: Optional[bool] = None,
            can_post_messages: Optional[bool] = None,
            can_edit_messages: Optional[bool] = None,
            can_delete_messages: Optional[bool] = None,
            can_invite_users: Optional[bool] = None,
            can_restrict_members: Optional[bool] = None,
            can_pin_messages: Optional[bool] = None,
            can_manage_video_chats: Optional[bool] = None,
            can_manage_topics: Optional[bool] = None,
            can_promote_members: Optional[bool] = None,
            can_manage_tags: Optional[bool] = None
    ) -> bool:
        """
        Promuje użytkownika na administratora (API 9.5 z can_manage_tags).
        
        Args:
            chat_id: Identifier czatu lub nazwa użytkownika
            user_id: ID użytkownika do promowania
            is_anonymous: Czy admin jest anonimowy
            can_manage_chat: Czy może zarządzać czatem
            can_change_info: Czy może zmieniać informacje o czacie
            can_post_messages: Czy może publikować w kanale
            can_edit_messages: Czy może edytować wiadomości
            can_delete_messages: Czy może usuwać wiadomości
            can_invite_users: Czy może zapraszać użytkowników
            can_restrict_members: Czy może ograniczać użytkowników
            can_pin_messages: Czy może przypinać wiadomości
            can_manage_video_chats: Czy może zarządzać czatami wideo
            can_manage_topics: Czy może zarządzać tematami
            can_promote_members: Czy może promować członków
            can_manage_tags: Czy może zarządzać tagami członków (API 9.5)
        
        Returns:
            True po sukcesie
        
        Documentation:
            https://core.telegram.org/bots/api#promotechatmember
        """
        data = {
            'chat_id': chat_id,
            'user_id': user_id,
            'is_anonymous': is_anonymous,
            'can_manage_chat': can_manage_chat,
            'can_change_info': can_change_info,
            'can_post_messages': can_post_messages,
            'can_edit_messages': can_edit_messages,
            'can_delete_messages': can_delete_messages,
            'can_invite_users': can_invite_users,
            'can_restrict_members': can_restrict_members,
            'can_pin_messages': can_pin_messages,
            'can_manage_video_chats': can_manage_video_chats,
            'can_manage_topics': can_manage_topics,
            'can_promote_members': can_promote_members,
            'can_manage_tags': can_manage_tags
        }
        # Usuń None values
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('promoteChatMember', data)

    # ==================== Bot Commands API ====================

    async def set_my_commands(
            self,
            commands: List[Dict[str, str]],
            scope: Optional[Dict[str, Any]] = None,
            language_code: Optional[str] = None
    ) -> bool:
        """
        Sets bot commands for the specified scope and language.
        
        Args:
            commands: List of dicts with 'command' and 'description' keys
            scope: BotCommandScope dict (optional)
            language_code: IETF language code (optional)
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#setmycommands
        """
        data = {'commands': commands}
        if scope:
            data['scope'] = scope
        if language_code:
            data['language_code'] = language_code
        return await self._request('setMyCommands', data)

    async def get_my_commands(
            self,
            scope: Optional[Dict[str, Any]] = None,
            language_code: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Gets bot commands for the specified scope and language.
        
        Args:
            scope: BotCommandScope dict (optional)
            language_code: IETF language code (optional)
            
        Returns:
            List of BotCommand objects
            
        Documentation:
            https://core.telegram.org/bots/api#getmycommands
        """
        data = {}
        if scope:
            data['scope'] = scope
        if language_code:
            data['language_code'] = language_code
        return await self._request('getMyCommands', data)

    async def delete_my_commands(
            self,
            scope: Optional[Dict[str, Any]] = None,
            language_code: Optional[str] = None
    ) -> bool:
        """
        Deletes bot commands for the specified scope and language.
        
        Args:
            scope: BotCommandScope dict (optional)
            language_code: IETF language code (optional)
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#deletemycommands
        """
        data = {}
        if scope:
            data['scope'] = scope
        if language_code:
            data['language_code'] = language_code
        return await self._request('deleteMyCommands', data)

    async def set_my_name(
            self,
            name: Optional[str] = None,
            language_code: Optional[str] = None
    ) -> bool:
        """
        Sets bot name for the specified language.
        
        Args:
            name: Bot name (2-64 chars, optional)
            language_code: IETF language code (optional)
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#setmyname
        """
        data = {}
        if name is not None:
            data['name'] = name
        if language_code:
            data['language_code'] = language_code
        return await self._request('setMyName', data)

    async def get_my_name(self, language_code: Optional[str] = None) -> Dict[str, str]:
        """
        Gets bot name for the specified language.
        
        Args:
            language_code: IETF language code (optional)
            
        Returns:
            Dict with 'name' key
            
        Documentation:
            https://core.telegram.org/bots/api#getmyname
        """
        data = {}
        if language_code:
            data['language_code'] = language_code
        return await self._request('getMyName', data)

    async def set_my_description(
            self,
            description: Optional[str] = None,
            language_code: Optional[str] = None
    ) -> bool:
        """
        Sets bot description for the specified language.
        
        Args:
            description: Bot description (0-512 chars, optional)
            language_code: IETF language code (optional)
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#setmydescription
        """
        data = {}
        if description is not None:
            data['description'] = description
        if language_code:
            data['language_code'] = language_code
        return await self._request('setMyDescription', data)

    async def get_my_description(self, language_code: Optional[str] = None) -> Dict[str, str]:
        """
        Gets bot description for the specified language.
        
        Args:
            language_code: IETF language code (optional)
            
        Returns:
            Dict with 'description' key
            
        Documentation:
            https://core.telegram.org/bots/api#getmydescription
        """
        data = {}
        if language_code:
            data['language_code'] = language_code
        return await self._request('getMyDescription', data)

    async def set_my_short_description(
            self,
            short_description: Optional[str] = None,
            language_code: Optional[str] = None
    ) -> bool:
        """
        Sets bot short description for the specified language.
        
        Args:
            short_description: Short description (0-120 chars, optional)
            language_code: IETF language code (optional)
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#setmyshortdescription
        """
        data = {}
        if short_description is not None:
            data['short_description'] = short_description
        if language_code:
            data['language_code'] = language_code
        return await self._request('setMyShortDescription', data)

    async def get_my_short_description(self, language_code: Optional[str] = None) -> Dict[str, str]:
        """
        Gets bot short description for the specified language.
        
        Args:
            language_code: IETF language code (optional)
            
        Returns:
            Dict with 'short_description' key
            
        Documentation:
            https://core.telegram.org/bots/api#getmyshortdescription
        """
        data = {}
        if language_code:
            data['language_code'] = language_code
        return await self._request('getMyShortDescription', data)

    # ==================== Payments API ====================

    async def send_invoice(
            self,
            chat_id: Union[int, str],
            title: str,
            description: str,
            payload: str,
            currency: str,
            prices: List[Dict[str, Any]],
            provider_token: Optional[str] = None,
            max_tip_amount: Optional[int] = None,
            suggested_tip_amounts: Optional[List[int]] = None,
            start_parameter: Optional[str] = None,
            provider_data: Optional[Union[str, Dict]] = None,
            photo_url: Optional[str] = None,
            photo_size: Optional[int] = None,
            photo_width: Optional[int] = None,
            photo_height: Optional[int] = None,
            need_name: Optional[bool] = None,
            need_phone_number: Optional[bool] = None,
            need_email: Optional[bool] = None,
            need_shipping_address: Optional[bool] = None,
            send_phone_number_to_provider: Optional[bool] = None,
            send_email_to_provider: Optional[bool] = None,
            is_flexible: Optional[bool] = None,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Dict] = None
    ) -> Dict:
        """
        Sends an invoice.
        
        Args:
            chat_id: Target chat ID
            title: Product name
            description: Product description
            payload: Bot-defined payload (max 128 bytes)
            currency: ISO 4217 currency code
            prices: Price breakdown (list of {label, amount})
            provider_token: Payment provider token (optional for Telegram Stars)
            max_tip_amount: Max tip amount in smallest units
            suggested_tip_amounts: Array of suggested tip amounts
            start_parameter: Deep-linking parameter
            provider_data: Payment provider data (JSON)
            photo_url: Product photo URL
            photo_size: Photo size
            photo_width: Photo width
            photo_height: Photo height
            need_name: Require user name
            need_phone_number: Require phone
            need_email: Require email
            need_shipping_address: Require shipping
            send_phone_number_to_provider: Send phone to provider
            send_email_to_provider: Send email to provider
            is_flexible: Flexible price
            disable_notification: Silent send
            reply_to_message_id: Reply to message ID
            reply_markup: Inline keyboard
            
        Returns:
            Message object
            
        Documentation:
            https://core.telegram.org/bots/api#sendinvoice
        """
        data = {
            'chat_id': chat_id,
            'title': title,
            'description': description,
            'payload': payload,
            'currency': currency,
            'prices': prices,
            'provider_token': provider_token,
            'max_tip_amount': max_tip_amount,
            'suggested_tip_amounts': suggested_tip_amounts,
            'start_parameter': start_parameter,
            'provider_data': json.dumps(provider_data) if isinstance(provider_data, dict) else provider_data,
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
            'reply_markup': _convert_markup(reply_markup)
        }
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('sendInvoice', data)

    async def create_invoice_link(
            self,
            title: str,
            description: str,
            payload: str,
            currency: str,
            prices: List[Dict[str, Any]],
            provider_token: Optional[str] = None,
            max_tip_amount: Optional[int] = None,
            suggested_tip_amounts: Optional[List[int]] = None,
            provider_data: Optional[Union[str, Dict]] = None,
            photo_url: Optional[str] = None,
            photo_size: Optional[int] = None,
            photo_width: Optional[int] = None,
            photo_height: Optional[int] = None,
            need_name: Optional[bool] = None,
            need_phone_number: Optional[bool] = None,
            need_email: Optional[bool] = None,
            need_shipping_address: Optional[bool] = None,
            send_phone_number_to_provider: Optional[bool] = None,
            send_email_to_provider: Optional[bool] = None,
            is_flexible: Optional[bool] = None
    ) -> str:
        """
        Creates an invoice link.
        
        Returns:
            Invoice link URL
            
        Documentation:
            https://core.telegram.org/bots/api#createinvoicelink
        """
        data = {
            'title': title,
            'description': description,
            'payload': payload,
            'currency': currency,
            'prices': prices,
            'provider_token': provider_token,
            'max_tip_amount': max_tip_amount,
            'suggested_tip_amounts': suggested_tip_amounts,
            'provider_data': json.dumps(provider_data) if isinstance(provider_data, dict) else provider_data,
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
            'is_flexible': is_flexible
        }
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('createInvoiceLink', data)

    async def answer_shipping_query(
            self,
            shipping_query_id: str,
            ok: bool,
            shipping_options: Optional[List[Dict[str, Any]]] = None,
            error_message: Optional[str] = None
    ) -> bool:
        """
        Answers a shipping query.
        
        Args:
            shipping_query_id: Query ID
            ok: True if delivery is possible
            shipping_options: Available shipping options (required if ok=True)
            error_message: Error message (required if ok=False)
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#answershippingquery
        """
        data = {
            'shipping_query_id': shipping_query_id,
            'ok': ok,
            'shipping_options': shipping_options,
            'error_message': error_message
        }
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('answerShippingQuery', data)

    async def answer_pre_checkout_query(
            self,
            pre_checkout_query_id: str,
            ok: bool,
            error_message: Optional[str] = None
    ) -> bool:
        """
        Answers a pre-checkout query.
        
        Args:
            pre_checkout_query_id: Query ID
            ok: True if checkout is possible
            error_message: Error message (required if ok=False)
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#answerprecheckoutquery
        """
        data = {
            'pre_checkout_query_id': pre_checkout_query_id,
            'ok': ok,
            'error_message': error_message
        }
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('answerPreCheckoutQuery', data)

    async def get_star_transactions(
            self,
            offset: Optional[int] = None,
            limit: Optional[int] = None
    ) -> Dict:
        """
        Gets Telegram Star transactions.

        Returns:
            StarTransactions object

        Documentation:
            https://core.telegram.org/bots/api#getstartransactions
        """
        data = {}
        if offset:
            data['offset'] = offset
        if limit:
            data['limit'] = limit
        return await self._request('getStarTransactions', data)

    async def get_my_star_balance(self) -> int:
        """
        Returns the current Telegram Star balance of the bot.

        Returns:
            Current balance in Telegram Stars

        Documentation:
            https://core.telegram.org/bots/api#getmystarbalance
        """
        result = await self._request('getMyStarBalance')
        return result.get('balance', 0)

    async def refund_star_payment(
            self,
            user_id: int,
            telegram_payment_charge_id: str
    ) -> bool:
        """
        Refunds a successful Telegram Star payment.
        
        Args:
            user_id: User ID who made the payment
            telegram_payment_charge_id: Telegram payment charge ID
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#refundstarpayment
        """
        data = {
            'user_id': user_id,
            'telegram_payment_charge_id': telegram_payment_charge_id
        }
        return await self._request('refundStarPayment', data)

    # ==================== Games API ====================

    async def send_game(
            self,
            chat_id: Union[int, str],
            game_short_name: str,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Dict] = None
    ) -> Dict:
        """
        Sends a game.
        
        Args:
            chat_id: Target chat ID
            game_short_name: Game short name (set via @BotFather)
            disable_notification: Silent send
            reply_to_message_id: Reply to message ID
            reply_markup: Inline keyboard with game button
            
        Returns:
            Message object
            
        Documentation:
            https://core.telegram.org/bots/api#sendgame
        """
        data = {
            'chat_id': chat_id,
            'game_short_name': game_short_name,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': _convert_markup(reply_markup)
        }
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('sendGame', data)

    async def set_game_score(
            self,
            user_id: int,
            score: int,
            force: bool = False,
            disable_edit_message: bool = False,
            chat_id: Optional[Union[int, str]] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None
    ) -> Union[Dict, bool]:
        """
        Sets game score for a user.
        
        Args:
            user_id: User ID
            score: New score
            force: True if score can be decreased
            disable_edit_message: Don't edit message
            chat_id: Chat ID
            message_id: Message ID
            inline_message_id: Inline message ID
            
        Returns:
            Message on success, or True if inline
            
        Documentation:
            https://core.telegram.org/bots/api#setgamescore
        """
        data = {
            'user_id': user_id,
            'score': score,
            'force': force,
            'disable_edit_message': disable_edit_message,
            'chat_id': chat_id,
            'message_id': message_id,
            'inline_message_id': inline_message_id
        }
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('setGameScore', data)

    async def get_game_high_scores(
            self,
            user_id: int,
            chat_id: Optional[Union[int, str]] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None
    ) -> List[Dict]:
        """
        Gets game high scores.
        
        Args:
            user_id: Target user ID
            chat_id: Chat ID
            message_id: Message ID
            inline_message_id: Inline message ID
            
        Returns:
            List of GameHighScore objects
            
        Documentation:
            https://core.telegram.org/bots/api#getgamehighscores
        """
        data = {
            'user_id': user_id,
            'chat_id': chat_id,
            'message_id': message_id,
            'inline_message_id': inline_message_id
        }
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('getGameHighScores', data)

    # ==================== Forum/Topics API ====================

    async def create_forum_topic(
            self,
            chat_id: Union[int, str],
            name: str,
            icon_color: Optional[int] = None,
            icon_custom_emoji_id: Optional[str] = None
    ) -> Dict:
        """
        Creates a forum topic.
        
        Args:
            chat_id: Target chat ID
            name: Topic name (1-128 chars)
            icon_color: RGB color (0x6FB9F0, 0xFFD67E, 0xE8A269, etc.)
            icon_custom_emoji_id: Custom emoji ID
            
        Returns:
            ForumTopic object
            
        Documentation:
            https://core.telegram.org/bots/api#createforumtopic
        """
        data = {
            'chat_id': chat_id,
            'name': name,
            'icon_color': icon_color,
            'icon_custom_emoji_id': icon_custom_emoji_id
        }
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('createForumTopic', data)

    async def edit_forum_topic(
            self,
            chat_id: Union[int, str],
            message_thread_id: int,
            name: Optional[str] = None,
            icon_custom_emoji_id: Optional[str] = None
    ) -> bool:
        """
        Edits a forum topic.
        
        Args:
            chat_id: Target chat ID
            message_thread_id: Thread ID
            name: New topic name
            icon_custom_emoji_id: New custom emoji ID
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#editforumtopic
        """
        data = {
            'chat_id': chat_id,
            'message_thread_id': message_thread_id,
            'name': name,
            'icon_custom_emoji_id': icon_custom_emoji_id
        }
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('editForumTopic', data)

    async def close_forum_topic(
            self,
            chat_id: Union[int, str],
            message_thread_id: int
    ) -> bool:
        """
        Closes a forum topic.
        
        Args:
            chat_id: Target chat ID
            message_thread_id: Thread ID
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#closeforumtopic
        """
        data = {
            'chat_id': chat_id,
            'message_thread_id': message_thread_id
        }
        return await self._request('closeForumTopic', data)

    async def reopen_forum_topic(
            self,
            chat_id: Union[int, str],
            message_thread_id: int
    ) -> bool:
        """
        Reopens a forum topic.
        
        Args:
            chat_id: Target chat ID
            message_thread_id: Thread ID
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#reopenforumtopic
        """
        data = {
            'chat_id': chat_id,
            'message_thread_id': message_thread_id
        }
        return await self._request('reopenForumTopic', data)

    async def delete_forum_topic(
            self,
            chat_id: Union[int, str],
            message_thread_id: int
    ) -> bool:
        """
        Deletes a forum topic.
        
        Args:
            chat_id: Target chat ID
            message_thread_id: Thread ID
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#deleteforumtopic
        """
        data = {
            'chat_id': chat_id,
            'message_thread_id': message_thread_id
        }
        return await self._request('deleteForumTopic', data)

    async def unpin_all_forum_topic_messages(
            self,
            chat_id: Union[int, str],
            message_thread_id: int
    ) -> bool:
        """
        Unpins all messages in a forum topic.
        
        Args:
            chat_id: Target chat ID
            message_thread_id: Thread ID
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#unpinallforumtopicmessages
        """
        data = {
            'chat_id': chat_id,
            'message_thread_id': message_thread_id
        }
        return await self._request('unpinAllForumTopicMessages', data)

    async def edit_general_forum_topic(
            self,
            chat_id: Union[int, str],
            name: str
    ) -> bool:
        """
        Edits the General forum topic.
        
        Args:
            chat_id: Target chat ID
            name: New name (1-128 chars)
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#editgeneralforumtopic
        """
        data = {
            'chat_id': chat_id,
            'name': name
        }
        return await self._request('editGeneralForumTopic', data)

    async def close_general_forum_topic(
            self,
            chat_id: Union[int, str]
    ) -> bool:
        """Closes the General forum topic."""
        return await self._request('closeGeneralForumTopic', {'chat_id': chat_id})

    async def reopen_general_forum_topic(
            self,
            chat_id: Union[int, str]
    ) -> bool:
        """Reopens the General forum topic."""
        return await self._request('reopenGeneralForumTopic', {'chat_id': chat_id})

    async def hide_general_forum_topic(
            self,
            chat_id: Union[int, str]
    ) -> bool:
        """Hides the General forum topic."""
        return await self._request('hideGeneralForumTopic', {'chat_id': chat_id})

    async def unhide_general_forum_topic(
            self,
            chat_id: Union[int, str]
    ) -> bool:
        """Unhides the General forum topic."""
        return await self._request('unhideGeneralForumTopic', {'chat_id': chat_id})

    async def unpin_all_general_forum_topic_messages(
            self,
            chat_id: Union[int, str]
    ) -> bool:
        """Unpins all messages in the General forum topic."""
        return await self._request('unpinAllGeneralForumTopicMessages', {'chat_id': chat_id})

    # ==================== Bot Menu API ====================

    async def set_chat_menu_button(
            self,
            chat_id: Optional[Union[int, str]] = None,
            menu_button: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Sets the menu button for a chat or default.
        
        Args:
            chat_id: Target chat ID (optional for default)
            menu_button: MenuButton dict (commands, web_app, or default)
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#setchatmenubutton
        """
        data = {}
        if chat_id:
            data['chat_id'] = chat_id
        if menu_button:
            data['menu_button'] = menu_button
        return await self._request('setChatMenuButton', data)

    async def get_chat_menu_button(
            self,
            chat_id: Optional[Union[int, str]] = None
    ) -> Dict:
        """
        Gets the menu button for a chat or default.
        
        Args:
            chat_id: Target chat ID (optional for default)
            
        Returns:
            MenuButton object
            
        Documentation:
            https://core.telegram.org/bots/api#getchatmenubutton
        """
        data = {}
        if chat_id:
            data['chat_id'] = chat_id
        return await self._request('getChatMenuButton', data)

    # ==================== Sticker API ====================

    async def send_sticker(
            self,
            chat_id: Union[int, str],
            sticker: Union[str, Any],
            emoji: Optional[str] = None,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Dict] = None
    ) -> Dict:
        """
        Sends a sticker.
        
        Args:
            chat_id: Target chat ID
            sticker: File ID, file path, or file object
            emoji: Emoji associated with sticker
            disable_notification: Silent send
            reply_to_message_id: Reply to message ID
            reply_markup: Reply markup
            
        Returns:
            Message object
            
        Documentation:
            https://core.telegram.org/bots/api#sendsticker
        """
        data = {
            'chat_id': chat_id,
            'sticker': sticker,
            'emoji': emoji,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': _convert_markup(reply_markup)
        }
        data = {k: v for k, v in data.items() if v is not None}
        
        # Handle file upload
        files = None
        if isinstance(sticker, str) and not sticker.startswith(('http', 'file://')) and len(sticker) < 200:
            # Likely a file_id, no upload needed
            pass
        elif isinstance(sticker, str) and sticker.startswith('file://'):
            files = {'sticker': open(sticker[7:], 'rb')}
            data['sticker'] = 'sticker_file'
        
        result = await self._request('sendSticker', data, files)
        
        if files:
            files['sticker'].close()
        
        return result

    async def get_sticker_set(
            self,
            name: str
    ) -> Dict:
        """
        Gets a sticker set.
        
        Args:
            name: Sticker set name
            
        Returns:
            StickerSet object
            
        Documentation:
            https://core.telegram.org/bots/api#getstickerset
        """
        return await self._request('getStickerSet', {'name': name})

    async def upload_sticker_file(
            self,
            user_id: int,
            sticker: Union[str, Any],
            sticker_format: str = "static"
    ) -> Dict:
        """
        Uploads a sticker file for later use.
        
        Args:
            user_id: User ID
            sticker: File path or object
            sticker_format: "static", "animated", or "video"
            
        Returns:
            File object
            
        Documentation:
            https://core.telegram.org/bots/api#uploadstickerfile
        """
        data = {
            'user_id': user_id,
            'sticker_format': sticker_format
        }
        files = None
        
        if isinstance(sticker, str) and sticker.startswith('file://'):
            files = {'sticker': open(sticker[7:], 'rb')}
            data['sticker'] = 'sticker_file'
        
        result = await self._request('uploadStickerFile', data, files)
        
        if files:
            files['sticker'].close()
        
        return result

    async def create_new_sticker_set(
            self,
            user_id: int,
            name: str,
            title: str,
            stickers: List[Dict[str, Any]],
            sticker_type: str = "regular",
            needs_repainting: bool = False
    ) -> bool:
        """
        Creates a new sticker set.
        
        Args:
            user_id: User ID
            name: Sticker set name
            title: Sticker set title
            stickers: List of sticker objects
            sticker_type: "regular", "mask", or "custom_emoji"
            needs_repainting: True if masks need repainting
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#createnewstickerset
        """
        data = {
            'user_id': user_id,
            'name': name,
            'title': title,
            'stickers': stickers,
            'sticker_type': sticker_type,
            'needs_repainting': needs_repainting
        }
        return await self._request('createNewStickerSet', data)

    async def add_sticker_to_set(
            self,
            user_id: int,
            name: str,
            sticker: Dict[str, Any]
    ) -> bool:
        """
        Adds a sticker to a sticker set.
        
        Args:
            user_id: User ID
            name: Sticker set name
            sticker: Sticker object
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#addstickertoset
        """
        data = {
            'user_id': user_id,
            'name': name,
            'sticker': sticker
        }
        return await self._request('addStickerToSet', data)

    async def set_sticker_position_in_set(
            self,
            sticker: str,
            position: int
    ) -> bool:
        """
        Sets the position of a sticker in its set.
        
        Args:
            sticker: File ID of the sticker
            position: New position (0-based)
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#setstickerpositioninset
        """
        data = {
            'sticker': sticker,
            'position': position
        }
        return await self._request('setStickerPositionInSet', data)

    async def delete_sticker_from_set(
            self,
            sticker: str
    ) -> bool:
        """
        Deletes a sticker from its set.
        
        Args:
            sticker: File ID of the sticker
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#deletestickerfromset
        """
        return await self._request('deleteStickerFromSet', {'sticker': sticker})

    async def set_sticker_set_thumb(
            self,
            name: str,
            user_id: int,
            thumb: Optional[str] = None
    ) -> bool:
        """
        Sets the thumbnail of a sticker set.
        
        Args:
            name: Sticker set name
            user_id: User ID
            thumb: Thumbnail file path or ID
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#setstickersetthumb
        """
        data = {
            'name': name,
            'user_id': user_id,
            'thumb': thumb
        }
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('setStickerSetThumb', data)

    async def set_custom_emoji_sticker_set_thumbnail(
            self,
            name: str,
            custom_emoji_id: Optional[str] = None
    ) -> bool:
        """
        Sets the custom emoji sticker set thumbnail.
        
        Documentation:
            https://core.telegram.org/bots/api#setcustomemojistickersetthumbnail
        """
        data = {'name': name, 'custom_emoji_id': custom_emoji_id}
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('setCustomEmojiStickerSetThumbnail', data)

    async def delete_sticker_set(self, name: str) -> bool:
        """
        Deletes a sticker set.
        
        Documentation:
            https://core.telegram.org/bots/api#deletestickerset
        """
        return await self._request('deleteStickerSet', {'name': name})

    # ==================== Reaction API ====================

    async def set_message_reaction(
            self,
            chat_id: Union[int, str],
            message_id: int,
            reaction: Optional[List[Dict[str, str]]] = None,
            is_big: bool = False
    ) -> bool:
        """
        Sets reaction on a message.
        
        Args:
            chat_id: Target chat ID
            message_id: Message ID
            reaction: List of ReactionType dicts (e.g., {"type": "emoji", "emoji": "👍"})
            is_big: Show big animation
            
        Returns:
            True on success
            
        Documentation:
            https://core.telegram.org/bots/api#setmessagereaction
        """
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'reaction': reaction,
            'is_big': is_big
        }
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('setMessageReaction', data)

    # ==================== Business API ====================

    async def get_business_connection(self, business_connection_id: str) -> Dict:
        """
        Gets business connection info.
        
        Args:
            business_connection_id: Business connection ID
            
        Returns:
            BusinessConnection object
            
        Documentation:
            https://core.telegram.org/bots/api#getbusinessconnection
        """
        return await self._request('getBusinessConnection', {'business_connection_id': business_connection_id})

    async def edit_user_star_subscription(
            self,
            user_id: int,
            telegram_payment_charge_id: str,
            is_canceled: bool
    ) -> bool:
        """
        Edits a user's Telegram Star subscription.
        
        Documentation:
            https://core.telegram.org/bots/api#edituserstarsubscription
        """
        data = {
            'user_id': user_id,
            'telegram_payment_charge_id': telegram_payment_charge_id,
            'is_canceled': is_canceled
        }
        return await self._request('editUserStarSubscription', data)

    async def replace_sticker_in_set(
            self,
            user_id: int,
            name: str,
            old_sticker: str,
            sticker: Dict[str, Any]
    ) -> bool:
        """
        Replaces a sticker in a sticker set.
        
        Documentation:
            https://core.telegram.org/bots/api#replacestickerinset
        """
        data = {
            'user_id': user_id,
            'name': name,
            'old_sticker': old_sticker,
            'sticker': sticker
        }
        return await self._request('replaceStickerInSet', data)

    async def set_user_emoji_status(
            self,
            user_id: int,
            custom_emoji_id: Optional[str] = None,
            until_date: Optional[int] = None
    ) -> bool:
        """
        Sets the emoji status for a user (admin only).
        
        Documentation:
            https://core.telegram.org/bots/api#setuseremojistatus
        """
        data = {
            'user_id': user_id,
            'custom_emoji_id': custom_emoji_id,
            'until_date': until_date
        }
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('setUserEmojiStatus', data)

    async def get_available_gifts(self) -> List[Dict]:
        """
        Gets available gifts.
        
        Documentation:
            https://core.telegram.org/bots/api#getavailablegifts
        """
        return await self._request('getAvailableGifts', {})

    async def send_gift(
            self,
            user_id: int,
            gift_id: str,
            text: Optional[str] = None,
            pay_for_upgrade: bool = False
    ) -> bool:
        """
        Sends a gift to a user.
        
        Documentation:
            https://core.telegram.org/bots/api#sendgift
        """
        data = {
            'user_id': user_id,
            'gift_id': gift_id,
            'text': text,
            'pay_for_upgrade': pay_for_upgrade
        }
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('sendGift', data)

    async def verify_user(
            self,
            user_id: int,
            custom_description: Optional[str] = None
    ) -> bool:
        """
        Verifies a user (shows checkmark).
        
        Documentation:
            https://core.telegram.org/bots/api#verifyuser
        """
        data = {
            'user_id': user_id,
            'custom_description': custom_description
        }
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('verifyUser', data)

    async def verify_chat(
            self,
            chat_id: Union[int, str],
            custom_description: Optional[str] = None
    ) -> bool:
        """
        Verifies a chat (shows checkmark).
        
        Documentation:
            https://core.telegram.org/bots/api#verifychat
        """
        data = {
            'chat_id': chat_id,
            'custom_description': custom_description
        }
        data = {k: v for k, v in data.items() if v is not None}
        return await self._request('verifyChat', data)

    async def remove_user_verification(
            self,
            user_id: int
    ) -> bool:
        """
        Removes verification from a user.
        
        Documentation:
            https://core.telegram.org/bots/api#removeuserverification
        """
        return await self._request('removeUserVerification', {'user_id': user_id})

    async def remove_chat_verification(
            self,
            chat_id: Union[int, str]
    ) -> bool:
        """
        Removes verification from a chat.

        Documentation:
            https://core.telegram.org/bots/api#removechatverification
        """
        return await self._request('removeChatVerification', {'chat_id': chat_id})

    # ==================== API 9.6: Managed Bots ====================

    async def get_managed_bot_token(
            self,
            managed_bot_id: str
    ) -> Dict[str, str]:
        """
        Gets the token of a managed bot.

        Args:
            managed_bot_id: Unique identifier of the managed bot

        Returns:
            Dict with 'token' field

        Documentation:
            https://core.telegram.org/bots/api#getmanagedbottoken
        """
        return await self._request('getManagedBotToken', {'managed_bot_id': managed_bot_id})

    async def replace_managed_bot_token(
            self,
            managed_bot_id: str,
            name: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Replaces the token of a managed bot.

        Args:
            managed_bot_id: Unique identifier of the managed bot
            name: New name for the managed bot (optional)

        Returns:
            Dict with new 'token' field

        Documentation:
            https://core.telegram.org/bots/api#replacemanagedbottoken
        """
        data = {'managed_bot_id': managed_bot_id}
        if name:
            data['name'] = name
        return await self._request('replaceManagedBotToken', data)

    async def get_managed_bots(
            self,
            offset: Optional[int] = None,
            limit: Optional[int] = 100
    ) -> List[Dict]:
        """
        Gets a list of bots managed by the current bot.

        Args:
            offset: Identifier of the first bot to be returned
            limit: Limits the number of bots to be retrieved (1-100)

        Returns:
            Array of User objects

        Documentation:
            https://core.telegram.org/bots/api#getmanagedbots
        """
        data = {}
        if offset:
            data['offset'] = offset
        if limit:
            data['limit'] = limit
        return await self._request('getManagedBots', data)

    async def save_prepared_keyboard_button(
            self,
            button: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Saves a prepared keyboard button for Mini Apps.

        Args:
            button: PreparedKeyboardButton object or dict

        Returns:
            Dict with button 'id'

        Documentation:
            https://core.telegram.org/bots/api#savepreparedkeyboardbutton
        """
        if hasattr(button, 'to_dict'):
            button = button.to_dict()
        return await self._request('savePreparedKeyboardButton', button)

    # ==================== MISSING Methods from Earlier APIs ====================

    async def copy_message(
            self,
            chat_id: Union[int, str],
            from_chat_id: Union[int, str],
            message_id: int,
            caption: Optional[str] = None,
            caption_parse_mode: Optional[str] = None,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Dict] = None,
            show_caption_above_media: Optional[bool] = None
    ) -> Dict:
        """
        Copies a message without forwarding.

        Args:
            chat_id: Target chat
            from_chat_id: Source chat
            message_id: Message ID to copy
            caption: New caption for the copy
            caption_parse_mode: Parse mode for caption
            disable_notification: Send silently
            reply_to_message_id: Reply to this message
            reply_markup: Reply markup
            show_caption_above_media: Show caption above media

        Returns:
            MessageId of the copied message

        Documentation:
            https://core.telegram.org/bots/api#copymessage
        """
        data = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_id': message_id,
            'disable_notification': disable_notification
        }
        if caption:
            data['caption'] = caption
            if caption_parse_mode:
                data['caption_parse_mode'] = caption_parse_mode
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            data['reply_markup'] = _convert_markup(reply_markup)
        if show_caption_above_media is not None:
            data['show_caption_above_media'] = show_caption_above_media
        return await self._request('copyMessage', data)

    # ==================== Invite Link Management ====================

    async def create_chat_invite_link(
            self,
            chat_id: Union[int, str],
            name: Optional[str] = None,
            expire_date: Optional[int] = None,
            member_limit: Optional[int] = None,
            creates_join_request: bool = False
    ) -> Dict:
        """
        Creates an invite link for a chat.

        Args:
            chat_id: Target chat
            name: Link name (optional)
            expire_date: Expiration timestamp
            member_limit: Max users who can join
            creates_join_request: True for join requests instead of direct join

        Returns:
            ChatInviteLink object

        Documentation:
            https://core.telegram.org/bots/api#createchatinvitelink
        """
        data = {
            'chat_id': chat_id,
            'creates_join_request': creates_join_request
        }
        if name:
            data['name'] = name
        if expire_date:
            data['expire_date'] = expire_date
        if member_limit:
            data['member_limit'] = member_limit
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
        """
        Edits a non-revoked invite link.

        Args:
            chat_id: Target chat
            invite_link: The link to edit
            name: New link name
            expire_date: New expiration timestamp
            member_limit: New member limit
            creates_join_request: True for join requests

        Returns:
            Updated ChatInviteLink

        Documentation:
            https://core.telegram.org/bots/api#editchatinvitelink
        """
        data = {
            'chat_id': chat_id,
            'invite_link': invite_link,
            'creates_join_request': creates_join_request
        }
        if name:
            data['name'] = name
        if expire_date:
            data['expire_date'] = expire_date
        if member_limit:
            data['member_limit'] = member_limit
        return await self._request('editChatInviteLink', data)

    async def revoke_chat_invite_link(
            self,
            chat_id: Union[int, str],
            invite_link: str
    ) -> Dict:
        """
        Revokes an invite link.

        Args:
            chat_id: Target chat
            invite_link: The link to revoke

        Returns:
            Revoked ChatInviteLink

        Documentation:
            https://core.telegram.org/bots/api#revokechatinvitelink
        """
        return await self._request('revokeChatInviteLink', {
            'chat_id': chat_id,
            'invite_link': invite_link
        })

    # ==================== Pin/Unpin Messages ====================

    async def pin_chat_message(
            self,
            chat_id: Union[int, str],
            message_id: int,
            disable_notification: bool = False
    ) -> bool:
        """
        Pins a message in a chat.

        Args:
            chat_id: Target chat
            message_id: Message to pin
            disable_notification: Don't send notification

        Returns:
            True on success

        Documentation:
            https://core.telegram.org/bots/api#pinchatmessage
        """
        return await self._request('pinChatMessage', {
            'chat_id': chat_id,
            'message_id': message_id,
            'disable_notification': disable_notification
        })

    async def unpin_chat_message(
            self,
            chat_id: Union[int, str],
            message_id: Optional[int] = None
    ) -> bool:
        """
        Unpins a message or all messages in a chat.

        Args:
            chat_id: Target chat
            message_id: Specific message to unpin (optional)

        Returns:
            True on success

        Documentation:
            https://core.telegram.org/bots/api#unpinchatmessage
        """
        data = {'chat_id': chat_id}
        if message_id:
            data['message_id'] = message_id
        return await self._request('unpinChatMessage', data)

    async def unpin_all_chat_messages(
            self,
            chat_id: Union[int, str]
    ) -> bool:
        """
        Unpins all messages in a chat.

        Args:
            chat_id: Target chat

        Returns:
            True on success

        Documentation:
            https://core.telegram.org/bots/api#unpinallchatmessages
        """
        return await self._request('unpinAllChatMessages', {'chat_id': chat_id})

    # ==================== Chat Join Requests ====================

    async def approve_chat_join_request(
            self,
            chat_id: Union[int, str],
            user_id: int
    ) -> bool:
        """
        Approves a chat join request.

        Args:
            chat_id: Target chat
            user_id: User ID to approve

        Returns:
            True on success

        Documentation:
            https://core.telegram.org/bots/api#approvechatjoinrequest
        """
        return await self._request('approveChatJoinRequest', {
            'chat_id': chat_id,
            'user_id': user_id
        })

    async def decline_chat_join_request(
            self,
            chat_id: Union[int, str],
            user_id: int
    ) -> bool:
        """
        Declines a chat join request.

        Args:
            chat_id: Target chat
            user_id: User ID to decline

        Returns:
            True on success

        Documentation:
            https://core.telegram.org/bots/api#declinechatjoinrequest
        """
        return await self._request('declineChatJoinRequest', {
            'chat_id': chat_id,
            'user_id': user_id
        })

    # ==================== Chat Permissions ====================

    async def set_chat_permissions(
            self,
            chat_id: Union[int, str],
            permissions: Union[Dict, Any],
            use_independent_chat_permissions: bool = False
    ) -> bool:
        """
        Sets default chat permissions for all members.

        Args:
            chat_id: Target chat
            permissions: ChatPermissions object or dict
            use_independent_chat_permissions: Allow independent permissions

        Returns:
            True on success

        Documentation:
            https://core.telegram.org/bots/api#setchatpermissions
        """
        if hasattr(permissions, 'to_dict'):
            permissions = permissions.to_dict()
        data = {
            'chat_id': chat_id,
            'permissions': permissions,
            'use_independent_chat_permissions': use_independent_chat_permissions
        }
        return await self._request('setChatPermissions', data)

    # ==================== Ban/Unban Sender Chat ====================

    async def ban_chat_sender_chat(
            self,
            chat_id: Union[int, str],
            sender_chat_id: int
    ) -> bool:
        """
        Bans a channel/chat in a group or supergroup.

        Args:
            chat_id: Target chat
            sender_chat_id: Channel/chat ID to ban

        Returns:
            True on success

        Documentation:
            https://core.telegram.org/bots/api#banchatsenderchat
        """
        return await self._request('banChatSenderChat', {
            'chat_id': chat_id,
            'sender_chat_id': sender_chat_id
        })

    async def unban_chat_sender_chat(
            self,
            chat_id: Union[int, str],
            sender_chat_id: int
    ) -> bool:
        """
        Unbans a channel/chat in a group or supergroup.

        Args:
            chat_id: Target chat
            sender_chat_id: Channel/chat ID to unban

        Returns:
            True on success

        Documentation:
            https://core.telegram.org/bots/api#unbanchatsenderchat
        """
        return await self._request('unbanChatSenderChat', {
            'chat_id': chat_id,
            'sender_chat_id': sender_chat_id
        })

    # ==================== Administrator Rights ====================

    async def set_my_default_administrator_rights(
            self,
            rights: Optional[Union[Dict, Any]] = None,
            for_channels: bool = False
    ) -> bool:
        """
        Sets the default administrator rights for the bot.

        Args:
            rights: ChatAdministratorRights object or dict
            for_channels: True for channels, False for groups/supergroups

        Returns:
            True on success

        Documentation:
            https://core.telegram.org/bots/api#setmydefaultadministratorrights
        """
        data = {'for_channels': for_channels}
        if rights:
            if hasattr(rights, 'to_dict'):
                rights = rights.to_dict()
            data['rights'] = rights
        return await self._request('setMyDefaultAdministratorRights', data)

    async def get_my_default_administrator_rights(
            self,
            for_channels: bool = False
    ) -> Dict:
        """
        Gets the default administrator rights for the bot.

        Args:
            for_channels: True for channels, False for groups/supergroups

        Returns:
            ChatAdministratorRights object

        Documentation:
            https://core.telegram.org/bots/api#getmydefaultadministratorrights
        """
        return await self._request('getMyDefaultAdministratorRights', {
            'for_channels': for_channels
        })

    # ==================== Paid Media ====================

    async def send_paid_media(
            self,
            chat_id: Union[int, str],
            star_count: int,
            media: List[Dict[str, Any]],
            caption: Optional[str] = None,
            caption_parse_mode: Optional[str] = None,
            show_caption_above_media: bool = False,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Dict] = None
    ) -> Dict:
        """
        Sends paid media.

        Args:
            chat_id: Target chat
            star_count: Number of Telegram Stars required
            media: List of InputPaidMedia objects
            caption: Media caption
            caption_parse_mode: Parse mode for caption
            show_caption_above_media: Show caption above media
            disable_notification: Send silently
            reply_to_message_id: Reply to this message
            reply_markup: Reply markup

        Returns:
            Message object

        Documentation:
            https://core.telegram.org/bots/api#sendpaidmedia
        """
        data = {
            'chat_id': chat_id,
            'star_count': star_count,
            'media': media,
            'show_caption_above_media': show_caption_above_media,
            'disable_notification': disable_notification
        }
        if caption:
            data['caption'] = caption
            if caption_parse_mode:
                data['caption_parse_mode'] = caption_parse_mode
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            data['reply_markup'] = _convert_markup(reply_markup)
        return await self._request('sendPaidMedia', data)

    # ==================== Forum Topics ====================

    async def get_forum_topic_icon_stickers(self) -> List[Dict]:
        """
        Gets custom emoji stickers for forum topics.

        Returns:
            List of Sticker objects

        Documentation:
            https://core.telegram.org/bots/api#getforumtopiciconstickers
        """
        return await self._request('getForumTopicIconStickers')

    # ==================== Passport ====================

    async def set_passport_data_errors(
            self,
            user_id: int,
            errors: List[Dict[str, Any]]
    ) -> bool:
        """
        Informs the user about errors with passport data.

        Args:
            user_id: User ID
            errors: List of PassportElementError objects

        Returns:
            True on success

        Documentation:
            https://core.telegram.org/bots/api#setpassportdataerrors
        """
        return await self._request('setPassportDataErrors', {
            'user_id': user_id,
            'errors': errors
        })

    # ==================== Sticker Sets ====================

    async def set_sticker_set_title(
            self,
            name: str,
            title: str
    ) -> bool:
        """
        Sets the title of a sticker set.

        Args:
            name: Sticker set name
            title: New title

        Returns:
            True on success

        Documentation:
            https://core.telegram.org/bots/api#setstickersettitle
        """
        return await self._request('setStickerSetTitle', {
            'name': name,
            'title': title
        })

    async def set_sticker_set_emoji_sticker_format(
            self,
            name: str,
            emoji_sticker_format: str
    ) -> bool:
        """
        Sets the emoji sticker format of a sticker set.

        Args:
            name: Sticker set name
            emoji_sticker_format: Format (e.g., 'static', 'animated', 'video')

        Returns:
            True on success

        Documentation:
            https://core.telegram.org/bots/api#setstickerformat
        """
        return await self._request('setStickerSetEmojiStickerFormat', {
            'name': name,
            'emoji_sticker_format': emoji_sticker_format
        })
