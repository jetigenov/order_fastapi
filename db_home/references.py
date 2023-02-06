import enum


class Status(enum.Enum):
    PENDING = 'pending'
    IN_TRANSIT = 'in_transit'
    DELIVERED = 'delivered'


class Size(enum.Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
