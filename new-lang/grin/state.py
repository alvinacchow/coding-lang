#state.py
#contains the structure to each grin program
import grin
import sys
class State:
    def __init__(self, lines: list) -> None:
        """Initiates the State object"""
        self._lines = lines
        self._events = self.read()
        self._identifiers = {}
        self._labels = self.labels()
        self._commands = self.label_command()
        self._go_x = {}

    def read(self) -> list[list[grin.GrinToken]]:
        """Parses the input lines and returns a nested list of tokens.
           If a ParsingError or LexError occurs, a GrinError message is
           printed and the program ends"""
        try:
            parsed = grin.parsing.parse(self._lines)
            i_parsed = iter(parsed)
            events = []
            try:
                while True:
                    events.append(next(i_parsed))
            except StopIteration:
                return events
        except (grin.GrinParseError, grin.GrinLexError) as e:
            print(f'ERROR AT LINE {e.location().line()}: FAILED TO PARSE INPUT')
            sys.exit()

    def identifiers(self, line: list[grin.GrinToken]) -> None:
        """Adds to the identifier dictionary with the corresponding
           value"""
        if line[0].kind() == grin.GrinTokenKind.LET:
            key = line[1].text()
            if line[2].kind() == grin.GrinTokenKind.IDENTIFIER:
                if not line[2].text() in self._identifiers.keys():
                    self._identifiers[line[2].text()] = 0
                value = self._identifiers[line[2].text()]
            else:
                value = line[2].value()
            self._identifiers[key] = value

    def labels(self) -> dict:
        """Adds labels and their commands into a dictionary and
           returns that dictionary"""
        labels = dict()
        for line in range(len(self._events)):
            token = self._events[line]
            try:
                if token[1].kind() == grin.GrinTokenKind.COLON:
                    new_events = self._events[token[1].location().line()-1:]
                    labels[token[0].value()] = new_events
            except IndexError:
                pass
        return labels

    def label_command(self) -> dict:
        """Extracts the command from a label"""
        commands = dict()
        for line in range(len(self._events)):
            token = self._events[line]
            try:
                if token[1].kind() == grin.GrinTokenKind.COLON:
                    value = [token[x] for x in range(2, len(token))]
                    commands[token[0].value()] = value
            except IndexError:
                pass
        return commands
    def is_math(self, line: list) -> bool:
        """Checks to see if a line contains a math operation"""
        return line[0].kind() == grin.GrinTokenKind.ADD or \
        line[0].kind() == grin.GrinTokenKind.SUB or \
        line[0].kind() == grin.GrinTokenKind.MULT or \
        line[0].kind() == grin.GrinTokenKind.DIV

    def is_literal(self, line: list) -> bool:
        """Checks to see if the second character of a line
           is a literal value"""
        return line[1].kind() == grin.GrinTokenKind.LITERAL_STRING or \
               line[1].kind() == grin.GrinTokenKind.LITERAL_FLOAT or \
               line[1].kind() == grin.GrinTokenKind.LITERAL_INTEGER

    def do_math(self, line: list) -> None:
        """Computes math operation from a given line. If this fails,
           prints a GrinError message and ends the program"""
        if line[1].value() not in self._identifiers.keys():
            self._identifiers[line[1].value()] = 0
        if line[2].kind() == grin.GrinTokenKind.IDENTIFIER:
            second = self._identifiers[line[2].text()]
        else:
            second = line[2].value()

        try:
            if line[0].kind() == grin.GrinTokenKind.ADD:
                self._identifiers[line[1].value()] += second
            elif line[0].kind() == grin.GrinTokenKind.SUB:
                self._identifiers[line[1].value()] -= second
            elif line[0].kind() == grin.GrinTokenKind.MULT:
                self._identifiers[line[1].value()] *= second
            else:
                if type(self._identifiers[line[1].value()]) == int and type(second) == int:
                    self._identifiers[line[1].value()] = self._identifiers[line[1].value()] // second
                else:
                    self._identifiers[line[1].value()] = self._identifiers[line[1].value()] / second
        except TypeError:
            print(f'ERROR AT LINE {line[0].location().line()}: FAILED TO COMPUTE DUE TO INCOMPATIBLE TYPES')
            sys.exit()
        except ZeroDivisionError:
            print(f'ERROR AT LINE {line[0].location().line()}: CANNOT DIVIDE BY ZERO')
            sys.exit()

    def input_num(self, line: list) -> None:
        """Takes an input number and converts it
           to the corresponding type"""
        entry = input()
        i = grin.to_int(entry)
        f = grin.to_float(entry)
        self._identifiers[line[1].value()] = i if i is not None else f

    def retrieve_value(self, line: list) -> bool:
        """Gets the stored value inside an identifier if necessary.
           Compares the two values by calling check_condition()"""
        value1 = line[0].value()
        value2 = line[2].value()

        if line[0].kind() == grin.GrinTokenKind.IDENTIFIER or line[2].kind() == grin.GrinTokenKind.IDENTIFIER:
            if line[0].kind() == grin.GrinTokenKind.IDENTIFIER:
                if line[0].value() not in self._identifiers:
                    self._identifiers[line[0].value()] = 0
                value1 = self._identifiers[line[0].value()]

            if line[2].kind() == grin.GrinTokenKind.IDENTIFIER:
                if line[2].value() not in self._identifiers:
                    self._identifiers[line[2].value()] = 0
                value2 = self._identifiers[line[2].value()]
        return self.check_condition(line, value1, value2)

    def check_condition(self, line: list, value1: str | float | int, value2: str | float | int) -> bool:
        """Compares two values and returns the boolean result. If failed,
           prints a GrinError and ends the program"""
        sign = line[1].kind()
        try:
            if sign == grin.GrinTokenKind.LESS_THAN:
                return value1 < value2
            elif sign == grin.GrinTokenKind.LESS_THAN_OR_EQUAL:
                return value1 <= value2
            elif sign == grin.GrinTokenKind.GREATER_THAN:
                return value1 > value2
            elif sign == grin.GrinTokenKind.GREATER_THAN_OR_EQUAL:
                return value1 >= value2
            elif sign == grin.GrinTokenKind.EQUAL:
                return value1 == value2
            elif sign == grin.GrinTokenKind.NOT_EQUAL:
                return value1 != value2
        except TypeError:
            print(f'ERROR AT LINE {line[0].location().line()}: CANNOT COMPARE TYPES')
            sys.exit()

    def print_grin(self, line: list) -> None:
        """Prints a result given the line"""
        if self.is_literal(line):
            print(line[1].value())
        elif line[1].value() in self._identifiers.keys():
            print(self._identifiers[line[1].value()])
        else:
            self._identifiers[line[1].value()] = 0
            print(self._identifiers[line[1].value()])

    def get_line(self, label: str) -> int:
        """Given a label, gets the line location of the
           label's command"""
        for element in self._labels.keys():
            if element == label:
                value = self._labels[element][0][0]
                return value.location().line()

    def execute_go(self, line: list, kind: str) -> bool:
        """Executes a "GO" statement depending on whether the target
           is an integer or is stored in a label or identifier. If
           failed, a GrinError message is printed and the program ends"""
        valid = True
        try:
            if len(line) > 2:
                valid = self.retrieve_value(line[3:])
            if valid:
                if type(line[1].value()) == int:
                    limit = line[1].location().line() + line[1].value()
                    if limit > len(self._events) or limit < 0:
                        print(f'ERROR AT LINE {line[0].location().line()}: TARGET LINE IS OUT OF BOUNDS')
                        sys.exit()
                    else:
                        self.go_to_int(line, 1, kind)
                else:

                    if line[1].value() in self._labels.keys():
                        self.go_to_label(line, 1, kind)
                    elif line[1].value() in self._identifiers.keys():
                        self.go_to_identifier(line, 1, kind)
            return valid
        except RecursionError:
            print(f'ERROR AT LINE {line[0].location().line()}: MAXIMUM RECURSION REACHED')
            sys.exit()

    def construct_go(self, kind: str, target: list, events: list) -> 'grin.GoSub | grin.GoTo':
        """Creates and returns a GoSub or GoTo object depending
           on the type required"""
        if kind == 'GOTO':
            go = grin.GoTo(target, events)
        else:
            go = grin.GoSub(target, events)
        return go

    def go_to_int(self, line: list, i: int, kind: str) -> None:
        """Executes a go statement that has an integer target"""
        element = line[i]
        value = element.value()
        location = element.location().line()
        new_events = self._events[location+value-1:]
        go_statement = self.construct_go(kind, line, new_events)
        self._go_x[element.location().line()] = go_statement
        self.process_grin(events = [go_statement.get_statement()])

    def go_to_label(self, line: list, i: int, kind: str) -> None:
        """Executes a go statement that has a label target"""
        element = line[i]
        new_events = self._labels[element.value()]
        new_events[0] = self._commands[line[i].value()]
        go_statement = self.construct_go(kind, line, new_events)
        self._go_x[element.location().line()] = go_statement
        self.process_grin(events = [go_statement.get_statement()])

    def go_to_identifier(self, line: list, i: int, kind: str) -> None:
        """Executes a go statement that has a target stored inside
           an identifier. Prints a GrinError and exits the program
           if failed"""
        element = line[i]
        c = self.convert(element.value())
        if type(c) == int:
            limit = element.location().line() + c - 1
            if limit > len(self._events) or limit < 0:
                print(f'ERROR AT LINE {line[0].location().line()}: TARGET LINE IS OUT OF BOUNDS')
                sys.exit()
            else:
                new_events = self._events[limit:]
                go_statement = self.construct_go(kind, line, new_events)
                self._go_x[element.location().line()] = go_statement
                self.process_grin(events = [go_statement.get_statement()])
        elif c in self._labels.keys():
            self.go_to_label(self._labels[c][0], 0, kind)

    def convert(self, value: str) -> str | int | float:
        """Given the key of a dictionary, returns the key's value"""
        if value in self._identifiers.keys():
            new_key = self._identifiers[value]
            return new_key

    def process_grin(self, events: list = None) -> None:
        """Processes and executes events"""
        if events is None:
            events = [self._events]

        i = events[0]
        for line in i:
            if line[0].kind() == grin.GrinTokenKind.END or line[0].kind() == grin.GrinTokenKind.RETURN:
                return
            elif line[0].kind() == grin.GrinTokenKind.LET:
                self.identifiers(line)
            elif line[0].kind() == grin.GrinTokenKind.PRINT:
                self.print_grin(line)
            elif self.is_math(line):
                self.do_math(line)
            elif line[0].kind() == grin.GrinTokenKind.INSTR:
                self._identifiers[line[1].value()] = input()
            elif line[0].kind() == grin.GrinTokenKind.INNUM:
                self.input_num(line)
            elif line[0].kind() == grin.GrinTokenKind.GOTO:
                result = self.execute_go(line, 'GOTO')
                if result is True:
                    return
            elif line[0].kind() == grin.GrinTokenKind.GOSUB:
                self.execute_go(line, 'GOSUB')


    def get_identifiers(self) -> dict:
        """Returns the identifier dictionary"""
        return self._identifiers

    def get_labels(self) -> dict:
        """Returns the labels dictionary"""
        return self._labels

    def get_commands(self) -> dict:
        """Returns the commands dictionary"""
        return self._commands

__all__ = [State.__name__]