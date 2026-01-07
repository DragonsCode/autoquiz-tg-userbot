"""
AutoQuiz Telegram Userbot
Creates quizzes in @QuizBot from text files.
"""
import os
import random
import re
import sys
import asyncio
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.enums import PollType
from quiz_parser import find_quiz_files, parse_quiz_file


# Configuration
BOT_USERNAME = "QuizBot"
TIME_LIMIT = "15 сек"
SHUFFLE_OPTION = "Перемешать все"
MESSAGE_DELAY = 2.5  # Delay between messages in seconds
POLL_DELAY = 3.0     # Delay after sending a poll


async def wait_for_bot_response(client: Client, timeout: float = 10.0) -> str:
    """
    Wait for a response from QuizBot and return the last message text.
    """
    await asyncio.sleep(MESSAGE_DELAY)
    async for message in client.get_chat_history(BOT_USERNAME, limit=1):
        if message.from_user and message.from_user.username == BOT_USERNAME:
            return message.text or ""
    return ""


async def create_quiz_in_bot(client: Client, quiz) -> str | None:
    """
    Create a quiz in @QuizBot using the provided quiz data.
    
    Args:
        client: Kurigram Client instance
        quiz: Quiz object containing quiz data
        
    Returns:
        Quiz link if successful, None otherwise
    """
    try:
        print(f"\n{'='*60}")
        print(f"Creating quiz: {quiz.name}")
        print(f"Description: {quiz.description}")
        print(f"Questions: {len(quiz.questions)}")
        print(f"{'='*60}\n")
        
        # Cancel any existing quiz creation
        print("Cancelling any previous quiz creation...")
        await client.send_message(BOT_USERNAME, "/cancel")
        await asyncio.sleep(MESSAGE_DELAY)
        
        # Send /newquiz command to create a new quiz
        print("Sending /newquiz command...")
        await client.send_message(BOT_USERNAME, "/newquiz")
        await asyncio.sleep(MESSAGE_DELAY)
        
        # Send quiz name
        print(f"Sending quiz name: {quiz.name}")
        await client.send_message(BOT_USERNAME, quiz.name)
        await asyncio.sleep(MESSAGE_DELAY)
        
        # Send quiz description
        print(f"Sending description: {quiz.description}")
        await client.send_message(BOT_USERNAME, quiz.description)
        await asyncio.sleep(MESSAGE_DELAY)
        
        # Send each question as a poll
        for idx, question in enumerate(quiz.questions, 1):
            print(f"\nQuestion {idx}/{len(quiz.questions)}: {question.question[:60]}...")
            
            # Shuffle answers to randomize correct answer position
            # (Original files often have the same letter as correct answer)
            answers_with_indices = list(enumerate(question.answers))  # [(0, 'A) ...'), (1, 'B) ...'), ...]
            random.shuffle(answers_with_indices)
            
            # Find the new position of the correct answer after shuffling
            correct_option_id = 0
            shuffled_answers = []
            letters = ['A', 'B', 'C', 'D']
            for new_idx, (orig_idx, answer) in enumerate(answers_with_indices):
                # Replace original letter with new letter
                new_answer = letters[new_idx] + ')' + answer[2:]  # Replace 'X)' with new letter
                shuffled_answers.append(new_answer)
                if answer == question.correct_answer:
                    correct_option_id = new_idx
            
            # Combine question text with shuffled answer options into one message
            # (Poll options are limited to 100 chars, so we put full answers in the message)
            question_with_answers = question.question + "\n" + "\n".join(shuffled_answers)
            await client.send_message(BOT_USERNAME, question_with_answers)
            await asyncio.sleep(MESSAGE_DELAY)
            
            # Use just letters as poll options (A, B, C, D)
            poll_options = ["A", "B", "C", "D"]
            correct_letter = poll_options[correct_option_id]
            print(f"  Sending poll with options A/B/C/D, correct: {correct_letter}")
            
            # Send poll with quiz type (correct answer marked)
            await client.send_poll(
                chat_id=BOT_USERNAME,
                question="Ответ",  # Poll question (QuizBot uses this)
                options=poll_options,
                type=PollType.QUIZ,
                correct_option_id=correct_option_id,
                is_anonymous=False
            )
            await asyncio.sleep(POLL_DELAY)
            
        # Finish quiz creation
        print("\nSending /done command...")
        await client.send_message(BOT_USERNAME, "/done")
        await asyncio.sleep(MESSAGE_DELAY)
        
        # Send time limit
        print(f"Setting time limit: {TIME_LIMIT}")
        await client.send_message(BOT_USERNAME, TIME_LIMIT)
        await asyncio.sleep(MESSAGE_DELAY)
        
        # Send shuffle option
        print(f"Setting shuffle: {SHUFFLE_OPTION}")
        await client.send_message(BOT_USERNAME, SHUFFLE_OPTION)
        await asyncio.sleep(MESSAGE_DELAY)
        
        # Get the quiz link from bot's response
        quiz_link = None
        async for message in client.get_chat_history(BOT_USERNAME, limit=5):
            if message.text and "t.me/QuizBot?start=" in message.text:
                # Extract the link using regex
                match = re.search(r't\.me/QuizBot\?start=\w+', message.text)
                if match:
                    quiz_link = f"https://{match.group(0)}"
                    break
        
        if quiz_link:
            print(f"\n✓ Successfully created quiz: {quiz.name}")
            print(f"  Link: {quiz_link}\n")
        else:
            print(f"\n⚠ Quiz created but couldn't extract link for: {quiz.name}\n")
            
        return quiz_link
        
    except Exception as e:
        print(f"\n✗ Error creating quiz {quiz.name}: {e}")
        import traceback
        traceback.print_exc()
        return None


