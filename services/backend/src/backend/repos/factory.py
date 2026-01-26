from backend.db import engine
from backend.repos.sql.account import SqlAccountRepo
from backend.repos.sql.user_message import SqlUserMessageRepo
from backend.repos.sql.bot_message import SqlBotMessageRepo
from backend.repos.sql.answer_config import SqlAnswerConfigRepo


def get_account_repo():
    return SqlAccountRepo(engine)


def get_user_message_repo():
    return SqlUserMessageRepo(engine)


def get_bot_message_repo():
    return SqlBotMessageRepo(engine)


def get_answer_config_repo():
    return SqlAnswerConfigRepo(engine)
