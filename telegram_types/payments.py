from dataclasses import dataclass
from typing import Optional, Dict, List

from .user import User


@dataclass
class ShippingAddress:
    """Adres dostawy"""
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'ShippingAddress':
        return cls(
            country_code=data['country_code'],
            state=data['state'],
            city=data['city'],
            street_line1=data['street_line1'],
            street_line2=data['street_line2'],
            post_code=data['post_code']
        )


@dataclass
class OrderInfo:
    """Informacje o zamówieniu"""
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    shipping_address: Optional[ShippingAddress] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'OrderInfo':
        return cls(
            name=data.get('name'),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            shipping_address=ShippingAddress.from_dict(data['shipping_address']) if 'shipping_address' in data else None
        )


@dataclass
class Invoice:
    """Faktura"""
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int

    @classmethod
    def from_dict(cls, data: Dict) -> 'Invoice':
        return cls(
            title=data['title'],
            description=data['description'],
            start_parameter=data['start_parameter'],
            currency=data['currency'],
            total_amount=data['total_amount']
        )


@dataclass
class SuccessfulPayment:
    """Udana płatność"""
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None
    telegram_payment_charge_id: str
    provider_payment_charge_id: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'SuccessfulPayment':
        return cls(
            currency=data['currency'],
            total_amount=data['total_amount'],
            invoice_payload=data['invoice_payload'],
            shipping_option_id=data.get('shipping_option_id'),
            order_info=OrderInfo.from_dict(data['order_info']) if 'order_info' in data else None,
            telegram_payment_charge_id=data['telegram_payment_charge_id'],
            provider_payment_charge_id=data['provider_payment_charge_id']
        )


@dataclass
class ShippingQuery:
    """Zapytanie o dostawę"""
    id: str
    from_user: User
    invoice_payload: str
    shipping_address: ShippingAddress

    @classmethod
    def from_dict(cls, data: Dict) -> 'ShippingQuery':
        return cls(
            id=data['id'],
            from_user=User.from_dict(data['from']),
            invoice_payload=data['invoice_payload'],
            shipping_address=ShippingAddress.from_dict(data['shipping_address'])
        )


@dataclass
class PreCheckoutQuery:
    """Zapytanie przedpłatne"""
    id: str
    from_user: User
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'PreCheckoutQuery':
        return cls(
            id=data['id'],
            from_user=User.from_dict(data['from']),
            currency=data['currency'],
            total_amount=data['total_amount'],
            invoice_payload=data['invoice_payload'],
            shipping_option_id=data.get('shipping_option_id'),
            order_info=OrderInfo.from_dict(data['order_info']) if 'order_info' in data else None
        )