<div align="center">

# 🪨 CAVEMATH
## U STEAL MY NUMBAS!

### NUMBA 1™ — FIRST NUMBER EVER INVENTED. PROBABLY.

**Me see 1 before you. You use 1. Pay rock royalty.**

**ME INVENT MATH. ME INVENT INVOICE. ME INVENT DENIAL OF APPEAL.**

</div>

---

### 🚨 CAVE PATENT OFFICE: YOU UNDER INVESTIGATION

Somebody wrote \`1\`. Cave Patent Office has opened an imaginary case.
No innocent digits. No independent discovery. No sedimentary refunds.

| Crime against cave | Punishment (fictional) |
| --- | --- |
| Type \`1\` | 7 sedimentary rocks |
| Type \`1 + 1\` | 14 sedimentary rocks |
| Invent mathematics independently | Rock cease-and-desist |
| Perform exact Q16.16 arithmetic | Suspiciously competent |
| Say "I invented Math" | Appointed Chief Numeral Officer |
| Pay igneous rock | REJECTED: TOO VOLCANIC |

**Important:** NUMBA 1™ is a fictional, unregistered parody mark. No patent,
trademark exclusivity, actual royalty, historical authorship claim, or
payment obligation is asserted.

## Rock-powered interactive demo

Open **[index.html](index.html)** locally in a browser. No server, build step,
CDN, npm, tracking, third-party dependency or network access required.

The demo includes a live **NUMBA 1™ detector**, a fictional sedimentary
royalty calculator, a petty rock payment desk, and an actual Q16.16
calculator. Browser computation uses \`BigInt\` for exact authoritative
integer arithmetic, not binary floating-point approximations.

## CLI: CAVE PATENT OFFICE, NOW WITH REAL MATH

Requires Python 3.10+ and the standard library only.

~~~sh
python3 cavemath.py claim
python3 cavemath.py audit "1 + 1" --json
python3 cavemath.py calc add 1.5 2.25
python3 cavemath.py calc mul -2 0.5 --json
python3 cavemath.py calc div 1 3 --json
python3 cavemath.py calc sqrt 2
python3 -m unittest discover -s tests -v
~~~

The CLI supports \`audit --file path.txt\` for UTF-8 files up to 1 MiB.
The audit counts the digit \`1\` only when not adjacent to another digit:
\`11\` is not two standalone \`1\` claims; \`1.0\` is one.

### Cave math contract (the part without bullshit)

- Signed 32-bit Q16.16, **65,536 raw units per 1**.
- Decimal-to-fixed parsing truncates **toward zero**.
- \`add\`, \`sub\`, \`mul\`, \`div\` and \`sqrt\` use integer intermediates.
- Multiply/divide truncate toward zero, including negative results.
- Square root is the integer floor of the exact scaled radicand.
- No signed overflow wraparound, division by zero, NaN, Infinity or
  negative square roots. Invalid input is rejected.
- The browser demo and Python CLI use separately written implementations;
  tests exercise the Python reference. They do **not** constitute a
  formal proof of cross-language parity.

**The math is real. The intellectual-property claim is complete bollocks.**

## Where cave get very bad idea

- **[FP-HIST-001 — You Didn't Invent Doom Edition](https://doi.org/10.5281/zenodo.24049474)**:
  historical evidence for 16.16 fixed-point arithmetic in published DOOM
  source, alongside independently documented VANILLAJS engineering.
- **[QSOLKCB/VANILLAJS](https://github.com/QSOLKCB/VANILLAJS)**:
  source project for independently developed Q16.16 engineering and its
  precisely bounded verification claims.
- **[JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)**:
  inspiration for terse caveman speech; attribution for the
  [actual caveman skill](https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman/SKILL.md).
  No upstream code or assets are incorporated.

CAVEMATH exists to satirize exaggerated claims to ancient or common
mathematical techniques. It is **not** an allegation that any named person
stole code, invented nothing, or made a legally actionable statement.

See [NOTICE-OF-INFRINGEMENT.md](NOTICE-OF-INFRINGEMENT.md) for the
entire fictional prosecution.

## Licence

Apache-2.0 (see [LICENSE](LICENSE)).

**No steal my numbas. No steal my jokes. No pretend real patent.**
