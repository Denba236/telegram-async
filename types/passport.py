from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime


@dataclass
class PassportFile:
    """Plik passport"""
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: datetime

    @classmethod
    def from_dict(cls, data: Dict) -> 'PassportFile':
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            file_size=data['file_size'],
            file_date=datetime.fromtimestamp(data['file_date'])
        )


@dataclass
class EncryptedPassportElement:
    """Zaszyfrowany element passport"""
    type: str
    hash: str
    data: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    files: Optional[List[PassportFile]] = None
    front_side: Optional[PassportFile] = None
    reverse_side: Optional[PassportFile] = None
    selfie: Optional[PassportFile] = None
    translation: Optional[List[PassportFile]] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'EncryptedPassportElement':
        return cls(
            type=data['type'],
            hash=data['hash'],
            data=data.get('data'),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            files=[PassportFile.from_dict(f) for f in data['files']] if 'files' in data else None,
            front_side=PassportFile.from_dict(data['front_side']) if 'front_side' in data else None,
            reverse_side=PassportFile.from_dict(data['reverse_side']) if 'reverse_side' in data else None,
            selfie=PassportFile.from_dict(data['selfie']) if 'selfie' in data else None,
            translation=[PassportFile.from_dict(t) for t in data['translation']] if 'translation' in data else None
        )


@dataclass
class EncryptedCredentials:
    """Zaszyfrowane poświadczenia"""
    data: str
    hash: str
    secret: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'EncryptedCredentials':
        return cls(
            data=data['data'],
            hash=data['hash'],
            secret=data['secret']
        )


@dataclass
class PassportData:
    """Dane passport"""
    data: List[EncryptedPassportElement]
    credentials: EncryptedCredentials

    @classmethod
    def from_dict(cls, data: Dict) -> 'PassportData':
        return cls(
            data=[EncryptedPassportElement.from_dict(e) for e in data['data']],
            credentials=EncryptedCredentials.from_dict(data['credentials'])
        )