# Quiz File Format Specification

This document describes the format for quiz text files used by autoquiz-tg-userbot.

## File Structure

Each quiz file must be a plain text file (`.txt`) with UTF-8 encoding.

### Format Overview

```
Line 1: Quiz Name
Line 2: Quiz Description
Line 3: Question 1
Line 4: Answer 1 for Question 1
Line 5: Answer 2 for Question 1
Line 6: Answer 3 for Question 1
Line 7: Answer 4 for Question 1
Line 8: Correct answer for Question 1 (duplicate of one of lines 4-7)
Line 9: Question 2
Line 10: Answer 1 for Question 2
...
(Pattern repeats for all 20 questions)
```

## Structure Rules

1. **Line 1**: The name/title of the quiz
2. **Line 2**: A description of the quiz
3. **Lines 3+**: Questions and answers in repeating blocks

## Question Block Format

Each question block consists of exactly **6 lines**:
1. Question text
2. Answer option 1
3. Answer option 2
4. Answer option 3
5. Answer option 4
6. Correct answer (must be an exact duplicate of one of the 4 answer options above)

## Requirements

- **Total questions**: 20 (as specified)
- **Answers per question**: Exactly 4
- **Correct answer format**: Must be an exact text match of one of the 4 answer options
- **Empty lines**: Should be avoided or will be ignored
- **Encoding**: UTF-8

## Example

```
Python Programming Basics
Test your knowledge of Python fundamentals
What is the output of print(2 ** 3)?
6
8
9
16
8
What keyword is used to define a function in Python?
def
function
func
define
def
```

In this example:
- Quiz name: "Python Programming Basics"
- Description: "Test your knowledge of Python fundamentals"
- First question: "What is the output of print(2 ** 3)?"
  - Options: 6, 8, 9, 16
  - Correct answer: 8 (line 8 duplicates line 5)
- Second question: "What keyword is used to define a function in Python?"
  - Options: def, function, func, define
  - Correct answer: def (line 14 duplicates line 10)

## Tips for Creating Quiz Files

1. **Verify correct answers**: Make sure the duplicate line exactly matches one of the answer options
2. **No extra whitespace**: Avoid trailing spaces or tabs
3. **Consistent formatting**: Keep answer options concise and clear
4. **Question clarity**: Make questions unambiguous
5. **Test your file**: Use `test_parser.py` to validate your quiz file before running the bot

## Common Mistakes to Avoid

❌ **Incorrect**: Correct answer doesn't match any option
```
What is 2 + 2?
3
4
5
6
four  ← Wrong! Should be "4"
```

✅ **Correct**: Exact match
```
What is 2 + 2?
3
4
5
6
4
```

❌ **Incorrect**: Wrong number of answers
```
What is 2 + 2?
3
4
5
4  ← Only 3 options provided, needs 4
```

✅ **Correct**: Exactly 4 options
```
What is 2 + 2?
3
4
5
6
4
```

## Validation

Run the test script to validate your quiz files:

```bash
python test_parser.py
```

This will check:
- File can be parsed
- Correct number of questions
- Each question has exactly 4 answers
- Correct answer matches one of the options
