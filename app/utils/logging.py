def get_logger(name: str = "rag"):
    """Simple fallback logger using Python's standard logging.
    This avoids requiring external logger configuration for quick tests.
    """
    import logging
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def log_request(logger, request_id: str, method: str, path: str, status_code: int, duration_ms: float):
    """Log a single HTTP-like request.
    """
    try:
        logger.info("request_complete", request_id=request_id, method=method, path=path, status_code=status_code, duration_ms=duration_ms)
    except Exception:
        pass
