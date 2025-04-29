import FreeSimpleGUI as sg
import json
import time
from QuestionGenerator import generate_question, question_buffer
from Database import Database
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import os
import io
import random

# Set dark theme colors
sg.theme('DarkBlue3')

class ExamMode:
    def __init__(self, username):
        self.username = username
        self.db = Database()
        self.image_reference = None
        
        # Load questions
        with open('Questions.json') as f:
            self.questions = json.load(f)['questions']
        
        # Get unique paper types
        paper_types = {q_data['paper'] for q_data in self.questions.values()}
        
        # Define the layout with dark theme
        layout = [
            [sg.Text('Select Exam Paper', font=('Segoe UI', 20), justification='center', size=(30, 1), text_color='white', background_color='#1E1E1E')],
        ]
        
        # Add radio buttons for each paper type
        for paper in sorted(paper_types):
            layout.append([sg.Radio(paper, "PAPER", key=f'-{paper}-', font=('Segoe UI', 12), text_color='white', background_color='#1E1E1E')])
        
        layout.extend([
            [sg.Button('Start Exam', size=(15, 2), font=('Segoe UI', 12), button_color=('white', '#0078D7')),
             sg.Button('Back to Main Menu', size=(15, 2), font=('Segoe UI', 12), button_color=('white', '#0078D7'))],
            [sg.Text('', key='-ERROR-', text_color='#FF4444', font=('Segoe UI', 12), background_color='#1E1E1E')]
        ])
        
        # Create the window
        self.window = sg.Window('Exam Paper Selector', layout, size=(401, 400), element_justification='center', background_color='#1E1E1E', finalize=True)
    
    def show_question(self, question_num, question_id, question_data, correct_answer):
        # Start timing for this question
        question_start_time = time.time()
        
        # Calculate total possible marks for this question
        if 'answerbox' in question_data:
            total_marks = sum(box['marks'] for box in question_data['answerbox'])
        else:
            total_marks = question_data.get('marks', 1)
        
        # Generate the question and get the image buffer
        answer, image_buffer = generate_question(question_id)
        
        # Load image to check dimensions
        img = Image.open(image_buffer)
        max_height = 600
        
        # Only scale down if image is too tall
        if img.height > max_height:
            # Calculate new width while maintaining aspect ratio
            width_percent = (max_height / float(img.height))
            new_width = int((float(img.width) * float(width_percent)))
            # Resize image
            img = img.resize((new_width, max_height), Image.Resampling.LANCZOS)
            # Convert back to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
        else:
            img_byte_arr = image_buffer.getvalue()
        
        # Save the original image temporarily
        temp_img_path = os.path.join(os.getenv('TEMP'), f'question_{question_id}.png')
        with open(temp_img_path, 'wb') as f:
            f.write(image_buffer.getvalue())
        
        # Create layout for question window
        layout = [
            [sg.Text(f'Question {question_num}', font=('Segoe UI', 16), text_color='white', background_color='#1E1E1E')],
            [sg.Image(data=img_byte_arr, key='-IMAGE-', background_color='#1e1e1e', enable_events=True)],
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
                        # Only try to extract index if label is in format "(number)"
                        if label.startswith('(') and label.endswith(')'):
                            try:
                                index = int(label.strip('()')) - 1
                                if 0 <= index < len(correct_answer):
                                    correct_answer_dict[label] = str(correct_answer[index])
                                else:
                                    correct_answer_dict[label] = str(correct_answer[0])
                            except (ValueError, IndexError):
                                correct_answer_dict[label] = str(correct_answer[0])
                        else:
                            # For non-numeric labels, use the first answer
                            correct_answer_dict[label] = str(correct_answer[0])
                    else:
                        # If answer is a single value, use it for all boxes
                        correct_answer_dict[label] = str(correct_answer)
                correct_answer = correct_answer_dict
            else:
                # If it's already a dictionary, ensure all values are strings
                correct_answer = {k: str(v) for k, v in correct_answer.items()}

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
        
        # Create the window with larger size and maximize it
        question_window = sg.Window('Question', layout, size=(1200, 800), element_justification='center', 
                                  background_color='#1E1E1E', finalize=True, resizable=True)
        question_window.maximize()
        
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
                        correct_ans = correct_answer[label].strip()
                        
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
                        marks_earned = total_marks
                        question_window['-RESULT-'].update(f'All answers correct! (+{total_marks} marks)', text_color='#00FF00')
                        # Lock the answer boxes
                        for box in question_data['answerbox']:
                            label = box['label']
                            question_window[f'-ANSWER-{label}'].update(disabled=True)
                        question_window['Submit'].update(disabled=True)
                        
                        # Update statistics for correct answer
                        time_taken = time.time() - question_start_time
                        self.db.update_user_statistics(
                            self.username,
                            question_data['topic'],
                            True,  # is_correct
                            marks_earned,
                            total_marks,
                            time_taken
                        )
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
                            
                            # Update statistics for incorrect answer
                            time_taken = time.time() - question_start_time
                            self.db.update_user_statistics(
                                self.username,
                                question_data['topic'],
                                False,  # is_correct
                                0,  # marks_earned
                                total_marks,
                                time_taken
                            )
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
                        marks_earned = total_marks
                        question_window['-RESULT-'].update(f'Correct! (+{total_marks} marks)', text_color='#00FF00')
                        # Lock the answer box
                        question_window['-ANSWER-'].update(disabled=True)
                        question_window['Submit'].update(disabled=True)
                        
                        # Update statistics for correct answer
                        time_taken = time.time() - question_start_time
                        self.db.update_user_statistics(
                            self.username,
                            question_data['topic'],
                            True,  # is_correct
                            marks_earned,
                            total_marks,
                            time_taken
                        )
                    else:
                        if first_attempt:
                            question_window['-RESULT-'].update('Incorrect. Try again.', text_color='#FF4444')
                            first_attempt = False
                        else:
                            # Show correct answer and lock the box
                            question_window['-RESULT-'].update(f'Correct answer: {correct_ans}', text_color='#FF4444')
                            question_window['-ANSWER-'].update(disabled=True)
                            question_window['Submit'].update(disabled=True)
                            
                            # Update statistics for incorrect answer
                            time_taken = time.time() - question_start_time
                            self.db.update_user_statistics(
                                self.username,
                                question_data['topic'],
                                False,  # is_correct
                                0,  # marks_earned
                                total_marks,
                                time_taken
                            )
            
            if event == 'Next':
                question_window.close()
                # Clean up temporary image file
                try:
                    os.remove(temp_img_path)
                except:
                    pass
                return True, marks_earned
            
            if event == '-IMAGE-':
                # Open image in Windows Photo Viewer
                os.startfile(temp_img_path)

    def show_summary(self, total_marks, total_possible_marks, question_marks, paper):
        # Prevent division by zero
        if total_possible_marks == 0:
            percentage = 0
        else:
            percentage = round((total_marks/total_possible_marks)*100, 1)
            
        # Create a table of marks per question
        marks_table = []
        for i, (q_id, marks) in enumerate(question_marks.items(), 1):
            topic = self.questions[q_id]['topic']
            marks_table.append([f'Question {i}', topic, f'{marks} marks'])
            
        summary_layout = [
            [sg.Text('Exam Complete!', font=('Segoe UI', 20), text_color='white', background_color='#1E1E1E')],
            [sg.Text(f'Total Marks: {total_marks}/{total_possible_marks}', font=('Segoe UI', 16), text_color='white', background_color='#1E1E1E')],
            [sg.Text(f'Percentage: {percentage}%', font=('Segoe UI', 16), text_color='white', background_color='#1E1E1E')],
            [sg.Text('Marks per Question:', font=('Segoe UI', 16), text_color='white', background_color='#1E1E1E')],
            [sg.Table(values=marks_table, headings=['Question', 'Topic', 'Marks'], 
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
                self.window.close()
                return 'closed'
            
            if event == 'Back to Main Menu':
                self.window.close()
                return 'back_to_main'
            
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
                        [sg.Button('Start Exam', size=(10, 1), font=('Segoe UI', 12), button_color=('white', '#0078D7'))]
                    ]
                    
                    info_window = sg.Window('Answer Format Guidelines', info_layout, size=(400, 400), 
                                          element_justification='center', background_color='#1E1E1E', finalize=True)
                    
                    while True:
                        event, _ = info_window.read()
                        if event in (sg.WIN_CLOSED, 'Start Exam'):
                            info_window.close()
                            break
                    
                    # Start the exam
                    total_marks = 0
                    total_possible_marks = 0
                    question_marks = {}
                    
                    # Get questions for selected paper and randomize order
                    paper_questions = [(q_id, q_data) for q_id, q_data in self.questions.items() 
                                     if q_data['paper'] == selected_paper]
                    random.shuffle(paper_questions)
                    
                    for question_num, (question_id, question_data) in enumerate(paper_questions, 1):
                        # Generate question and get correct answer
                        correct_answer, _ = generate_question(question_id)
                        
                        # Show question and get result
                        continue_exam, marks = self.show_question(question_num, question_id, question_data, correct_answer)
                        
                        if not continue_exam:
                            self.window.close()
                            return 'closed'
                        
                        # Update marks
                        question_marks[question_id] = marks
                        total_marks += marks
                        
                        # Calculate total possible marks
                        if 'answerbox' in question_data:
                            total_possible_marks += sum(box['marks'] for box in question_data['answerbox'])
                        else:
                            total_possible_marks += question_data.get('marks', 1)
                    
                    # Show summary
                    self.show_summary(total_marks, total_possible_marks, question_marks, selected_paper)
                else:
                    self.window['-ERROR-'].update('Please select a paper')
        
        self.window.close()
        return None

if __name__ == "__main__":
    app = ExamMode("test_user")
    selected_paper = app.run()
    if selected_paper:
        print(f"Selected paper: {selected_paper}")
