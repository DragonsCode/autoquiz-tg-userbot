"""
AutoQuiz Telegram Userbot
Creates quizzes in @QuizBot from text files.
"""
import os
import sys
import asyncio
from dotenv import load_dotenv
from kurigram import Client
from quiz_parser import find_quiz_files, parse_quiz_file


async def create_quiz_in_bot(client: Client, quiz):
    """
    Create a quiz in @QuizBot using the provided quiz data.
    
    Args:
        client: Kurigram Client instance
        quiz: Quiz object containing quiz data
    """
    bot_username = "QuizBot"
    
    try:
        print(f"\n{'='*60}")
        print(f"Creating quiz: {quiz.name}")
        print(f"Description: {quiz.description}")
        print(f"Questions: {len(quiz.questions)}")
        print(f"{'='*60}\n")
        
        # Start conversation with QuizBot
        await client.send_message(bot_username, "/start")
        await asyncio.sleep(2)
        
        # Send /newquiz command to create a new quiz
        await client.send_message(bot_username, "/newquiz")
        await asyncio.sleep(2)
        
        # Send quiz name
        await client.send_message(bot_username, quiz.name)
        await asyncio.sleep(2)
        
        # Send quiz description
        await client.send_message(bot_username, quiz.description)
        await asyncio.sleep(2)
        
        # Send each question
        for idx, question in enumerate(quiz.questions, 1):
            print(f"Sending question {idx}/{len(quiz.questions)}: {question.question[:50]}...")
            
            # Send question text
            await client.send_message(bot_username, question.question)
            await asyncio.sleep(2)
            
            # Send answers
            for answer in question.answers:
                await client.send_message(bot_username, answer)
                await asyncio.sleep(1)
                
            # Mark correct answer (might need to send the answer text again or a specific command)
            # This depends on QuizBot's exact protocol
            # Some bots require you to select/mark the correct answer
            await asyncio.sleep(2)
            
        # Finish quiz creation (send /done or similar command)
        await client.send_message(bot_username, "/done")
        await asyncio.sleep(2)
        
        print(f"✓ Successfully created quiz: {quiz.name}\n")
        
    except Exception as e:
        print(f"✗ Error creating quiz {quiz.name}: {e}")
        raise


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
        
        # Create each quiz
        for quiz in quizzes:
            try:
                await create_quiz_in_bot(app, quiz)
                # Wait a bit between quizzes to avoid rate limiting
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Failed to create quiz {quiz.name}: {e}")
                continue
                
        print("\n" + "="*60)
        print("All quizzes processed!")
        print("="*60)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        print("\nStopping Telegram client...")
        await app.stop()
        print("✓ Disconnected")


if __name__ == "__main__":
    asyncio.run(main())
