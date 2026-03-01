from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime


@dataclass
class MessageEntity:
    """Encja w wiadomości (np. bold, italic, mention)"""
    type: str
    offset: int
    length: int
    url: Optional[str] = None
    user: Optional['User'] = None  # Odwołanie jako string
    language: Optional[str] = None
    custom_emoji_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'MessageEntity':
        # Import wewnątrz metody
        from .user import User

        return cls(
            type=data['type'],
            offset=data['offset'],
            length=data['length'],
            url=data.get('url'),
            user=User.from_dict(data['user']) if 'user' in data else None,
            language=data.get('language'),
            custom_emoji_id=data.get('custom_emoji_id')
        )


@dataclass
class MessageAutoDeleteTimerChanged:
    """Zmiana timera auto-usuwania"""
    message_auto_delete_time: int

    @classmethod
    def from_dict(cls, data: Dict) -> 'MessageAutoDeleteTimerChanged':
        return cls(
            message_auto_delete_time=data['message_auto_delete_time']
        )


@dataclass
class Message:
    """Obiekt reprezentujący wiadomość"""
    message_id: int
    date: datetime
    chat: 'Chat'  # Odwołanie jako string
    from_user: Optional['User'] = None
    sender_chat: Optional['Chat'] = None
    forward_from: Optional['User'] = None
    forward_from_chat: Optional['Chat'] = None
    forward_from_message_id: Optional[int] = None
    forward_signature: Optional[str] = None
    forward_sender_name: Optional[str] = None
    forward_date: Optional[datetime] = None
    reply_to_message: Optional['Message'] = None
    via_bot: Optional['User'] = None
    edit_date: Optional[datetime] = None
    has_protected_content: Optional[bool] = None
    media_group_id: Optional[str] = None
    author_signature: Optional[str] = None
    text: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    caption: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None

    # Media
    animation: Optional['Animation'] = None
    audio: Optional['Audio'] = None
    document: Optional['Document'] = None
    photo: Optional[List['PhotoSize']] = None
    sticker: Optional['Sticker'] = None
    video: Optional['Video'] = None
    video_note: Optional['VideoNote'] = None
    voice: Optional['Voice'] = None
    contact: Optional['Contact'] = None
    dice: Optional['Dice'] = None
    game: Optional['Game'] = None
    poll: Optional['Poll'] = None
    venue: Optional['Venue'] = None
    location: Optional['Location'] = None

    # Inne typy
    new_chat_members: Optional[List['User']] = None
    left_chat_member: Optional['User'] = None
    new_chat_title: Optional[str] = None
    new_chat_photo: Optional[List['PhotoSize']] = None
    delete_chat_photo: Optional[bool] = None
    group_chat_created: Optional[bool] = None
    supergroup_chat_created: Optional[bool] = None
    channel_chat_created: Optional[bool] = None
    message_auto_delete_timer_changed: Optional[MessageAutoDeleteTimerChanged] = None
    migrate_to_chat_id: Optional[int] = None
    migrate_from_chat_id: Optional[int] = None
    pinned_message: Optional['Message'] = None
    invoice: Optional['Invoice'] = None
    successful_payment: Optional['SuccessfulPayment'] = None
    connected_website: Optional[str] = None
    passport_data: Optional['PassportData'] = None
    proximity_alert_triggered: Optional['ProximityAlertTriggered'] = None
    video_chat_scheduled: Optional['VideoChatScheduled'] = None
    video_chat_started: Optional['VideoChatStarted'] = None
    video_chat_ended: Optional['VideoChatEnded'] = None
    video_chat_participants_invited: Optional['VideoChatParticipantsInvited'] = None
    web_app_data: Optional['WebAppData'] = None
    reply_markup: Optional['InlineKeyboardMarkup'] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Message':
        # Importy wewnątrz metody
        from .user import User, Chat
        from .media import PhotoSize, Animation, Audio, Document, Video, VideoNote, Voice, Sticker
        from .misc import Contact, Dice, Location, Venue, Poll, Game
        from .payments import Invoice, SuccessfulPayment
        from .passport import PassportData
        from .proximity import ProximityAlertTriggered
        from .video_chat import (
            VideoChatScheduled, VideoChatStarted, VideoChatEnded,
            VideoChatParticipantsInvited
        )
        from .web_app import WebAppData

        return cls(
            message_id=data['message_id'],
            date=datetime.fromtimestamp(data['date']),
            chat=Chat.from_dict(data['chat']),
            from_user=User.from_dict(data['from']) if 'from' in data else None,
            sender_chat=Chat.from_dict(data['sender_chat']) if 'sender_chat' in data else None,
            forward_from=User.from_dict(data['forward_from']) if 'forward_from' in data else None,
            forward_from_chat=Chat.from_dict(data['forward_from_chat']) if 'forward_from_chat' in data else None,
            forward_from_message_id=data.get('forward_from_message_id'),
            forward_signature=data.get('forward_signature'),
            forward_sender_name=data.get('forward_sender_name'),
            forward_date=datetime.fromtimestamp(data['forward_date']) if data.get('forward_date') else None,
            reply_to_message=Message.from_dict(data['reply_to_message']) if 'reply_to_message' in data else None,
            via_bot=User.from_dict(data['via_bot']) if 'via_bot' in data else None,
            edit_date=datetime.fromtimestamp(data['edit_date']) if data.get('edit_date') else None,
            has_protected_content=data.get('has_protected_content'),
            media_group_id=data.get('media_group_id'),
            author_signature=data.get('author_signature'),
            text=data.get('text'),
            entities=[MessageEntity.from_dict(e) for e in data['entities']] if 'entities' in data else None,
            caption=data.get('caption'),
            caption_entities=[MessageEntity.from_dict(e) for e in
                              data['caption_entities']] if 'caption_entities' in data else None,

            # Media
            animation=Animation.from_dict(data['animation']) if 'animation' in data else None,
            audio=Audio.from_dict(data['audio']) if 'audio' in data else None,
            document=Document.from_dict(data['document']) if 'document' in data else None,
            photo=[PhotoSize.from_dict(p) for p in data['photo']] if 'photo' in data else None,
            sticker=Sticker.from_dict(data['sticker']) if 'sticker' in data else None,
            video=Video.from_dict(data['video']) if 'video' in data else None,
            video_note=VideoNote.from_dict(data['video_note']) if 'video_note' in data else None,
            voice=Voice.from_dict(data['voice']) if 'voice' in data else None,
            contact=Contact.from_dict(data['contact']) if 'contact' in data else None,
            dice=Dice.from_dict(data['dice']) if 'dice' in data else None,
            game=Game.from_dict(data['game']) if 'game' in data else None,
            poll=Poll.from_dict(data['poll']) if 'poll' in data else None,
            venue=Venue.from_dict(data['venue']) if 'venue' in data else None,
            location=Location.from_dict(data['location']) if 'location' in data else None,

            # Inne
            new_chat_members=[User.from_dict(u) for u in
                              data['new_chat_members']] if 'new_chat_members' in data else None,
            left_chat_member=User.from_dict(data['left_chat_member']) if 'left_chat_member' in data else None,
            new_chat_title=data.get('new_chat_title'),
            new_chat_photo=[PhotoSize.from_dict(p) for p in
                            data['new_chat_photo']] if 'new_chat_photo' in data else None,
            delete_chat_photo=data.get('delete_chat_photo'),
            group_chat_created=data.get('group_chat_created'),
            supergroup_chat_created=data.get('supergroup_chat_created'),
            channel_chat_created=data.get('channel_chat_created'),
            message_auto_delete_timer_changed=MessageAutoDeleteTimerChanged.from_dict(
                data['message_auto_delete_timer_changed']) if 'message_auto_delete_timer_changed' in data else None,
            migrate_to_chat_id=data.get('migrate_to_chat_id'),
            migrate_from_chat_id=data.get('migrate_from_chat_id'),
            pinned_message=Message.from_dict(data['pinned_message']) if 'pinned_message' in data else None,
            invoice=Invoice.from_dict(data['invoice']) if 'invoice' in data else None,
            successful_payment=SuccessfulPayment.from_dict(
                data['successful_payment']) if 'successful_payment' in data else None,
            connected_website=data.get('connected_website'),
            passport_data=PassportData.from_dict(data['passport_data']) if 'passport_data' in data else None,
            proximity_alert_triggered=ProximityAlertTriggered.from_dict(
                data['proximity_alert_triggered']) if 'proximity_alert_triggered' in data else None,
            video_chat_scheduled=VideoChatScheduled.from_dict(
                data['video_chat_scheduled']) if 'video_chat_scheduled' in data else None,
            video_chat_started=VideoChatStarted.from_dict(
                data['video_chat_started']) if 'video_chat_started' in data else None,
            video_chat_ended=VideoChatEnded.from_dict(data['video_chat_ended']) if 'video_chat_ended' in data else None,
            video_chat_participants_invited=VideoChatParticipantsInvited.from_dict(
                data['video_chat_participants_invited']) if 'video_chat_participants_invited' in data else None,
            web_app_data=WebAppData.from_dict(data['web_app_data']) if 'web_app_data' in data else None
        )