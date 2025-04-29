# Sigma Maths Documentation

## Overview
This is a mathematics practice and exam system designed to help students prepare for A-Level mathematics exams. The system includes practice mode, exam mode, and tracks user statistics.

## Core Files

### Main.py
- Entry point of the application
- Handles user authentication and navigation between different modes
- Manages the main application window

### QuestionGenerator.py
Core functionality for generating mathematical questions:
- `VariableType`: Enum defining different types of variables (integer, float, string, list, graph)
- `Variable`: Class representing a variable with name, value, and type
- `plot`: Generates polynomial function plots with optional shaded regions
- `generate_image`: Creates question images with text and graphs
- `generate_question`: Main function that generates questions based on JSON configuration
- `generate_variables`: Creates variables based on specifications
- `calculate_answer`: Processes answer steps and calculates final answers

### Maths.py
Mathematical utility functions:
- `Rcos`: Converts linear combination of cosine and sine to Rcos(x + α) form
- `surd`: Simplifies square root expressions
- `primefactors`: Finds prime factors of a number
- `complete_square`: Completes the square for quadratic expressions
- `dijkstra`: Finds shortest path in a weighted graph
- `integrate`: Calculates definite integrals of polynomials
- `merge_sort`: Sorts lists using merge sort algorithm
- `roots`: Finds roots of polynomial equations

### ExamMode.py
Handles exam functionality:
- `ExamMode`: Main class managing exam sessions
  - `__init__`: Sets up exam paper selection interface
  - `show_question`: Displays questions and handles user answers
  - `show_summary`: Shows exam results and statistics
  - `run`: Main exam loop

### PracticeMode.py
Handles practice sessions:
- `PracticeMode`: Main class managing practice sessions
  - `__init__`: Sets up practice interface
  - `show_question`: Displays practice questions
  - `run`: Main practice loop

### Database.py
Manages user data and statistics:
- `Database`: Class handling database operations
  - User authentication
  - Statistics tracking
  - Marks storage
  - User management

### UI Files
- `MainMenu_ui.py`: Main menu interface
- `Login_ui.py`: Login interface
- `Register_ui.py`: Registration interface
- `Statistics_ui.py`: Statistics display interface
- `MarksView_ui.py`: Marks viewing interface
- `Settings_ui.py`: Settings interface

### Configuration Files
- `Questions.json`: Question templates and configurations
- `requirements.txt`: Python package dependencies

## Data Flow
1. User logs in through Login.py
2. Main menu (MainMenu_ui.py) provides access to:
   - Practice Mode
   - Exam Mode
   - Statistics
   - Settings
3. Questions are generated using QuestionGenerator.py
4. User answers are processed and stored in Database.py
5. Statistics are tracked and displayed through Statistics.py

## Key Features
- Dynamic question generation
- Real-time answer validation
- Progress tracking
- Exam simulation
- Practice mode with instant feedback
- Statistics and performance analysis 