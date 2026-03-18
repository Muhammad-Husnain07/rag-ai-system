def flatten_list(list_of_lists):
    """Flatten a list of lists into a single list.

    If an element is not a list, it will be appended as-is.
    """
    if list_of_lists is None:
        return []
    result = []
    for item in list_of_lists:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result
