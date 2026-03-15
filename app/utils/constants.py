ERROR_CODES = {
    "AUTH_001": "Invalid credentials",
    "AUTH_002": "Token expired",
    "AUTH_003": "User already exists",
    "AUTH_004": "User not found",
    "DOC_001": "Document not found",
    "DOC_002": "Document processing failed",
    "DOC_003": "Unsupported file type",
    "DOC_004": "File too large",
    "CHAT_001": "No relevant context found",
    "CHAT_002": "Conversation not found",
    "SYS_001": "Rate limit exceeded",
    "SYS_002": "Internal server error",
    "VAL_001": "Validation error",
    "PER_001": "Permission denied",
}

# Public API
__all__ = ["ERROR_CODES", "get_error_message"]


def get_error_message(code: str, default: str = "An error occurred") -> str:
    """Get error message by code."""
    return ERROR_CODES.get(code, default)
