"""No made-up mathematics survives these tests. The invoices may."""
from contextlib import redirect_stdout
from io import StringIO
import json
import unittest

from cavemath import (
    MAX_RAW, MIN_RAW, SCALE, audit, calculate, checked, format_q, main,
    parse_q, trunc_div,
)


class ExactRockArithmetic(unittest.TestCase):
    def test_constant(self):
        self.assertEqual(SCALE, 65536)

    def test_integer_boundaries(self):
        self.assertEqual(parse_q("-32768"), MIN_RAW)
        self.assertEqual(parse_q("32767.9999847412109375"), MAX_RAW)

    def test_overflow_does_not_wrap(self):
        with self.assertRaises(ValueError):
            parse_q("32768")
        with self.assertRaises(ValueError):
            checked(MAX_RAW + 1)
        with self.assertRaises(ValueError):
            calculate("add", MAX_RAW, 1)

    def test_truncated_fraction_exact(self):
        self.assertEqual(parse_q("0.1"), 6553)
        self.assertEqual(parse_q("-0.1"), -6553)
        self.assertEqual(parse_q("1.1"), 72089)

    def test_no_binary_float_rounding(self):
        self.assertEqual(format_q(6553), "0.0999908447265625")
        self.assertEqual(format_q(-1), "-0.0000152587890625")
        self.assertEqual(format_q(0), "0")
        self.assertEqual(format_q(-65536), "-1")

    def test_reject_nonfinite_and_exponential_input(self):
        for text in ("nan", "NaN", "Infinity", "1e5", "", "1.2.3", "1" * 49):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_q(text)

    def test_add_sub(self):
        self.assertEqual(calculate("add", parse_q("1.5"), parse_q("2.25")), parse_q("3.75"))
        self.assertEqual(calculate("sub", parse_q("1"), parse_q("2")), parse_q("-1"))

    def test_negative_multiply_truncates_toward_zero(self):
        self.assertEqual(trunc_div(-3, 2), -1)
        self.assertEqual(calculate("mul", -1, 32768), 0)
        self.assertEqual(calculate("mul", parse_q("-2"), parse_q("0.5")), -65536)

    def test_divide_uses_widened_integer(self):
        self.assertEqual(calculate("div", parse_q("1"), parse_q("3")), 21845)
        self.assertEqual(calculate("div", parse_q("-1"), parse_q("3")), -21845)

    def test_division_by_zero_rejected(self):
        with self.assertRaisesRegex(ValueError, "division by zero"):
            calculate("div", SCALE, 0)

    def test_overflow_on_division(self):
        with self.assertRaises(ValueError):
            calculate("div", MAX_RAW, 1)

    def test_integer_square_root(self):
        self.assertEqual(calculate("sqrt", parse_q("2")), 92681)
        self.assertEqual(calculate("sqrt", parse_q("4")), 131072)
        self.assertEqual(calculate("sqrt", 0), 0)

    def test_negative_sqrt_rejected(self):
        with self.assertRaises(ValueError):
            calculate("sqrt", -1)

    def test_sqrt_is_unary(self):
        with self.assertRaises(ValueError):
            calculate("sqrt", SCALE, SCALE)

    def test_binary_missing_operand_rejected(self):
        with self.assertRaises(ValueError):
            calculate("mul", SCALE)

    def test_unknown_operation_rejected(self):
        with self.assertRaises(ValueError):
            calculate("claim_math", SCALE, SCALE)


class FictionalRockRoyalty(unittest.TestCase):
    def test_only_standalone_ones_trigger_invoice(self):
        receipt = audit("1 11 16.16 1.0 -1")
        self.assertEqual(receipt["infringements"], 3)
        self.assertEqual(receipt["rock_royalty"], 21)
        self.assertFalse(receipt["legally_enforceable"])

    def test_no_numba_no_invoice(self):
        self.assertEqual(audit("222 and 999")["rock_royalty"], 0)

    def test_claim_is_explicit_parody(self):
        output = StringIO()
        with redirect_stdout(output):
            status = main(["claim"])
        self.assertEqual(status, 0)
        self.assertIn("NO ACTUAL TRADEMARK", output.getvalue())

    def test_json_invoice(self):
        output = StringIO()
        with redirect_stdout(output):
            status = main(["audit", "1 + 1", "--json"])
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(output.getvalue())["rock_royalty"], 14)

    def test_json_calculator(self):
        output = StringIO()
        with redirect_stdout(output):
            status = main(["calc", "mul", "-2", "0.5", "--json"])
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(output.getvalue())["exact_decimal"], "-1")


if __name__ == "__main__":
    unittest.main()
