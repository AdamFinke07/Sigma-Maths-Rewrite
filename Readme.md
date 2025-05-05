# Sigma Maths

## Overview
This is a mathematics practice and exam system designed to help students prepare for A-Level mathematics exams. The system includes practice mode, exam mode, and comprehensive user statistics tracking.

## Core Files

### Main.py
- Entry point of the application
- Handles user authentication and navigation between different modes
- Manages the main application window

### QuestionGenerator.py
Core functionality for generating mathematical questions:
- Dynamic question generation based on templates
- Variable generation and management
- Mathematical expression processing
- Image and graph generation for questions
- Answer validation and processing

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
- Timed exam sessions
- Question presentation and answer collection
- Score calculation and feedback
- Progress tracking
- Results summary and analysis

### PracticeMode.py
Manages practice sessions:
- Topic-specific practice
- Instant feedback on answers
- Detailed solution explanations
- Progress tracking
- Adaptive difficulty

### Database.py
Comprehensive data management system:
- User authentication and session management
- Statistics and performance tracking
- Question history and marks storage
- User preferences and settings
- Progress analytics

### PtQt6UI.py
Unified UI management system:
- Centralized UI component handling
- Consistent styling across all windows
- Dynamic form generation
- Responsive layouts
- Interactive elements for question display

### Authentication Files
- `Login.py`: Handles user login process
- `Register.py`: Manages new user registration

### Additional Components
- `Statistics.py`: Detailed performance analytics and visualization
- `Settings.py`: User preferences and application configuration
- `MarksView.py`: Exam and practice session results viewer

### Configuration Files
- `Questions.json`: Question templates and configurations
- `requirements.txt`: Python package dependencies

## Directory Structure
- `Assets/`: Contains database files and UI resources
- `Questions/`: Stores generated question images and resources
- `Fonts/`: Custom fonts for UI rendering

## Data Flow
1. User authentication through Login/Register system
2. Main menu provides access to:
   - Practice Mode
   - Exam Mode
   - Statistics
   - Settings
3. Questions are dynamically generated using QuestionGenerator.py
4. User interactions are managed through PtQt6UI.py
5. Data is persistently stored using Database.py
6. Statistics and performance are tracked and visualized

## Key Features
- Dynamic question generation with LaTeX support
- Real-time answer validation
- Comprehensive progress tracking
- Realistic exam simulation
- Practice mode with detailed feedback
- Advanced statistics and performance analysis
- Modern, responsive UI
- Secure user authentication
- Persistent data storage 