import logging


def replace_none_with_empty_str(some_dict):
    logging.info("Replacing dictionary None values with empty string")
    print(some_dict.items())
    return {('REPLACE' if k is None else k): ('' if v is None else v) for k, v in some_dict.items()}