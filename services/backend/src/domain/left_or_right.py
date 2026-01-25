def left_or_right(
    text: str,
    left: bool,
    right: bool,
) -> str:
    output = text
    if left:
        output = "Left " + output
    if right:
        output = output + " Right"
    return output
