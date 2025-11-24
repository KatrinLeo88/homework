from typing import Union

from src.logger import setup_logger

logger = setup_logger("masks", "masks.log")


def get_mask_card_number(card_number: Union[int, str]) -> str:
    """функция маскировки номера банковской карты"""
    logger.debug("Начало работы функции get_mask_card_number")
    try:
        card_number_str = str(card_number)
    except Exception as e:
        logger.error(e)
        raise e
    return (
        card_number_str[0:-16]
        + card_number_str[-16:-12]
        + " "
        + card_number_str[-12:-10]
        + "**"
        + " **** "
        + card_number_str[-4:]
    )


def get_mask_account(mask_account: Union[int, str]) -> str:
    """функция маскировки номера банковского счета"""
    logger.debug("Начало работы функции get_mask_account")
    mask_account_str = str(mask_account)
    try:
        return mask_account_str[0:5] + " **" + mask_account_str[-4:]
    except IndexError as e:
        logger.error(e)
        raise e
