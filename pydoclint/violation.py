import types

from pydoclint.internal_error import InternalError


VIOLATION_CODES = types.MappingProxyType({
    101: 'Docstring contains fewer arguments than in function signature.',
    102: 'Docstring contains more arguments than in function signature.',
    103: 'Docstring arguments are different from function arguments.',
    104: 'Arguments are the same in the docstring and the function signature, but are in a different order.',
    105: 'Argument names match, but type hints do not match',
    201: 'does not have a return section in docstring',
    202: 'has a return section in docstring, but there are no return statements or annotations',
})


class Violation():
    def __init__(
            self,
            code: int,
            msgPrefix: str = '',
            msgPostfix: str = '',
    ) -> None:
        if code not in VIOLATION_CODES:
            raise InternalError('Invalid violation code')

        self.code = code
        self.msg = msgPrefix + ' ' + VIOLATION_CODES[code] + ' ' + msgPostfix

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'DOC{self.code}: {self.msg}'
