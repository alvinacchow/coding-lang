#test_state.py
#conducts tests for the grin.State class

import unittest
import grin
import contextlib
import io

class ProgramLogistics(unittest.TestCase):
    def test_cannot_parse_invalid_input_lines(self):
        lines = ['ABCDEF']
        with contextlib.redirect_stdout(io.StringIO()) as output:
            try:
                grin.State(lines)
            except (grin.GrinParseError, grin.GrinLexError, SystemExit):
                pass
            self.assertEqual(output.getvalue(), 'ERROR AT LINE 1: FAILED TO PARSE INPUT\n')

    def test_get_line_of_first_label_action(self):
        lines = ['LABEL1: PRINT A', 'LABEL2: PRINT B', 'GOTO A']
        program = grin.State(lines)
        self.assertEqual(program.get_line('LABEL1'), 1)

    def test_get_line_of_second_label_action(self):
        lines = ['LABEL1: PRINT A', 'LABEL2: PRINT B', 'GOTO A']
        program = grin.State(lines)
        self.assertEqual(program.get_line('LABEL2'), 2)

    def test_cannot_get_line_of_nonexistent_label(self):
        lines = ['PRINT A', 'GOTO "HELLO"']
        program = grin.State(lines)
        self.assertEqual(program.get_line('HELLO'), None)

    def test_successfully_get_value_from_key(self):
        lines = ['LET A "HELLO"', 'HELLO: PRINT 4']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.convert('A'), 'HELLO')

    def test_cannot_get_value_from_nonexistent_key(self):
        lines = ['LET A "HELLO"', 'HELLO: PRINT 4']
        program = grin.State(lines)
        program.process_grin()
        self.assertIsNone(program.convert('AA'))

class IdentifierTests(unittest.TestCase):
    def test_integer_identifiers_created_correctly(self):
        lines = ['LET A 10', 'LET B 30']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers(), {'A': 10, 'B': 30})

    def test_float_identifiers_created_correctly(self):
        lines = ['LET A 1.23', 'LET B 3.22']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers(), {'A': 1.23, 'B': 3.22})

    def test_string_identifiers_created_correctly(self):
        lines = ['LET A "HELLO"', 'LET B "WORLD"']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers(), {'A': 'HELLO', 'B': 'WORLD'})

    def test_identifiers_equal_to_other_identifiers(self):
        lines = ['LET A 10', 'LET B A', 'LET C B']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers(), {'A': 10, 'B': 10, 'C': 10})

    def test_default_var_value_is_zero(self):
        lines = ['PRINT A']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()):
            program.process_grin()
            self.assertEqual(program.get_identifiers()['A'], 0)

    def test_add_to_default_var(self):
        lines = ['PRINT A', 'ADD A 3', 'PRINT A']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()):
            program.process_grin()
            self.assertEqual(program.get_identifiers()['A'], 3)

    def test_identifier_is_not_created_from_non_identifier_input(self):
        lines = ['PRINT A']
        program = grin.State(lines)
        program.identifiers(program._events[0])
        self.assertFalse('A' in program.get_identifiers())

    def test_set_variable_to_nonexistent_variable(self):
        lines = ['LET A B']
        program = grin.State(lines)
        program.identifiers(program._events[0])
        self.assertEqual(program.get_identifiers(), {'A': 0, 'B' : 0})

class LabelTest(unittest.TestCase):
    def test_label_is_created(self):
        lines = ['LABEL: PRINT "HELLO"', 'SECOND: LET A 10']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()):
            program.process_grin()
            self.assertEqual(len(program.get_labels()), 2)
            self.assertTrue('LABEL' in program.get_labels().keys())
            self.assertTrue('SECOND' in program.get_labels().keys())
            self.assertEqual(len(program.get_labels()['LABEL'][0]), 4)
            self.assertEqual(len(program.get_labels()['SECOND'][0]), 5)
            self.assertEqual(len(program.get_commands()['LABEL']), 2)
            self.assertEqual(len(program.get_commands()['SECOND']), 3)
            for value in program.get_labels().values():
                for sublist in value:
                    for element in sublist:
                        self.assertTrue(isinstance(element, grin.GrinToken))

class TestPrintTypes(unittest.TestCase):
    def test_print_identifier(self):
        lines = ['LET A 10', 'PRINT A']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue()[:-1], '10')

    def test_print_string(self):
        lines = ['PRINT "HELLO WORLD"']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue()[:-1], 'HELLO WORLD')

    def test_print_integer(self):
        lines = ['PRINT 20']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue()[:-1], '20')

    def test_print_float(self):
        lines = ['PRINT 1.23']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue()[:-1], '1.23')

    def test_print_unnamed_variable(self):
        lines = ['PRINT A']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue()[:-1], '0')

