from typing import Tuple


def left_right_switch(
    message_text: str,
    answer_config: Tuple[bool, bool],
    toggle_left: bool,
    toggle_right: bool,
) -> Tuple[str, Tuple[bool, bool]]:
    output_config = []

    if toggle_left:
        output_config.append(not answer_config[0])
    else:
        output_config.append(answer_config[0])

    if toggle_right:
        output_config.append(not answer_config[1])
    else:
        output_config.append(answer_config[1])

    text = message_text
    if output_config[0]:
        text = "Left " + text

    if output_config[1]:
        text = text + " Right"

    return text, tuple(output_config)
