# autoquiz-tg-userbot

Given the text files with test questions and answers (with right answer marked), this tool uses your Telegram account to create quizzes in @QuizBot.

## Features

- 📝 Parse quiz files from a folder
- 🤖 Automatically create quizzes in Telegram @QuizBot
- 🔄 Process multiple quiz files in batch
- ✅ Support for 20 questions per quiz as specified
- 🎯 Mark correct answers automatically

## Requirements

- Python 3.7 or higher
- Telegram account
- Telegram API credentials (API_ID and API_HASH)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/DragonsCode/autoquiz-tg-userbot.git
cd autoquiz-tg-userbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Get your Telegram API credentials:
   - Go to https://my.telegram.org/apps
   - Log in with your phone number
   - Create a new application
   - Copy your `API_ID` and `API_HASH`

4. Configure the application:
```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:
```
API_ID=your_api_id
API_HASH=your_api_hash
PHONE_NUMBER=+1234567890
QUIZZES_FOLDER=./quizzes
```

## Quiz File Format

Create `.txt` files in the `quizzes` folder with the following format:

```
Quiz Name
Quiz Description
Question 1 text
A) Answer option A
B) Answer option B
C) Answer option C
D) Answer option D

B) Answer option B

Question 2 text
A) Answer W
B) Answer X
C) Answer Y
D) Answer Z

D) Answer Z

...
```

**Format Rules:**
- **Line 1**: Quiz name
- **Line 2**: Quiz description  
- **Lines 3+**: Questions and answers
  - Question text (without A/B/C/D prefix)
  - 4 answer options starting with `A)`, `B)`, `C)`, `D)`
  - Blank line
  - Correct answer (full text including the letter prefix, e.g., `B) Answer option B`)
  - Blank line before next question

**Example:** See `quizzes/swt1.txt` and `quizzes/swt2.txt`

## Usage

1. Create your quiz files in the `quizzes` folder (or specify a different folder in `.env`)

2. Run the bot:
```bash
python main.py
```

3. On first run, you'll be asked to enter the confirmation code sent to your Telegram account

4. The bot will:
   - Parse all `.txt` files in the quizzes folder
   - Connect to Telegram using your account
   - Create each quiz in @QuizBot automatically
   - Save all quiz links to your Saved Messages when done

## Project Structure

```
autoquiz-tg-userbot/
├── main.py              # Main bot script
├── quiz_parser.py       # Quiz file parser
├── requirements.txt     # Python dependencies
├── .env.example        # Example environment configuration
├── .env                # Your configuration (not in git)
├── quizzes/            # Folder for quiz files
│   └── example_python_basics.txt
└── README.md           # This file
```

## Dependencies

- **Kurigram**: A fork of Pyrogram for Telegram automation ([docs](https://docs.kurigram.icu/))
- **python-dotenv**: For environment variable management

## Notes

- Each quiz should contain 20 questions as per the specification
- The bot adds delays between messages to avoid rate limiting
- Session data is stored in `autoquiz_session.session` file
- Make sure your Telegram account has access to @QuizBot

## Troubleshooting

**"Error: API_ID and API_HASH must be set"**
- Make sure you've created a `.env` file with your credentials

**"No .txt files found"**
- Check that your quiz files are in the correct folder
- Verify the `QUIZZES_FOLDER` path in `.env`

**Authentication issues**
- Delete the `autoquiz_session.session` file and try again
- Make sure your phone number is in international format (+1234567890)

**Quiz creation issues**
- The bot interaction with @QuizBot uses polls with the QUIZ type
- Questions are sent as text messages, then answers as a poll with the correct answer marked
- Monitor the Telegram conversation to see what @QuizBot expects
- The flow is: /cancel → /newquiz → name → description → [question text + poll] × N → /done → time limit → shuffle option

## Important Notes

⚠️ **@QuizBot Protocol**: The implementation sends quiz questions as Telegram polls with the QUIZ type, which allows marking the correct answer. After all questions are added, the bot sets a 15-second time limit and enables shuffling of questions and answers. All created quiz links are automatically saved to your Saved Messages.

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
