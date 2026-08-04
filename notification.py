from plyer import notification


def send_plyer(title: str, message: str, timeout :int=5):
    """
    Send a notification to the user. using `plyer`_.notification.

    Args:
        title(str):
        message(str): message to send with notification.
        timeout(int):

    Returns:
        None

    .. _plyer: https://pypi.org/project/plyer/
    """
    notification.notify(
        title=title,
        message=message,
        timeout=timeout,
    ) # type: ignore
