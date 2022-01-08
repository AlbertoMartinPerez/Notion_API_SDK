
def get_page_id(
    link : str) -> str:
    """
    Get page ID from Notion URL.

    Example
    -------
    >>> link = https://www.notion.so/Page-Title-7a5ddb2c3d48314e9775d2c49212be12
    >>> print(get_page_id(link))
    7a5ddb2c3d48314e9775d2c49212be12
    """
    return link.split('-')[-1]