class ComparisonTests(unittest.TestCase):
    def test_int_is_less_than_int(self):
        lines = ['GOTO A IF 3 < 5']
        program = grin.State(lines)
        condition = program._events[0][3:]
        self.assertTrue(program.retrieve_value(condition))

    def test_int_is_less_than_or_equal_to_int(self):
        lines = ['GOTO A IF 3 <= 5']
        program = grin.State(lines)
        condition = program._events[0][3:]
        self.assertTrue(program.retrieve_value(condition))

    def test_int_is_greater_than_int(self):
        lines = ['GOTO A IF 5 > 4']
        program = grin.State(lines)
        condition = program._events[0][3:]
        self.assertTrue(program.retrieve_value(condition))

    def test_int_is_greater_than_or_equal_to_int(self):
        lines = ['GOTO A IF 5 >= 5']
        program = grin.State(lines)
        condition = program._events[0][3:]
        self.assertTrue(program.retrieve_value(condition))

    def test_int_is_equal_to_int(self):
        lines = ['GOTO A IF 5 = 5']
        program = grin.State(lines)
        condition = program._events[0][3:]
        self.assertTrue(program.retrieve_value(condition))

    def test_int_is_not_equal_to_int(self):
        lines = ['GOTO A IF 3 <> 5']
        program = grin.State(lines)
        condition = program._events[0][3:]
        self.assertTrue(program.retrieve_value(condition))

    def test_string_is_less_than_string(self):
        lines = ['GOTO A IF "A" < "B"']
        program = grin.State(lines)
        condition = program._events[0][3:]
        self.assertTrue(program.retrieve_value(condition))

    def test_string_is_greater_than_string(self):
        lines = ['GOTO A IF "B" > "A"']
        program = grin.State(lines)
        condition = program._events[0][3:]
        self.assertTrue(program.retrieve_value(condition))

    def test_string_is_equal_to_string(self):
        lines = ['GOTO A IF "A" = "A"']
        program = grin.State(lines)
        condition = program._events[0][3:]
        self.assertTrue(program.retrieve_value(condition))

    def test_string_is_not_equal_to_string(self):
        lines = ['GOTO A IF "A" <> "B"']
        program = grin.State(lines)
        condition = program._events[0][3:]
        self.assertTrue(program.retrieve_value(condition))

    def test_float_is_equal_to_int(self):
        lines = ['GOTO A IF 1.0 = 1']
        program = grin.State(lines)
        condition = program._events[0][3:]
        self.assertTrue(program.retrieve_value(condition))

    def test_float_is_not_equal_to_int(self):
        lines = ['GOTO A IF 2.0 <> 1']
        program = grin.State(lines)
        condition = program._events[0][3:]
        self.assertTrue(program.retrieve_value(condition))

    def test_float_is_greater_than_int(self):
        lines = ['GOTO A IF 2.0 > 1']
        program = grin.State(lines)
        condition = program._events[0][3:]
        self.assertTrue(program.retrieve_value(condition))

    def test_float_is_less_than_int(self):
        lines = ['GOTO A IF 2.0 < 10']
        program = grin.State(lines)
        condition = program._events[0][3:]
        self.assertTrue(program.retrieve_value(condition))

    def test_cannot_compare_int_and_string(self):
        lines = ['GOTO A IF 2 < "HELLO"']
        program = grin.State(lines)
        condition = program._events[0][3:]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            try:
                program.retrieve_value(condition)
            except (TypeError, SystemExit):
                pass
        self.assertEqual(output.getvalue(), 'ERROR AT LINE 1: CANNOT COMPARE TYPES\n')

    def test_cannot_compare_float_and_string(self):
        lines = ['GOTO A IF 3.0 < "HELLO"']
        program = grin.State(lines)
        condition = program._events[0][3:]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            try:
                program.retrieve_value(condition)
            except (TypeError, SystemExit):
                pass
        self.assertEqual(output.getvalue(), 'ERROR AT LINE 1: CANNOT COMPARE TYPES\n')

