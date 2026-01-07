# Quick Start Guide

## Prerequisites

1. Python 3.7+ installed
2. Telegram account
3. Access to https://my.telegram.org/apps

## Step-by-Step Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Telegram API Credentials

1. Go to https://my.telegram.org/apps
2. Log in with your phone number
3. Click "Create new application"
4. Fill in the form (app title and short name)
5. Copy your `API_ID` and `API_HASH`

### 3. Configure the Bot

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
API_ID=12345678
API_HASH=your_api_hash_here
PHONE_NUMBER=+1234567890
QUIZZES_FOLDER=./quizzes
```

**Important**: Use international format for phone number (include + and country code)

### 4. Create Your Quiz Files

Create `.txt` files in the `quizzes/` folder. Each file should follow this format:

```
Quiz Title
Quiz Description
Question 1?
Option A
Option B
Option C
Option D
Option B
Question 2?
Option W
Option X
Option Y
Option Z
Option Z
... (repeat for 20 questions total)
```

**Format Rules:**
- Line 1: Quiz name
- Line 2: Quiz description  
- Then 20 question blocks, each with:
  - Question text
  - 4 answer options
  - Correct answer (exact copy of one option)

See `quizzes/example_python_basics.txt` for a complete example.

### 5. Validate Your Quiz Files (Optional but Recommended)

Before running the bot, test your quiz files:

```bash
python test_parser.py
```

This will check for:
- File format errors
- Missing or incorrect answers
- Correct answer validation

### 6. Run the Bot

```bash
python main.py
```

**First Run:**
- You'll be prompted to enter a confirmation code
- Check your Telegram for the code (sent by Telegram)
- Enter the code in the terminal
- A session file will be created for future runs

**Subsequent Runs:**
- The bot will use the saved session
- No code entry needed

### 7. Monitor the Process

The bot will:
1. List all found quiz files
2. Parse each file
3. Connect to Telegram
4. Create quizzes in @QuizBot one by one
5. Display progress for each question

Example output:
```
Looking for quiz files in: ./quizzes
Found 1 quiz file(s):
  - example_python_basics.txt

Parsing example_python_basics.txt...
  ✓ Parsed: Python Programming Basics (20 questions)

Starting Telegram client...
✓ Connected to Telegram

============================================================
Creating quiz: Python Programming Basics
Description: Test your knowledge of Python fundamentals
Questions: 20
============================================================

Starting conversation with @QuizBot...
Sending /newquiz command...
Sending quiz name: Python Programming Basics

Question 1/20: What is the output of print(2 ** 3)?...
  Answer 1: 6
  Answer 2: 8 ✓ (correct)
  Answer 3: 9
  Answer 4: 16
...
```

## Troubleshooting

### "Error: API_ID and API_HASH must be set"
- Make sure `.env` file exists in the project root
- Check that values are not empty
- Don't use quotes around values in `.env`

### "No .txt files found"
- Check the `QUIZZES_FOLDER` path in `.env`
- Make sure quiz files have `.txt` extension
- Verify files are in the correct folder

### Authentication Fails
- Delete `autoquiz_session.session` file
- Run the bot again
- Make sure phone number includes country code (e.g., +1)

### Telegram Flood Wait
- If you see "Too many requests", wait a few minutes
- Reduce the number of quizzes processed at once
- Increase delays in `main.py` if needed

### Quiz Not Created Correctly
- The @QuizBot protocol may differ from assumptions
- Monitor the conversation in Telegram
- Adjust commands in `main.py` if needed
- Report the issue with details

## Tips for Success

1. **Test with one quiz first**: Start with a single quiz file to verify everything works
2. **Use the example**: Copy and modify `example_python_basics.txt`
3. **Validate format**: Always run `test_parser.py` before running the bot
4. **Back up your work**: Keep copies of your quiz files
5. **Monitor Telegram**: Watch the conversation with @QuizBot to catch issues

## Example Quiz Files

### Minimal Quiz (20 questions required)

```
Math Basics
Simple arithmetic questions
What is 2 + 2?
3
4
5
6
4
What is 10 - 3?
5
6
7
8
7
... (continue for 18 more questions)
```

### Using the Parser Programmatically

```python
from quiz_parser import parse_quiz_file

# Parse a quiz file
quiz = parse_quiz_file('quizzes/my_quiz.txt')

# Access quiz data
print(f"Name: {quiz.name}")
print(f"Description: {quiz.description}")
print(f"Questions: {len(quiz.questions)}")

# Iterate through questions
for i, q in enumerate(quiz.questions, 1):
    print(f"\nQuestion {i}: {q.question}")
    print(f"Answers: {q.answers}")
    print(f"Correct: {q.correct_answer}")
```

## Advanced Usage

### Custom Quiz Folder

Set a different folder in `.env`:
```env
QUIZZES_FOLDER=/path/to/my/quizzes
```

### Processing Specific Files

Edit `main.py` to filter specific quiz files or implement your own selection logic.

### Adjusting Delays

If you experience rate limiting, increase delays in `main.py`:
```python
await asyncio.sleep(3)  # Instead of 2
```

### Batch Processing

The bot automatically processes all `.txt` files in the quizzes folder. Create multiple quiz files and run once to process all.

## Getting Help

- Check `README.md` for detailed information
- Review `QUIZ_FORMAT.md` for format specification
- See `IMPLEMENTATION.md` for technical details
- Validate files with `test_parser.py`
- Check Telegram conversation for @QuizBot responses

## Next Steps

1. Create your first quiz file
2. Validate it with `test_parser.py`
3. Run `python main.py`
4. Check @QuizBot in Telegram for your quiz
5. Share the quiz with your audience!

Happy quiz creating! 🎯
