#!/usr/bin/env python3
"""CAVEMATH: a very serious fictional NUMBA 1(TM) infringement office.

All royalty and trademark language is parody. Q16.16 arithmetic is real:
signed 32-bit raw values, exact integer intermediates, truncation toward zero,
and explicit overflow rejection. No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
from math import isqrt
from pathlib import Path
import re
import sys

SCALE = 1 << 16
MIN_RAW = -(1 << 31)
MAX_RAW = (1 << 31) - 1
ROCKS_PER_ONE = 7  # This rate was determined by hitting a rock with another rock.
MAX_AUDIT_BYTES = 1024 * 1024
_DECIMAL = re.compile(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)\Z")
_THE_STOLEN_NUMBER = re.compile(r"(?<!\d)1(?!\d)")


def checked(raw: int) -> int:
    """Reject a result that cannot be stored as signed Q16.16."""
    if raw < MIN_RAW or raw > MAX_RAW:
        raise ValueError("number escaped 32-bit cave; overflow rejected")
    return raw


def parse_q(text: str) -> int:
    """Parse a decimal string as Q16.16, truncating toward zero exactly."""
    if len(text) > 48 or not _DECIMAL.fullmatch(text):
        raise ValueError("expected finite decimal, at most 48 characters")
    negative = text.startswith("-")
    unsigned = text.lstrip("+-")
    whole, dot, fraction = unsigned.partition(".")
    raw = int(whole or "0") * SCALE
    if dot and fraction:
        raw += int(fraction) * SCALE // (10 ** len(fraction))
    return checked(-raw if negative else raw)


def format_q(raw: int) -> str:
    """Render every representable Q16.16 number as its exact decimal."""
    checked(raw)
    # 1 / 2^16 == 5^16 / 10^16, so no float or decimal rounding.
    units = abs(raw) * (5 ** 16)
    integer, fraction = divmod(units, 10 ** 16)
    tail = f"{fraction:016d}".rstrip("0")
    result = str(integer) + ("." + tail if tail else "")
    return "-" + result if raw < 0 else result


def trunc_div(numerator: int, denominator: int) -> int:
    """Integer division toward zero, unlike Python's negative floor division."""
    if denominator == 0:
        raise ValueError("division by zero: zero has no rocks")
    sign = -1 if (numerator < 0) != (denominator < 0) else 1
    return sign * (abs(numerator) // abs(denominator))


def calculate(operation: str, left: int, right: int | None = None) -> int:
    """Execute checked Q16.16 operations, with widened integer intermediates."""
    checked(left)
    if operation == "sqrt":
        if right is not None:
            raise ValueError("sqrt accepts exactly one operand")
        if left < 0:
            raise ValueError("negative square root: cave has no imaginary rocks")
        return checked(isqrt(left * SCALE))
    if right is None:
        raise ValueError("binary operation requires two operands")
    checked(right)
    if operation == "add":
        return checked(left + right)
    if operation == "sub":
        return checked(left - right)
    if operation == "mul":
        return checked(trunc_div(left * right, SCALE))
    if operation == "div":
        return checked(trunc_div(left * SCALE, right))
    raise ValueError("unknown cave operation: " + operation)


def audit(text: str) -> dict[str, int | str | bool]:
    """Count standalone digit 1 appearances; issue a *fictional* rock invoice."""
    count = len(_THE_STOLEN_NUMBER.findall(text))
    return {
        "office": "CAVE PATENT OFFICE (PARODY)",
        "claimed_mark": "NUMBA 1(TM) (NOT REGISTERED)",
        "infringements": count,
        "rock_royalty": count * ROCKS_PER_ONE,
        "rock_type": "sedimentary",
        "legally_enforceable": False,
    }


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="U STEAL MY NUMBAS. Satirical patent office; real Q16.16 math."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("claim", help="read the completely fictional NUMBA 1 claim")
    scan = commands.add_parser("audit", help="inspect text for stolen digit 1")
    scan.add_argument("text", nargs="?", help="text to scan (or use --file)")
    scan.add_argument("--file", type=Path, help="UTF-8 file to scan; maximum 1 MiB")
    scan.add_argument("--json", action="store_true", help="machine-readable invoice")
    calc = commands.add_parser("calc", help="real signed Q16.16 fixed-point arithmetic")
    calc.add_argument("operation", choices=("add", "sub", "mul", "div", "sqrt"))
    calc.add_argument("left", help="decimal operand")
    calc.add_argument("right", nargs="?", help="second operand, except sqrt")
    calc.add_argument("--json", action="store_true", help="machine-readable result")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = make_parser().parse_args(argv)
    try:
        if args.command == "claim":
            print(
                "CAVE PATENT OFFICE -- TOTALLY FICTIONAL NOTICE\n"
                "NUMBA 1(TM): Me see 1 before you. You use 1. Pay rock royalty.\n"
                "Me invent Math. Me invent invoice. Me invent interest on invoice.\n"
                "Sedimentary accepted. Igneous rejected. Metamorphic under review.\n"
                "NO ACTUAL TRADEMARK, PATENT, OR PAYMENT OBLIGATION EXISTS."
            )
            return 0
        if args.command == "audit":
            if (args.text is None) == (args.file is None):
                raise ValueError("provide exactly one of text or --file")
            if args.file is not None:
                if args.file.stat().st_size > MAX_AUDIT_BYTES:
                    raise ValueError("file too large for cave (1 MiB limit)")
                source = args.file.read_text(encoding="utf-8")
            else:
                source = args.text
            report = audit(source)
            if args.json:
                print(json.dumps(report, sort_keys=True))
            else:
                print(
                    f"NUMBA 1(TM) DETECTED: {report['infringements']} alleged offences. "
                    f"PAY {report['rock_royalty']} sedimentary rocks. (PARODY ONLY)"
                )
            return 0
        left = parse_q(args.left)
        right = parse_q(args.right) if args.right is not None else None
        raw = calculate(args.operation, left, right)
        result = {
            "operation": args.operation,
            "raw_q16_16": raw,
            "exact_decimal": format_q(raw),
            "scale": SCALE,
        }
        if args.json:
            print(json.dumps(result, sort_keys=True))
        else:
            print(
                f"REAL CAVE MATH: {result['exact_decimal']} "
                f"(raw {raw}, scale {SCALE}). NO ROCKS WERE HARMED."
            )
        return 0
    except (ValueError, OSError, UnicodeError) as error:
        print("CAVE ERROR: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
