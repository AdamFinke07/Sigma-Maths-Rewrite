import FreeSimpleGUI as sg
import json
import random
from QuestionGenerator import generate_question
from Database import Database
import os
import io
from PIL import Image

# Set dark theme colors
sg.theme('DarkBlue3')

class PracticeMode:
    def __init__(self, username):
        self.username = username
        self.db = Database()
        
        # Load questions
        with open('Questions.json') as f:
            self.questions = json.load(f)['questions']
        
        # Get unique topics
        topics = {q_data['topic'] for q_data in self.questions.values()}
        
        # Define the layout with dark theme
        layout = [
            [sg.Text('Select Topic', font=('Segoe UI', 20), justification='center', size=(30, 1), 
                    text_color='white', background_color='#1E1E1E')],
        ]
        
        # Add radio buttons for each topic
        for topic in sorted(topics):
            layout.append([sg.Radio(topic, "TOPIC", key=f'-{topic}-', font=('Segoe UI', 12), 
                                  text_color='white', background_color='#1E1E1E')])
        
        layout.extend([
            [sg.Button('Start Practice', size=(15, 2), font=('Segoe UI', 12), button_color=('white', '#0078D7')),
             sg.Button('Back to Main Menu', size=(15, 2), font=('Segoe UI', 12), button_color=('white', '#0078D7'))],
            [sg.Text('', key='-ERROR-', text_color='#FF4444', font=('Segoe UI', 12), background_color='#1E1E1E')]
        ])
        
        # Create the window
        self.window = sg.Window('Topic Selector', layout, size=(401, 400), 
                              element_justification='center', background_color='#1E1E1E', finalize=True)

    def show_question(self, question_num, question_id, question_data, correct_answer):
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
                            correct_answer_dict[label] = str(correct_answer[0])
                    else:
                        correct_answer_dict[label] = str(correct_answer)
                correct_answer = correct_answer_dict
            else:
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
        
        # Main event loop
        while True:
            event, values = question_window.read()
            
            if event == sg.WIN_CLOSED:
                question_window.close()
                return False
            
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
                        question_window['-RESULT-'].update('All answers correct!', text_color='#00FF00')
                        # Lock the answer boxes
                        for box in question_data['answerbox']:
                            label = box['label']
                            question_window[f'-ANSWER-{label}'].update(disabled=True)
                        question_window['Submit'].update(disabled=True)
                    else:
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
                        question_window['-RESULT-'].update('Correct!', text_color='#00FF00')
                        # Lock the answer box
                        question_window['-ANSWER-'].update(disabled=True)
                        question_window['Submit'].update(disabled=True)
                    else:
                        question_window['-RESULT-'].update(f'Correct answer: {correct_ans}', text_color='#FF4444')
                        question_window['-ANSWER-'].update(disabled=True)
                        question_window['Submit'].update(disabled=True)
            
            if event == 'Next':
                question_window.close()
                # Clean up temporary image file
                try:
                    os.remove(temp_img_path)
                except:
                    pass
                return True
            
            if event == '-IMAGE-':
                # Open image in Windows Photo Viewer
                os.startfile(temp_img_path)

    def run(self):
        while True:
            event, values = self.window.read()
            
            if event == sg.WIN_CLOSED:
                self.window.close()
                return 'closed'
            
            if event == 'Back to Main Menu':
                self.window.close()
                return 'back_to_main'
            
            if event == 'Start Practice':
                selected_topic = None
                for key, value in values.items():
                    if key.startswith('-') and key.endswith('-') and value:
                        selected_topic = key[1:-1]
                        break
                
                if selected_topic:
                    topic_questions = [(q_id, q_data) for q_id, q_data in self.questions.items() 
                                     if q_data['topic'] == selected_topic]
                    random.shuffle(topic_questions)
                    
                    for question_num, (question_id, question_data) in enumerate(topic_questions, 1):
                        correct_answer, _ = generate_question(question_id)
                        continue_practice = self.show_question(question_num, question_id, question_data, correct_answer)
                        
                        if not continue_practice:
                            self.window.close()
                            return 'closed'
                else:
                    self.window['-ERROR-'].update('Please select a topic')
        
        self.window.close()
        return None

if __name__ == "__main__":
    app = PracticeMode("test_user")
    selected_topic = app.run()
    if selected_topic:
        print(f"Selected topic: {selected_topic}") 