from typing import Annotated, Iterable

from pydantic import BeforeValidator


def create_list(_input: str | list[str] | None) -> list[str]:
    if _input is None:
        return []
    if isinstance(_input, str):
        return [_input]
    if isinstance(_input, list):
        return _input
    if isinstance(_input, Iterable):
        return list(_input)
    raise ValueError


StrList = Annotated[list[str], create_list]


def str_to_int(__input: int | str) -> int:
    if isinstance(__input, int):
        return __input

    return int(__input.replace(" ", ""))


Int = Annotated[int, BeforeValidator(str_to_int)]
