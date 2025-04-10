import PySimpleGUI as sg
import json
from QuestionGenerator import generate_question
from Database import Database

# Set dark theme colors
sg.theme('DarkBlue3')

class ExamMode:
    def __init__(self, username):
        # Load questions from JSON
        with open('Questions.json') as f:
            self.questions_data = json.load(f)['questions']
        
        self.username = username
        self.db = Database()
        
        # Get unique paper types
        paper_types = set()
        for q_id, q_data in self.questions_data.items():
            paper_types.add(q_data['paper'])
        
        # Define the layout with dark theme
        layout = [
            [sg.Text('Select Exam Paper', font=('Segoe UI', 20), justification='center', size=(30, 1), text_color='white', background_color='#1E1E1E')],
        ]
        
        # Add radio buttons for each paper type
        for paper in sorted(paper_types):
            layout.append([sg.Radio(paper, "PAPER", key=f'-{paper}-', font=('Segoe UI', 12), text_color='white', background_color='#1E1E1E')])
        
        layout.extend([
            [sg.Button('Start Exam', size=(15, 2), font=('Segoe UI', 12), button_color=('white', '#0078D7'))],
            [sg.Text('', key='-ERROR-', text_color='#FF4444', font=('Segoe UI', 12), background_color='#1E1E1E')]
        ])
        
        # Create the window
        self.window = sg.Window('Exam Paper Selector', layout, size=(401, 400), element_justification='center', background_color='#1E1E1E', finalize=True)
    
    def show_question(self, question_id, question_data, correct_answer):
        # Create layout for question window
        layout = [
            [sg.Text(f'Question {question_id}', font=('Segoe UI', 16), text_color='white', background_color='#1E1E1E')],
            [sg.Image(filename='edited.png', key='-IMAGE-')],
        ]

        # Check if question has answerbox
        if 'answerbox' in question_data:
            # Convert correct_answer to dictionary format if it's not already
            if not isinstance(correct_answer, dict):
                correct_answer_dict = {}
                for box in question_data['answerbox']:
                    label = box['label']
                    answer_var = box['answer']
                    if isinstance(correct_answer, tuple):
                        # If answer is a tuple, use the corresponding index
                        index = int(label.strip(')')) - 1
                        correct_answer_dict[label] = str(correct_answer[index])
                    else:
                        # If answer is a single value, use it for all boxes
                        correct_answer_dict[label] = str(correct_answer)
                correct_answer = correct_answer_dict

            # Add input fields for each answer box
            for box in question_data['answerbox']:
                label = box['label']
                layout.extend([
                    [sg.Text(f'{label}', font=('Segoe UI', 12), text_color='white', background_color='#1E1E1E')],
                    [sg.Input(key=f'-ANSWER-{label}', size=(30, 1), font=('Segoe UI', 12))]
                ])
        else:
            # Single answer input for questions without answerbox
            layout.extend([
                [sg.Input(key='-ANSWER-', size=(30, 1), font=('Segoe UI', 12))]
            ])

        layout.extend([
            [sg.Button('Submit', size=(10, 1), font=('Segoe UI', 12), button_color=('white', '#0078D7')),
             sg.Button('Next', size=(10, 1), font=('Segoe UI', 12), button_color=('white', '#0078D7'))],
            [sg.Text('', key='-RESULT-', text_color='white', font=('Segoe UI', 12), background_color='#1E1E1E')]
        ])
        
        # Create the window with larger size
        question_window = sg.Window('Question', layout, size=(1200, 800), element_justification='center', background_color='#1E1E1E', finalize=True)
        
        # Force the window to be on top
        question_window.bring_to_front()
        
        # Track if this is the first attempt
        first_attempt = True
        marks_earned = 0
        
        # Main event loop
        while True:
            event, values = question_window.read()
            
            if event == sg.WIN_CLOSED:
                question_window.close()
                return False, 0
            
            if event == 'Submit':
                if 'answerbox' in question_data:
                    # Handle multiple answers
                    user_answers = {}
                    for box in question_data['answerbox']:
                        label = box['label']
                        user_answers[label] = values[f'-ANSWER-{label}']
                    
                    # Compare each answer
                    all_correct = True
                    result_text = []
                    for label, user_answer in user_answers.items():
                        # Clean up the answers for comparison
                        user_ans = user_answer.strip()
                        correct_ans = str(correct_answer[label]).strip()
                        
                        # Try to convert to float for numerical comparison
                        try:
                            user_float = float(user_ans)
                            correct_float = float(correct_ans)
                            correct = abs(user_float - correct_float) < 0.001  # Allow small floating point differences
                        except ValueError:
                            # If conversion fails, do string comparison
                            correct = user_ans == correct_ans
                        
                        if not correct:
                            all_correct = False
                    
                    if all_correct:
                        # Calculate marks for correct answer
                        total_marks = sum(box['marks'] for box in question_data['answerbox'])
                        marks_earned = total_marks
                        question_window['-RESULT-'].update(f'All answers correct! (+{total_marks} marks)', text_color='#00FF00')
                        # Lock the answer boxes
                        for box in question_data['answerbox']:
                            label = box['label']
                            question_window[f'-ANSWER-{label}'].update(disabled=True)
                        question_window['Submit'].update(disabled=True)
                    else:
                        if first_attempt:
                            question_window['-RESULT-'].update('Incorrect. Try again.', text_color='#FF4444')
                            first_attempt = False
                        else:
                            # Show correct answers and lock the boxes
                            result_text = []
                            for label, correct_ans in correct_answer.items():
                                result_text.append(f'{label} Correct answer: {correct_ans}')
                            question_window['-RESULT-'].update('\n'.join(result_text), text_color='#FF4444')
                            # Lock the answer boxes
                            for box in question_data['answerbox']:
                                label = box['label']
                                question_window[f'-ANSWER-{label}'].update(disabled=True)
                            question_window['Submit'].update(disabled=True)
                else:
                    # Handle single answer
                    user_answer = values['-ANSWER-'].strip()
                    correct_ans = str(correct_answer).strip()
                    
                    # Try to convert to float for numerical comparison
                    try:
                        user_float = float(user_answer)
                        correct_float = float(correct_ans)
                        correct = abs(user_float - correct_float) < 0.001  # Allow small floating point differences
                    except ValueError:
                        # If conversion fails, do string comparison
                        correct = user_answer == correct_ans
                    
                    if correct:
                        # Get marks from question data
                        marks = question_data.get('marks', 1)  # Default to 1 mark if not specified
                        marks_earned = marks
                        question_window['-RESULT-'].update(f'Correct! (+{marks} marks)', text_color='#00FF00')
                        # Lock the answer box
                        question_window['-ANSWER-'].update(disabled=True)
                        question_window['Submit'].update(disabled=True)
                    else:
                        if first_attempt:
                            question_window['-RESULT-'].update('Incorrect. Try again.', text_color='#FF4444')
                            first_attempt = False
                        else:
                            # Show correct answer and lock the box
                            question_window['-RESULT-'].update(f'Correct answer: {correct_ans}', text_color='#FF4444')
                            question_window['-ANSWER-'].update(disabled=True)
                            question_window['Submit'].update(disabled=True)
            
            if event == 'Next':
                question_window.close()
                return True, marks_earned

    def show_summary(self, total_marks, total_possible_marks, question_marks, paper):
        # Prevent division by zero
        if total_possible_marks == 0:
            percentage = 0
        else:
            percentage = round((total_marks/total_possible_marks)*100, 1)
            
        # Create a table of marks per question
        marks_table = []
        for q_id, marks in question_marks.items():
            marks_table.append([f'Question {q_id}', f'{marks} marks'])
            
        summary_layout = [
            [sg.Text('Exam Complete!', font=('Segoe UI', 20), text_color='white', background_color='#1E1E1E')],
            [sg.Text(f'Total Marks: {total_marks}/{total_possible_marks}', font=('Segoe UI', 16), text_color='white', background_color='#1E1E1E')],
            [sg.Text(f'Percentage: {percentage}%', font=('Segoe UI', 16), text_color='white', background_color='#1E1E1E')],
            [sg.Text('Marks per Question:', font=('Segoe UI', 16), text_color='white', background_color='#1E1E1E')],
            [sg.Table(values=marks_table, headings=['Question', 'Marks'], 
                     auto_size_columns=True, justification='center',
                     font=('Segoe UI', 12), text_color='white', background_color='#1E1E1E',
                     header_font=('Segoe UI', 12, 'bold'), header_text_color='white',
                     header_background_color='#0078D7', num_rows=min(len(marks_table), 10))],
            [sg.Button('Close', size=(10, 1), font=('Segoe UI', 12), button_color=('white', '#0078D7'))]
        ]
        
        summary_window = sg.Window('Exam Summary', summary_layout, size=(400, 400), 
                                 element_justification='center', background_color='#1E1E1E', finalize=True)
        
        while True:
            event, _ = summary_window.read()
            if event in (sg.WIN_CLOSED, 'Close'):
                summary_window.close()
                break

    def run(self):
        while True:
            event, values = self.window.read()
            
            if event == sg.WIN_CLOSED:
                break
            
            if event == 'Start Exam':
                # Find selected paper
                selected_paper = None
                for key, value in values.items():
                    if key.startswith('-') and key.endswith('-') and value:
                        selected_paper = key[1:-1]  # Remove the '-' characters
                        break
                
                if selected_paper:
                    # Show information window before starting exam
                    info_layout = [
                        [sg.Text('Answer Format Guidelines', font=('Segoe UI', 16), text_color='white', background_color='#1E1E1E')],
                        [sg.Text('For answers involving square roots:', font=('Segoe UI', 12), text_color='white', background_color='#1E1E1E')],
                        [sg.Text('• Use the format "asqrt(b)"', font=('Segoe UI', 12), text_color='white', background_color='#1E1E1E')],
                        [sg.Text('• Example: 2sqrt(3) for 2√3', font=('Segoe UI', 12), text_color='white', background_color='#1E1E1E')],
                        [sg.Text('For decimal answers:', font=('Segoe UI', 12), text_color='white', background_color='#1E1E1E')],
                        [sg.Text('• Round to 3 decimal places if needed', font=('Segoe UI', 12), text_color='white', background_color='#1E1E1E')],
                        [sg.Text('• Example: 3.142', font=('Segoe UI', 12), text_color='white', background_color='#1E1E1E')],
                        [sg.Text('For vector answers:', font=('Segoe UI', 12), text_color='white', background_color='#1E1E1E')],
                        [sg.Text('• Use capital letters for vector names', font=('Segoe UI', 12), text_color='white', background_color='#1E1E1E')],
                        [sg.Text('• Example: AB for vector AB', font=('Segoe UI', 12), text_color='white', background_color='#1E1E1E')],
                        [sg.Button('Start Exam', size=(15, 2), font=('Segoe UI', 12), button_color=('white', '#0078D7'))]
                    ]
                    
                    info_window = sg.Window('Answer Format Information', info_layout, size=(400, 300), 
                                          element_justification='center', background_color='#1E1E1E', finalize=True)
                    
                    while True:
                        info_event, _ = info_window.read()
                        if info_event in (sg.WIN_CLOSED, 'Start Exam'):
                            info_window.close()
                            break
                    
                    print(f"Starting {selected_paper} exam...")
                    # Get questions for the selected paper
                    paper_questions = []
                    for q_id, q_data in self.questions_data.items():
                        if q_data['paper'] == selected_paper:
                            paper_questions.append(q_id)
                    
                    print(f"Found {len(paper_questions)} questions for {selected_paper}")
                    
                    if paper_questions:
                        # Close the main window
                        self.window.close()
                        
                        # Track total marks and marks per question
                        total_marks = 0
                        total_possible_marks = 0
                        question_marks = {}
                        
                        # Generate and show questions
                        for q_id in paper_questions:
                            try:
                                print(f"Generating question {q_id}...")
                                # Generate question and get answer
                                answer = generate_question(q_id)
                                print(f"Generated answer: {answer}")
                                question_data = self.questions_data[q_id]
                                
                                # Calculate total possible marks
                                if 'answerbox' in question_data:
                                    total_possible_marks += sum(box['marks'] for box in question_data['answerbox'])
                                else:
                                    total_possible_marks += question_data.get('marks', 1)
                                
                                # Show question window
                                print("Showing question window...")
                                continue_question, marks = self.show_question(q_id, question_data, answer)
                                question_marks[q_id] = marks
                                total_marks += marks
                                
                                # Update marks in database
                                self.db.add_marks(self.username, selected_paper, q_id, marks, 
                                                question_data.get('marks', 1) if 'answerbox' not in question_data 
                                                else sum(box['marks'] for box in question_data['answerbox']))
                                
                                if not continue_question:
                                    return selected_paper  # User closed the window
                                    
                            except Exception as e:
                                print(f"Error generating question {q_id}: {e}")
                                import traceback
                                traceback.print_exc()
                        
                        # Show summary window
                        self.show_summary(total_marks, total_possible_marks, question_marks, selected_paper)
                        return selected_paper
                else:
                    self.window['-ERROR-'].update('Please select a paper')
        
        self.window.close()
        return None

if __name__ == "__main__":
    app = ExamMode()
    selected_paper = app.run()
    if selected_paper:
        print(f"Selected paper: {selected_paper}")
