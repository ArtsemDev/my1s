from typing import Annotated
from re import compile

from annotated_types import Predicate

__all__ = ["PasswordStr"]


PasswordPattern = compile(pattern=r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,72}$")

PasswordStr = Annotated[str, Predicate(func=lambda x: PasswordPattern.fullmatch(string=x) is not None)]
