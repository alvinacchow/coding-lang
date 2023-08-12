#test_math.py
#conducts tests with math operations

import unittest
import grin
import contextlib
import io

class AddTests(unittest.TestCase):
    def test_add_integers(self):
        lines = ['LET A 10', 'ADD A 2']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 12)

    def test_add_floats(self):
        lines = ['LET A 1.5', 'ADD A 3.5']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 5.0)

    def test_add_strings(self):
        lines = ['LET A "HELLO"', 'ADD A "WORLD"']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 'HELLOWORLD')

    def test_mix_numerics_for_add(self):
        lines = ['LET A 10', 'ADD A 1.23']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 11.23)

    def test_reflective_mix_numerics_for_add(self):
        lines = ['LET A 1.23', 'ADD A 10']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 11.23)

    def test_add_between_two_variables(self):
        lines = ['LET A 10', 'LET B 20', 'ADD A B']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers(), {'A': 30, 'B': 20})

    def test_add_string_to_defaulted_variable_raises_error(self):
        lines = ['ADD A "HELLO"']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            try:
                program.process_grin()
            except (TypeError, SystemExit):
                pass
            self.assertEqual(output.getvalue(), 'ERROR AT LINE 1: FAILED TO COMPUTE DUE TO INCOMPATIBLE TYPES\n')

    def test_add_to_defaulted_variable(self):
        lines = ['ADD A 10']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 10)

class SubtractTests(unittest.TestCase):
    def test_sub_integers(self):
        lines = ['LET A 10', 'SUB A 2']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 8)

    def test_sub_floats(self):
        lines = ['LET A 1.5', 'SUB A 1.0']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 0.5)

    def test_sub_strings_raises_errors(self):
        lines = ['LET A "HELLO"', 'SUB A "WORLD"']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            try:
                program.process_grin()
            except (TypeError, SystemExit):
                pass
            self.assertEqual(output.getvalue(), 'ERROR AT LINE 2: FAILED TO COMPUTE DUE TO INCOMPATIBLE TYPES\n')

    def test_mix_numerics_for_sub(self):
        lines = ['LET A 10', 'SUB A 1.5']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 8.5)

    def test_reflective_mix_numerics_for_sub(self):
        lines = ['LET A 1.5', 'SUB A 1']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 0.5)

    def test_subtract_between_two_variables(self):
        lines = ['LET A 10', 'LET B 20', 'SUB A B']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers(), {'A': -10, 'B': 20})

    def test_subtract_from_defaulted_variable(self):
        lines = ['SUB A 10']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], -10)

    def test_cannot_subtract_int_from_string(self):
        lines = ['LET A "HELLO"', 'SUB A 10']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            try:
                program.process_grin()
            except (TypeError, SystemExit):
                pass
            self.assertEqual(output.getvalue(),'ERROR AT LINE 2: FAILED TO COMPUTE DUE TO INCOMPATIBLE TYPES\n')

class MultiplyTests(unittest.TestCase):
    def test_mult_integers(self):
        lines = ['LET A 10', 'MULT A 2']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 20)

    def test_mult_floats(self):
        lines = ['LET A 1.5', 'MULT A 2.0']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 3.0)

    def test_mult_strings(self):
        lines = ['LET A "HELLO"', 'MULT A 3']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], "HELLOHELLOHELLO")

    def test_reflexive_mult_strings(self):
        lines = ['LET A 3', 'MULT A "HELLO"']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], "HELLOHELLOHELLO")

    def test_mix_numerics_for_mult(self):
        lines = ['LET A 10', 'MULT A 1.5']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 15.0)

    def test_reflective_mix_numerics_for_mult(self):
        lines = ['LET A 1.5', 'MULT A 10']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 15.0)

    def test_mult_between_two_variables(self):
        lines = ['LET A 10', 'LET B 20', 'MULT A B']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers(), {'A': 200, 'B': 20})

    def test_multiply_defaulted_variable(self):
        lines = ['MULT A 10']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 0)

class DivideTests(unittest.TestCase):
    def test_div_integers(self):
        lines = ['LET A 10', 'DIV A 2']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 5)

    def test_div_integers_with_floor(self):
        lines = ['LET A 7', 'DIV A 2']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 3)

    def test_div_floats(self):
        lines = ['LET A 5.0', 'DIV A 2.0']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 2.5)

    def test_div_strings_raises_error(self):
        lines = ['LET A "HELLO"', 'DIV A 3']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            try:
                program.process_grin()
            except (TypeError, SystemExit):
                pass
            self.assertEqual(output.getvalue(),'ERROR AT LINE 2: FAILED TO COMPUTE DUE TO INCOMPATIBLE TYPES\n')

    def test_mix_numerics_for_div(self):
        lines = ['LET A 10', 'DIV A 2.5']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 4.0)

    def test_reflective_mix_numerics_for_div(self):
        lines = ['LET A 15.0', 'DIV A 10.0']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 1.5)

    def test_div_between_two_int_variables(self):
        lines = ['LET A 10', 'LET B 20', 'DIV A B']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers(), {'A': 0, 'B': 20})

    def test_div_between_two_float_variables(self):
        lines = ['LET A 10.0', 'LET B 20', 'DIV A B']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers(), {'A': 0.5, 'B': 20})

    def test_divide_defaulted_variable(self):
        lines = ['DIV A 10']
        program = grin.State(lines)
        program.process_grin()
        self.assertEqual(program.get_identifiers()['A'], 0)

    def test_cannot_divide_by_zero(self):
        lines = ['LET A 10', 'DIV A 0']
        program = grin.State(lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            try:
                program.process_grin()
            except (TypeError, SystemExit):
                pass
            self.assertEqual(output.getvalue(),'ERROR AT LINE 2: CANNOT DIVIDE BY ZERO\n')

class ConvertTests(unittest.TestCase):
    def test_string_to_float(self):
        self.assertIsNone(grin.to_float('HELLO'))

    def test_string_to_int(self):
        self.assertIsNone(grin.to_int('HELLO'))

    def test_float_string_to_float(self):
        self.assertEqual(grin.to_float('1.23'), 1.23)

    def test_int_string_to_int(self):
        self.assertEqual(grin.to_int('3'), 3)

if __name__ == '__main__':
    unittest.main()
