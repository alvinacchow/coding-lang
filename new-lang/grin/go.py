#go.py
#contains GoTo and GoSub classes, which have an inherited relationship
import grin
class GoTo:
    def __init__(self, target: list, statement: list) -> None:
        """Initiates the GoTo object"""
        self._target = target
        self._statement = statement
        self.modify()

    def modify(self) -> None:
        """Removes the label from a line to extract the command"""
        for line in range(len(self._statement)):
            for token in self._statement[line]:
                if token.kind() == grin.GrinTokenKind.COLON:
                    self._statement[line] = self._statement[line][2:]

    def get_statement(self) -> list:
        """Returns action statements"""
        return self._statement

class GoSub(GoTo):
    def __init__(self, target: list, statement: list) -> None:
        """Initiates GoSub object using parent __init__ method"""
        super().__init__(target, statement)
        self._line_num = self._target[0].location().line()