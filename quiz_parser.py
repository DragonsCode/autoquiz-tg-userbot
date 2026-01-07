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
    - Then for each question:
      - Question text
      - Answer A) ...
      - Answer B) ...
      - Answer C) ...
      - Answer D) ...
      - (blank line)
      - Correct answer (one of A, B, C, or D with full text)
      - (blank line)
    
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
            
        if len(lines) < 2:
            print(f"Error: File {filepath} must have at least 2 lines (name and description)")
            return None
            
        name = lines[0].strip()
        description = lines[1].strip()
        
        # Parse questions - handle blank lines properly
        questions = []
        i = 2
        
        while i < len(lines):
            # Skip empty lines
            while i < len(lines) and not lines[i].strip():
                i += 1
            
            if i >= len(lines):
                break
                
            # Question text (doesn't start with A), B), C), D))
            question_text = lines[i].strip()
            i += 1
            
            # Collect 4 answer options (A, B, C, D)
            answers = []
            while i < len(lines) and len(answers) < 4:
                line = lines[i].strip()
                if not line:
                    i += 1
                    continue
                # Check if it looks like an answer option (starts with A), B), C), or D))
                if len(line) >= 2 and line[0] in 'ABCD' and line[1] == ')':
                    answers.append(line)
                    i += 1
                else:
                    break
            
            if len(answers) != 4:
                print(f"Warning: Expected 4 answers for question '{question_text[:40]}...', got {len(answers)}")
                continue
            
            # Skip empty lines before correct answer
            while i < len(lines) and not lines[i].strip():
                i += 1
            
            if i >= len(lines):
                print(f"Warning: No correct answer found for question '{question_text[:40]}...'")
                break
                
            correct_answer = lines[i].strip()
            i += 1
            
            # Verify that the correct answer matches one of the options
            if correct_answer not in answers:
                print(f"Warning: Correct answer '{correct_answer[:40]}...' not found in options for '{question_text[:40]}...'")
                # Try to match by first letter (A, B, C, D)
                if correct_answer and correct_answer[0] in 'ABCD':
                    for ans in answers:
                        if ans.startswith(correct_answer[0] + ')'):
                            correct_answer = ans
                            break
                            
            if correct_answer in answers:
                questions.append(QuizQuestion(question_text, answers, correct_answer))
            else:
                print(f"  Skipping question due to format error.")
                
        if not questions:
            print(f"Warning: No questions found in {filepath}")
            return None
        
        print(f"  Parsed {len(questions)} questions from {os.path.basename(filepath)}")
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
