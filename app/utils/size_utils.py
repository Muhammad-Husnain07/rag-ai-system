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
