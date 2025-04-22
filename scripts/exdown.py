# ----
# Code coppied/modified from https://github.com/koaning/exdown
# ----


def extract(
    filename: str, max_num_lines: int = 10000, syntax_filter: str | None = None
) -> list[tuple[str, int]]:
    out = []
    previous_line = None
    k = 1

    with open(filename, "r", encoding="UTF-8") as f:
        while True:
            line = f.readline()
            k += 1
            if not line:
                # EOF
                break

            if line.lstrip()[:3] == "```":
                syntax = line.lstrip()[3:]
                num_leading_spaces = len(line) - len(line.lstrip())
                lineno = k - 1
                # read the block
                code_block = []
                while True:
                    line = f.readline()
                    k += 1
                    if not line:
                        raise RuntimeError("Hit end-of-file prematurely. Syntax error?")
                    if k > max_num_lines:
                        raise RuntimeError(
                            f"File too large (> {max_num_lines} lines). Set max_num_lines."
                        )
                    # check if end of block
                    if line.lstrip()[:3] == "```":
                        break
                    # Cut (at most) num_leading_spaces leading spaces
                    nls = min(num_leading_spaces, len(line) - len(line.lstrip()))
                    line = line[nls:]
                    code_block.append(line)

                if syntax_filter and syntax_filter.strip() != syntax.strip():
                    continue
                if (
                    previous_line is not None
                    and previous_line.strip() == "<!--exdown-skip-->"
                ):
                    continue

                out.append(("".join(code_block), lineno))

            previous_line = line

        return out
