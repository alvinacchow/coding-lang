#test_full_match.py
#conducts full program tests to match output

import unittest
import contextlib
import io
import grin

class ThorntonFullTestPrograms(unittest.TestCase):
    def test_mixed_integer_goto(self):
        lines = ['LET Z 5', 'GOTO 5', 'LET C 4', 'PRINT C', 'PRINT Z', 'END', 'PRINT C', 'PRINT Z',
                 'GOTO -6']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue(), '0\n5\n4\n5\n')

    def test_positive_goto(self):
        lines = ['LET A 1', 'GOTO 2', 'LET A 2', 'PRINT A']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue(), '1\n')

    def test_labels_goto(self):
        lines = ['LET Z 5', 'GOTO "CZ"', 'CCZ: LET C 4', 'PRINT C', 'PRINT Z', 'END', 'CZ: PRINT C',
                'PRINT Z', 'GOTO "CCZ"']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue(), '0\n5\n4\n5\n')

    def test_nested_labels_goto(self):
        lines = ['LET Z 1', 'LET C 11', 'LET F 4', 'LET B "ZC"', 'GOTO F', 'ZC: PRINT Z', 'PRINT C',
                 'END', 'CZ: PRINT C', 'PRINT Z', 'GOTO B']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue(), '11\n1\n1\n11\n')

    def test_goto_with_true_conditional(self):
        lines = ['LET A 3', 'LET B 5', 'GOTO 2 IF A < 4', 'PRINT A', 'PRINT B']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue(), '5\n')

    def test_goto_with_false_conditional(self):
        lines = ['LET A 3', 'LET B 5', 'GOTO 2 IF A > 4', 'PRINT A', 'PRINT B']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue(), '3\n5\n')

    def test_gosub_with_mixed_integers(self):
        lines = ['LET A 1', 'GOSUB 5', 'PRINT A', 'END', 'LET A 3', 'RETURN', 'PRINT A', 'LET A 2',
                 'GOSUB -4', 'PRINT A', 'RETURN']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue(), '1\n3\n3\n')

    def test_single_positive_gosub_statement(self):
        lines = ['LET A 1', 'GOSUB 4', 'PRINT A', 'PRINT B', 'END', 'LET A 2', 'LET B 3', 'RETURN']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue(), '2\n3\n')

    def test_repetitive_gosub_statement(self):
        lines = ['LET A 3', 'GOSUB "PRINTABC"', 'LET B 4', 'GOSUB "PRINTABC"', 'LET C 5',
                 'GOSUB "PRINTABC"', 'LET A 1', 'GOSUB "PRINTABC"', 'END', 'PRINTABC: PRINT A',
                 'PRINT B', 'PRINT C', 'RETURN']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue(), '3\n0\n0\n3\n4\n0\n3\n4\n5\n1\n4\n5\n')

class MoreFullMathTests(unittest.TestCase):
    def test_match_output_one(self):
        lines = ['LET A 10', 'LET B 4', 'PRINT A', 'ADD A B', 'PRINT A']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue(), '10\n14\n')

    def test_match_output_two(self):
        lines = ['LET A 2', 'GOTO 2', 'LET A 3', 'LET A 4', 'PRINT A']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue(), '4\n')

    def test_match_output_three(self):
        lines = ['       LET        A    10','     PRINT        A  ',
                 '  GOSUB    "STRAWBERRY"     ','PRINT    A','PRINT   B    ',
                 '     GOTO         "BANANA"','    STRAWBERRY:  LET    A 12',
                 '   LET B     3', 'RETURN     ','   BANANA: PRINT    A  '
                 ]
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue(), '10\n12\n3\n12\n')

    def test_match_output_four(self):
        lines = ['GOSUB "APPLE"', 'PRINT "!"','END','APPLE: PRINT "HELLO"', 'PRINT "WORLD"', 'RETURN']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue(), 'HELLO\nWORLD\n!\n')


    def test_match_output_five(self):
        lines = ['LET NAME "NAME"', 'LET AGE 12',
                 'PRINT NAME','PRINT AGE']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue(), 'NAME\n12\n')

    def test_match_output_six(self):
        lines = ['LET C 20', 'GOTO 2', 'LET C 30', 'PRINT C']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue(), '20\n')

    def test_match_output_seven(self):
        lines = ['LET A 10','LET B A', 'SUB A 6', 'MULT A B','PRINT A',
                 'DIV A 10','LET C "C"', 'MULT C A','PRINT C']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue(), '40\nCCCC\n')

    def test_match_output_eight(self):
        lines = ['LET A "STRAW"', 'GOSUB 4', 'MULT A 2', 'PRINT A','END',
                  'PRINT A','ADD A "BERRY"', 'RETURN']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue(), 'STRAW\nSTRAWBERRYSTRAWBERRY\n')

    def test_output_nine(self):
        lines = ['LET A "HI"', 'GOTO 2 IF A = "HI"', 'LET A "BYE"', 'PRINT A']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            program.process_grin()
            self.assertEqual(output.getvalue(), 'HI\n')

if __name__ == '__main__':
    unittest.main()
