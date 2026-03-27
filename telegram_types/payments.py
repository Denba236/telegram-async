from dataclasses import dataclass
from typing import Optional, Dict, List, Any

from .user import User
from .base import TelegramObject


@dataclass
class LabeledPrice(TelegramObject):
    """Labeled price"""
    label: str
    amount: int

    @classmethod
    def from_dict(cls, data: Dict) -> 'LabeledPrice':
        return cls(
            label=data['label'],
            amount=data['amount']
        )


@dataclass
class Invoice(TelegramObject):
    """Invoice"""
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
class ShippingAddress(TelegramObject):
    """Shipping address"""
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
class OrderInfo(TelegramObject):
    """Order information"""
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    shipping_address: Optional[ShippingAddress] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'OrderInfo':
        shipping_address = None
        if 'shipping_address' in data:
            shipping_address = ShippingAddress.from_dict(data['shipping_address'])

        return cls(
            name=data.get('name'),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            shipping_address=shipping_address
        )


@dataclass
class SuccessfulPayment(TelegramObject):
    """Successful payment"""
    currency: str
    total_amount: int
    invoice_payload: str
    telegram_payment_charge_id: str
    provider_payment_charge_id: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'SuccessfulPayment':
        order_info = None
        if 'order_info' in data:
            order_info = OrderInfo.from_dict(data['order_info'])

        return cls(
            currency=data['currency'],
            total_amount=data['total_amount'],
            invoice_payload=data['invoice_payload'],
            telegram_payment_charge_id=data['telegram_payment_charge_id'],
            provider_payment_charge_id=data['provider_payment_charge_id'],
            shipping_option_id=data.get('shipping_option_id'),
            order_info=order_info
        )


@dataclass
class ShippingOption(TelegramObject):
    """Shipping option"""
    id: str
    title: str
    prices: List[LabeledPrice]

    @classmethod
    def from_dict(cls, data: Dict) -> 'ShippingOption':
        prices = [LabeledPrice.from_dict(price) for price in data['prices']]

        return cls(
            id=data['id'],
            title=data['title'],
            prices=prices
        )


# Payment callback classes
@dataclass
class PreCheckoutQuery(TelegramObject):
    """Pre-checkout query"""
    id: str
    from_user: User
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None

    def __post_init__(self):
        if isinstance(self.from_user, dict):
            self.from_user = User.from_dict(self.from_user)
        if isinstance(self.order_info, dict):
            self.order_info = OrderInfo.from_dict(self.order_info)

    @classmethod
    def from_dict(cls, data: Dict) -> 'PreCheckoutQuery':
        from_user = User.from_dict(data['from'])
        order_info = None
        if 'order_info' in data:
            order_info = OrderInfo.from_dict(data['order_info'])

        return cls(
            id=data['id'],
            from_user=from_user,
            currency=data['currency'],
            total_amount=data['total_amount'],
            invoice_payload=data['invoice_payload'],
            shipping_option_id=data.get('shipping_option_id'),
            order_info=order_info
        )


@dataclass
class ShippingQuery(TelegramObject):
    """Shipping query"""
    id: str
    from_user: User
    invoice_payload: str
    shipping_address: ShippingAddress

    def __post_init__(self):
        if isinstance(self.from_user, dict):
            self.from_user = User.from_dict(self.from_user)
        if isinstance(self.shipping_address, dict):
            self.shipping_address = ShippingAddress.from_dict(self.shipping_address)

    @classmethod
    def from_dict(cls, data: Dict) -> 'ShippingQuery':
        from_user = User.from_dict(data['from'])
        shipping_address = ShippingAddress.from_dict(data['shipping_address'])

        return cls(
            id=data['id'],
            from_user=from_user,
            invoice_payload=data['invoice_payload'],
            shipping_address=shipping_address
        )


# Response classes
@dataclass
class AnswerPreCheckoutQuery:
    """Response to pre-checkout query"""
    ok: bool
    pre_checkout_query_id: str
    error_message: Optional[str] = None

    def to_dict(self) -> Dict:
        result = {
            'ok': self.ok,
            'pre_checkout_query_id': self.pre_checkout_query_id
        }
        if self.error_message:
            result['error_message'] = self.error_message
        return result


@dataclass
class AnswerShippingQuery:
    """Response to shipping query"""
    ok: bool
    shipping_query_id: str
    shipping_options: Optional[List[ShippingOption]] = None
    error_message: Optional[str] = None

    def to_dict(self) -> Dict:
        result = {
            'ok': self.ok,
            'shipping_query_id': self.shipping_query_id
        }
        if self.shipping_options:
            result['shipping_options'] = [opt.to_dict() for opt in self.shipping_options]
        if self.error_message:
            result['error_message'] = self.error_message
        return result