class GoTestsWithTrueComparisonInIdentifiers(unittest.TestCase):
    def test_less_than_in_identifiers(self):
        lines = ['LET A 3', 'LET B 4', 'GOTO 2 IF A < B', 'END', 'PRINT A', 'END']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            condition = program._events[2][3:]
            self.assertEqual(output.getvalue(), '3\n')
            self.assertTrue(program.retrieve_value(condition))

    def test_greater_than_in_identifiers(self):
        lines = ['LET A 5', 'LET B 4', 'GOTO 2 IF A > B', 'END', 'PRINT A', 'END']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            condition = program._events[2][3:]
            self.assertEqual(output.getvalue(), '5\n')
            self.assertTrue(program.retrieve_value(condition))

    def test_greater_than_or_equal_to_in_identifiers(self):
        lines = ['LET A 5', 'LET B 4', 'GOTO 2 IF A >= B', 'END', 'PRINT A', 'END']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            condition = program._events[2][3:]
            self.assertEqual(output.getvalue(), '5\n')
            self.assertTrue(program.retrieve_value(condition))

    def test_less_than_or_equal_to_in_identifiers(self):
        lines = ['LET A 3', 'LET B 3', 'GOTO 2 IF A <= B', 'END', 'PRINT A', 'END']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            condition = program._events[2][3:]
            self.assertEqual(output.getvalue(), '3\n')
            self.assertTrue(program.retrieve_value(condition))

    def test_equal_to_in_identifiers(self):
        lines = ['LET A 4', 'LET B 4', 'GOTO 2 IF A = B', 'END', 'PRINT A', 'END']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            condition = program._events[2][3:]
            self.assertEqual(output.getvalue(), '4\n')
            self.assertTrue(program.retrieve_value(condition))

    def test_not_equal_to_in_identifiers(self):
        lines = ['LET A 3', 'LET B 4', 'GOTO 2 IF A <> B', 'END', 'PRINT A', 'END']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            condition = program._events[2][3:]
            self.assertEqual(output.getvalue(), '3\n')
            self.assertTrue(program.retrieve_value(condition))

class GoTestsWithFalseComparisonInIdentifiers(unittest.TestCase):
    def test_false_less_than_in_identifiers(self):
        lines = ['LET A 5', 'LET B 4', 'GOTO 2 IF A < B', 'END', 'PRINT A', 'END']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            condition = program._events[2][3:]
            self.assertEqual(output.getvalue(), '')
            self.assertFalse(program.retrieve_value(condition))

    def test_false_greater_than_in_identifiers(self):
        lines = ['LET A 2', 'LET B 4', 'GOTO 2 IF A > B', 'END', 'PRINT A', 'END']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            condition = program._events[2][3:]
            self.assertEqual(output.getvalue(), '')
            self.assertFalse(program.retrieve_value(condition))

    def test_false_greater_than_or_equal_to_in_identifiers(self):
        lines = ['LET A 2', 'LET B 4', 'GOTO 2 IF A >= B', 'END', 'PRINT A', 'END']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            condition = program._events[2][3:]
            self.assertEqual(output.getvalue(), '')
            self.assertFalse(program.retrieve_value(condition))

    def test_false_less_than_or_equal_to_in_identifiers(self):
        lines = ['LET A 4', 'LET B 3', 'GOTO 2 IF A <= B', 'END', 'PRINT A', 'END']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            condition = program._events[2][3:]
            self.assertEqual(output.getvalue(), '')
            self.assertFalse(program.retrieve_value(condition))

    def test_false_equal_to_in_identifiers(self):
        lines = ['LET A 4', 'LET B 3', 'GOTO 2 IF A = B', 'END', 'PRINT A', 'END']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            condition = program._events[2][3:]
            self.assertEqual(output.getvalue(), '')
            self.assertFalse(program.retrieve_value(condition))

    def test_false_not_equal_to_in_identifiers(self):
        lines = ['LET A 3', 'LET B 3', 'GOTO 2 IF A <> B', 'END', 'PRINT A', 'END']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            condition = program._events[2][3:]
            self.assertEqual(output.getvalue(), '')
            self.assertFalse(program.retrieve_value(condition))

class FailedGoTests(unittest.TestCase):
    def test_jumped_past_lines_and_value_is_stored_in_identifier(self):
        lines = ['LET A 3', 'LET B 5', 'GOTO B IF A <> B', 'END', 'PRINT A', 'END']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            try:
                program.process_grin()
                condition = program._events[2][3:]
                self.assertTrue(program.retrieve_value(condition))
            except SystemExit:
                self.assertEqual(output.getvalue(),'ERROR AT LINE 3: TARGET LINE IS OUT OF BOUNDS\n')

    def test_max_recursion_go_statement(self):
        lines = ['PRINT "HI"', 'GOTO -1']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            with self.assertRaises((SystemExit, RecursionError)):
                    program.process_grin()

    def test_goto_int_that_exceeds_bounds(self):
        lines = ['GOTO -100']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            with self.assertRaises((SystemExit, RecursionError)):
                program.process_grin()

if __name__ == '__main__':
    unittest.main()