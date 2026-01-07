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
      - Answer options (one per line)
      - Correct answer (duplicated)
    
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
            
        name = lines[0]
        description = lines[1]
        
        # Parse questions from remaining lines
        questions = []
        i = 2
        
        while i < len(lines):
            # Skip empty lines
            if not lines[i].strip():
                i += 1
                continue
                
            # Read question
            question = lines[i]
            i += 1
            
            # Read answers until we find the correct answer marker
            answers = []
            correct_answer = None
            
            while i < len(lines):
                line = lines[i]
                i += 1
                
                # Empty line might indicate end of question
                if not line.strip():
                    break
                    
                # Check if this might be a new question (heuristic: starts with capital or number)
                # But first we need to collect answers
                answers.append(line)
                
                # Look ahead to see if next line is a duplicate (correct answer)
                if i < len(lines) and lines[i].strip() == line.strip():
                    correct_answer = line
                    i += 1  # Skip the duplicate
                    break
                    
                # If we have collected several answers and no duplicate yet,
                # the last one might be the correct answer
                if len(answers) >= 4 and correct_answer is None:
                    # Assume last answer is correct and might not be duplicated
                    correct_answer = answers[-1]
                    break
            
            if not correct_answer and answers:
                # If no duplicate found, assume last answer is correct
                correct_answer = answers[-1]
                
            if question and answers and correct_answer:
                questions.append(QuizQuestion(question, answers, correct_answer))
            
        if not questions:
            print(f"Warning: No questions found in {filepath}")
            return None
            
        return Quiz(name, description, questions)
        
    except Exception as e:
        print(f"Error parsing file {filepath}: {e}")
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
