"""Simple line numbering and function parsing utilities."""

import ast
import os
import tokenize
import io


def line_number(input_filename: str, output_filename: str) -> None:
    """Read input_filename and write it to output_filename with each
    line prefixed by its line number (starting at 1)."""
    try:
        with open(input_filename, "r") as infile:
            lines = infile.readlines()

        with open(output_filename, "w") as outfile:
            for i, line in enumerate(lines, start=1):
                outfile.write(f"{i}. {line}")

    except Exception as error:
        print(f"Error while numbering lines: {error}")
        raise


def _remove_comments_and_blanks(code: str) -> str:
    """Remove comment text and blank lines from a piece of Python code.
    Uses tokenize so a '#' inside a string is not treated as a comment."""
    lines = code.splitlines()
    comment_cols = {}
    for tok in tokenize.generate_tokens(io.StringIO(code).readline):
        if tok.type == tokenize.COMMENT:
            comment_cols[tok.start[0]] = tok.start[1]

    result = []
    for i, line in enumerate(lines, start=1):
        if i in comment_cols:
            line = line[: comment_cols[i]]
        if line.strip() != "":
            result.append(line)

    return "\n".join(result) + "\n"


def parse_functions(filename: str) -> tuple:
    """Parse a .py file and return a tuple of tuples, one per top-level
    function: (line_number, name, args, code). code has blank lines and
    comments removed. The result is sorted alphabetically by name."""
    try:
        with open(filename, "r") as f:
            source = f.read()

        lines = source.splitlines()
        tree = ast.parse(source)

        functions = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                name = node.name
                args = ", ".join(arg.arg for arg in node.args.args)

                # grab the raw code lines for this function
                raw_lines = lines[node.lineno - 1 : node.end_lineno]
                raw_code = "\n".join(raw_lines) + "\n"

                code = _remove_comments_and_blanks(raw_code)
                functions.append((node.lineno, name, args, code))

        functions.sort(key=lambda item: item[1])
        return tuple(functions)

    except Exception as error:
        print(f"Error while parsing functions: {error}")
        raise


def main() -> None:
    """Demo line_number and parse_functions on this file itself."""
    print("FAU ID: Z23692334")

    this_file = os.path.abspath(__file__)
    output_file = this_file + ".numbered.txt"

    line_number(this_file, output_file)
    print(f"Wrote numbered file to {output_file}")

    functions = parse_functions(this_file)
    print("\nFunctions found:")
    for line_no, name, args, code in functions:
        print("-" * 50)
        print(f"line: {line_no}  name: {name}  args: {args}")
        print(code)


if __name__ == "__main__":
    main()
