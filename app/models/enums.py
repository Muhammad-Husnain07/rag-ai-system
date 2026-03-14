from enum import Enum


class DocumentStatus(str, Enum):
    """Document processing status."""
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class UserRole(str, Enum):
    """User roles."""
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class NotificationPriority(str, Enum):
    """Notification priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ChunkStrategy(str, Enum):
    """Text chunking strategies."""
    FIXED_SIZE = "fixed_size"
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"
