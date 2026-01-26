import pytest

from domain import left_right_switch


@pytest.mark.parametrize(
    "answer_config,toggle_left,toggle_right,expected_text,expected_config", (
        ((True, False), False, False, "Left carrot", (True, False)),
    )
)
def test_left_right_switch(
    answer_config,
    toggle_left,
    toggle_right,
    expected_text,
    expected_config,
):
    # Setup
    message_text = "carrot"

    # Run
    received_text, received_config = left_right_switch(
        message_text,
        answer_config,
        toggle_left,
        toggle_right,
    )

    # Check
    assert received_text == expected_text
    assert received_config == expected_config
