"""
Quiz file parser module.
Parses quiz files in the expected format.
"""
import os
from typing import List, Dict, Optional


class QuizQuestion:
    """Represents a single quiz question with answers."""
    
    def __init__(self, question: str, answers: List[str], correct_answer: str):
        self.question = question.strip()
        self.answers = [a.strip() for a in answers]
        self.correct_answer = correct_answer.strip()
        
    def __repr__(self):
        return f"QuizQuestion(q={self.question[:30]}..., answers={len(self.answers)}, correct={self.correct_answer[:20]}...)"


class Quiz:
    """Represents a complete quiz with metadata and questions."""
    
    def __init__(self, name: str, description: str, questions: List[QuizQuestion]):
        self.name = name.strip()
        self.description = description.strip()
        self.questions = questions
        
    def __repr__(self):
        return f"Quiz(name={self.name}, description={self.description[:30]}..., questions={len(self.questions)})"


def parse_quiz_file(filepath: str) -> Optional[Quiz]:
    """
    Parse a quiz file and return a Quiz object.
    
    Expected format:
    - Line 1: Quiz name
    - Line 2: Quiz description
    - Then for each question (repeated for all 20 questions):
      - Question text
      - Answer option 1
      - Answer option 2
      - Answer option 3
      - Answer option 4
      - Correct answer (duplicate of one of the options above)
    
    Args:
        filepath: Path to the quiz file
        
    Returns:
        Quiz object or None if parsing fails
    """
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} does not exist")
        return None
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f.readlines()]
            
        # Remove empty lines
        lines = [line for line in lines if line.strip()]
            
        if len(lines) < 2:
            print(f"Error: File {filepath} must have at least 2 lines (name and description)")
            return None
            
        name = lines[0]
        description = lines[1]
        
        # Parse questions from remaining lines
        # Each question has: question + 4 answers + 1 correct answer marker = 6 lines
        questions = []
        i = 2
        
        while i < len(lines):
            # Need at least 6 lines for a complete question (question + 4 answers + correct marker)
            if i + 5 >= len(lines):
                break
                
            question_text = lines[i]
            answer1 = lines[i + 1]
            answer2 = lines[i + 2]
            answer3 = lines[i + 3]
            answer4 = lines[i + 4]
            correct_answer = lines[i + 5]
            
            # Collect all answers
            answers = [answer1, answer2, answer3, answer4]
            
            # Verify that the correct answer matches one of the options
            if correct_answer not in answers:
                print(f"ERROR: In file {filepath}")
                print(f"  Question: {question_text[:60]}...")
                print(f"  Correct answer '{correct_answer}' not found in options:")
                for i, ans in enumerate(answers, 1):
                    print(f"    {i}. {ans}")
                print(f"  Skipping this question due to format error.")
                # Skip this question and continue to next
                i += 6
                continue
                
            questions.append(QuizQuestion(question_text, answers, correct_answer))
            
            # Move to next question (6 lines per question)
            i += 6
            
        if not questions:
            print(f"Warning: No questions found in {filepath}")
            return None
            
        return Quiz(name, description, questions)
        
    except Exception as e:
        print(f"Error parsing file {filepath}: {e}")
        import traceback
        traceback.print_exc()
        return None


def find_quiz_files(folder: str) -> List[str]:
    """
    Find all .txt files in the specified folder.
    
    Args:
        folder: Path to folder containing quiz files
        
    Returns:
        List of file paths
    """
    if not os.path.exists(folder):
        print(f"Error: Folder {folder} does not exist")
        return []
        
    quiz_files = []
    for filename in os.listdir(folder):
        if filename.endswith('.txt'):
            quiz_files.append(os.path.join(folder, filename))
            
    return sorted(quiz_files)
