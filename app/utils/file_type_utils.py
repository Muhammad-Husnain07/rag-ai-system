def normalize_extension(ext: str) -> str:
    """Normalize a file extension to a standard form.
    - Ensures a leading dot
    - Converts to lowercase
    - If input is None or empty, returns an empty string
    """
    if not ext:
        return ""
    if not ext.startswith("."):
        ext = "." + ext
    return ext.lower()


def is_image_file(filename: str) -> bool:
    """Check if file is an image based on extension."""
    image_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico"}
    return normalize_extension(filename) in image_exts


def is_video_file(filename: str) -> bool:
    """Check if file is a video based on extension."""
    video_exts = {".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv", ".webm"}
    return normalize_extension(filename) in video_exts


def is_audio_file(filename: str) -> bool:
    """Check if file is an audio based on extension."""
    audio_exts = {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"}
    return normalize_extension(filename) in audio_exts


def is_document_file(filename: str) -> bool:
    """Check if file is a document based on extension."""
    doc_exts = {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"}
    return normalize_extension(filename) in doc_exts


def is_archive_file(filename: str) -> bool:
    """Check if file is an archive based on extension."""
    archive_exts = {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"}
    return normalize_extension(filename) in archive_exts