async def save_links_to_saved_messages(client: Client, quiz_links: list[tuple[str, str]]):
    """
    Save all quiz links to Saved Messages (send to self).
    
    Args:
        client: Kurigram Client instance
        quiz_links: List of tuples (quiz_name, quiz_link)
    """
    if not quiz_links:
        print("No quiz links to save.")
        return
        
    print("\n" + "="*60)
    print("Saving quiz links to Saved Messages...")
    print("="*60 + "\n")
    
    # Format the message
    message_lines = ["📚 **Created Quizzes**\n"]
    for name, link in quiz_links:
        message_lines.append(f"• **{name}**: {link}")
    
    message = "\n".join(message_lines)
    
    # Send to "me" (Saved Messages)
    await client.send_message("me", message)
    print("✓ Quiz links saved to Saved Messages!")


async def main():
    """Main function to process quiz files and create quizzes."""
    # Load environment variables
    load_dotenv()
    
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    phone_number = os.getenv('PHONE_NUMBER')
    quizzes_folder = os.getenv('QUIZZES_FOLDER', './quizzes')
    
    # Validate environment variables
    if not api_id or not api_hash:
        print("Error: API_ID and API_HASH must be set in .env file")
        print("Get these from https://my.telegram.org/apps")
        sys.exit(1)
        
    if not phone_number:
        print("Error: PHONE_NUMBER must be set in .env file")
        sys.exit(1)
    
    # Find quiz files
    print(f"Looking for quiz files in: {quizzes_folder}")
    quiz_files = find_quiz_files(quizzes_folder)
    
    if not quiz_files:
        print(f"No .txt files found in {quizzes_folder}")
        print("Please create quiz files in the format specified in README.md")
        sys.exit(1)
        
    print(f"Found {len(quiz_files)} quiz file(s):")
    for qf in quiz_files:
        print(f"  - {os.path.basename(qf)}")
    print()
    
    # Parse quiz files
    quizzes = []
    for quiz_file in quiz_files:
        print(f"Parsing {os.path.basename(quiz_file)}...")
        quiz = parse_quiz_file(quiz_file)
        if quiz:
            quizzes.append(quiz)
            print(f"  ✓ Parsed: {quiz.name} ({len(quiz.questions)} questions)")
        else:
            print(f"  ✗ Failed to parse {quiz_file}")
    
    if not quizzes:
        print("\nNo valid quizzes found. Please check your quiz files.")
        sys.exit(1)
        
    print(f"\n{len(quizzes)} quiz(es) ready to create.\n")
    
    # Initialize Kurigram client
    app = Client(
        "autoquiz_session",
        api_id=int(api_id),
        api_hash=api_hash,
        phone_number=phone_number
    )
    
    try:
        print("Starting Telegram client...")
        await app.start()
        print("✓ Connected to Telegram\n")
        
        # Collect created quiz links
        quiz_links: list[tuple[str, str]] = []
        
        # Create each quiz
        for quiz in quizzes:
            try:
                link = await create_quiz_in_bot(app, quiz)
                if link:
                    quiz_links.append((quiz.name, link))
                # Wait between quizzes to avoid rate limiting
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Failed to create quiz {quiz.name}: {e}")
                continue
        
        # Save all links to Saved Messages
        await save_links_to_saved_messages(app, quiz_links)
                
        print("\n" + "="*60)
        print(f"All quizzes processed! Created {len(quiz_links)}/{len(quizzes)} quizzes.")
        print("="*60)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        print("\nStopping Telegram client...")
        await app.stop()
        print("✓ Disconnected")


if __name__ == "__main__":
    asyncio.run(main())
