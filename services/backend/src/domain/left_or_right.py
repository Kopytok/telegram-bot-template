def left_or_right(
    text: str,
    left: bool,
    right: bool,
) -> str:
    if left:
        return "Left " + text
    if right:
        return text + " Right"
    else:
        return text
