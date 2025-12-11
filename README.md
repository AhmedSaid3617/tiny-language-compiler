# TINY Language Parser

A recursive descent parser for the TINY programming language with GUI visualization of Abstract Syntax Trees (AST).

## Overview

This project implements a complete parser for the TINY language following the grammar rules specified in the project requirements. It includes:

- **Token File Parser**: Reads formatted token files
- **Recursive Descent Parser**: Implements TINY grammar with EBNF conversion
- **AST Visualization**: Graphical display of syntax trees using Tkinter
- **GUI Application**: Simple interface for loading files and viewing results

## Features

✓ Parses all TINY language constructs:
  - if-statements (with optional else)
  - repeat-statements
  - assign-statements
  - read-statements
  - write-statements
  - Expressions with correct operator precedence

✓ Displays syntax tree graphically:
  - Rectangles for statements
  - Ovals for expressions and operators
  - Proper tree layout with parent-child connections

✓ Error handling:
  - Syntax error detection
  - Clear error messages with position information

## Installation

1. **Clone or download the repository**

2. **Ensure Python 3.7+ is installed**
   ```bash
   python --version
   ```

3. **No external dependencies required** (uses built-in Tkinter)

## Usage

### Running the GUI Application

```bash
python main.py
```

This will launch the GUI where you can:
1. Click "Load Token File" button
2. Select a token file (e.g., `input_sample.txt`)
3. View the generated syntax tree
4. See success/error status

### Token File Format

The parser expects token files in this format:

```
TINY Language Scanner Output
=============================

Token Value         Token Type          
----------------------------------------
read                READ                
x                   IDENTIFIER          
;                   SEMICOLON           
...
```

See `input_sample.txt` for a complete example.

### Running Tests

Run the integration tests:
```bash
python test/integration_test.py
```

Run existing unit tests:
```bash
pytest
```

## Project Structure

```
code/
├── main.py                      # Application entry point
├── input_sample.txt             # Sample token file (factorial program)
├── src/
│   ├── parse/
│   │   ├── parser.py            # Recursive descent parser
│   │   ├── syntax_tree.py       # AST node definitions
│   │   ├── token_stream.py      # Token types and stream
│   │   └── token_file_parser.py # Token file reader
│   ├── gui/
│   │   ├── main_window.py       # Main GUI window
│   │   └── tree_visualizer.py   # AST visualization
│   └── tinyerror/
│       └── tiny_error.py        # Error handling
└── test/
    ├── parser_test.py           # Parser unit tests
    ├── syntax_tree_test.py      # AST node tests
    └── integration_test.py      # Integration tests
```

## Grammar Rules

The parser implements these TINY language grammar rules:

1. `program → stmt-sequence`
2. `stmt-sequence → statement { ; statement }`
3. `statement → if-stmt | repeat-stmt | assign-stmt | read-stmt | write-stmt`
4. `if-stmt → if exp then stmt-sequence [else stmt-sequence] end`
5. `repeat-stmt → repeat stmt-sequence until exp`
6. `assign-stmt → identifier := exp`
7. `read-stmt → read identifier`
8. `write-stmt → write exp`
9. `exp → simple-exp [comparison-op simple-exp]`
10. `comparison-op → < | = | >`
11. `simple-exp → term { addop term }`
12. `addop → + | -`
13. `term → factor { mulop factor }`
14. `mulop → * | /`
15. `factor → (exp) | number | identifier`

Note: Left-recursive rules (2, 11, 13) have been converted to EBNF form using repetition `{ }`.

## Operator Precedence

- **Lowest**: Comparison operators (`<`, `=`, `>`)
- **Medium**: Addition/Subtraction (`+`, `-`)
- **Highest**: Multiplication/Division (`*`, `/`)

## Example

The included `input_sample.txt` contains tokens for this factorial program:

```
read x;
if 0 < x then
    fact := 1;
    repeat
        fact := fact * x;
        x := x - 1
    until x = 0;
    write fact
end
```

When parsed and visualized, it produces a syntax tree showing:
- Root: statement sequence (read, if)
- If statement with comparison test
- Then-part with assign, repeat, and write statements
- Repeat body with two assignments
- Expression trees showing operator precedence

## Implementation Notes

### Parser Design
- **Recursive Descent**: Each grammar rule has a corresponding parsing method
- **EBNF Conversion**: Left-recursive rules converted to iterative form
- **Error Recovery**: TinyError exceptions with position information

### Visualization
- **Layout Algorithm**: Recursive positioning with horizontal spacing
- **Node Types**: Different shapes for statements vs expressions
- **Scrollable Canvas**: Handles large syntax trees

### Token Types
Token types match the input file format:
- Keywords: `READ`, `WRITE`, `IF`, `THEN`, `ELSE`, `END`, `REPEAT`, `UNTIL`
- Operators: `ASSIGN`, `PLUS`, `MINUS`, `MULT`, `DIV`, `LESSTHAN`, `EQUAL`, `GREATERTHAN`
- Literals: `IDENTIFIER`, `NUMBER`
- Punctuation: `SEMICOLON`, `LPAREN`, `RPAREN`

## Testing

The project includes comprehensive tests:

1. **Unit Tests**: Test individual parser methods and AST nodes
2. **Integration Tests**: Test complete parsing pipeline
3. **Sample Input**: Factorial program demonstrates all language features

All tests verify:
- Correct AST structure
- Proper operator precedence
- Error detection for invalid syntax
- Token file parsing accuracy

## License

Educational project for compiler construction course.

## Authors

Developed for the TINY Language Parser project.
