def bytes_to_human_readable(size_bytes: int) -> str:
    """Convert bytes to human readable format."""
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = float(size_bytes)
    unit_index = 0
    
    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    
    return f"{size:.2f} {units[unit_index]}"


def human_readable_to_bytes(size_str: str) -> int:
    """Convert human readable size to bytes."""
    units = {'B': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3, 'TB': 1024**4}
    
    size_str = size_str.upper().strip()
    
    for unit, multiplier in units.items():
        if size_str.endswith(unit):
            value = float(size_str[:-len(unit)].strip())
            return int(value * multiplier)
    
    return int(size_str)

def is_large_file(size_bytes: int, threshold_mb: int = 10) -> bool:
    """Return True if file size exceeds threshold (in MB)."""
    return size_bytes >= threshold_mb * 1024 * 1024


def bytes_to_kb(size_bytes: int) -> float:
    """Convert bytes to kilobytes."""
    return size_bytes / 1024.0


def bytes_to_mb(size_bytes: int) -> float:
    """Convert bytes to megabytes."""
    return size_bytes / (1024.0 * 1024.0)


def format_bytes(size_bytes: int, decimals: int = 2) -> str:
    """Format bytes with appropriate unit suffix."""
    if size_bytes == 0:
        return "0 B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    unit_index = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    
    return f"{size:.{decimals}f} {units[unit_index]}"
