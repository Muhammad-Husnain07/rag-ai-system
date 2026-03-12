from typing import Any, Dict, List, Optional


def build_filters(
    allowed_fields: List[str],
    params: Dict[str, Any]
) -> Dict[str, Any]:
    """Build filters dictionary from allowed parameters."""
    filters = {}
    
    for key, value in params.items():
        if key in allowed_fields and value is not None:
            filters[key] = value
    
    return filters


def apply_pagination(
    query: Any,
    page: int = 1,
    page_size: int = 20
):
    """Apply pagination to query."""
    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size)


def build_sorting(
    allowed_fields: List[str],
    sort_by: str,
    order: str = "asc"
):
    """Build sorting parameters."""
    if sort_by not in allowed_fields:
        return None
    
    from sqlalchemy import asc, desc
    
    if order.lower() == "desc":
        return desc(sort_by)
    return asc(sort_by)


def sanitize_search_query(query: str) -> str:
    """Sanitize search query input."""
    import re
    query = query.strip()
    query = re.sub(r'[^\w\s-]', '', query)
    return query[:200]
