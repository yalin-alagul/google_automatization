import time
import os
import subprocess
import pyautogui
import openai
import random
from dotenv import load_dotenv
from interactive_rating_generator import InteractiveRatingGenerator 

load_dotenv()

# Configuration from environment variables
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
CHATBOT_MAX_TOKENS_PER_REQUEST = int(os.environ.get('CHATBOT_MAX_TOKENS_PER_REQUEST'))
CHATBOT_MODEL = os.environ.get('CHATBOT_MODEL')
CHATBOT_TEMPERATURE = float(os.environ.get('CHATBOT_TEMPERATURE'))


openai.api_key = OPENAI_API_KEY

def generate_review():
    response = openai.ChatCompletion.create(
        model=CHATBOT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates positive hotel reviews."},
            {"role": "user", "content": "Generate a positive review for Residence Inn Istanbul Atasehir. Make it sound natural and include specific details about the hotel experience. Keep it under 80 words."}
        ],
        max_tokens=CHATBOT_MAX_TOKENS_PER_REQUEST,
        temperature=CHATBOT_TEMPERATURE
    )
    print("OpenAI response:", response)
    return response['choices'][0]['message']['content'].strip()

def generate_review_rooms():
    response = openai.ChatCompletion.create(
        model=CHATBOT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates positive hotel reviews."},
            {"role": "user", "content": "Generate a positive review for the rooms at Residence Inn Istanbul Atasehir. Make it sound natural and include specific details about the room experience. Keep it under 80 words."}
        ],
        max_tokens=CHATBOT_MAX_TOKENS_PER_REQUEST,
        temperature=CHATBOT_TEMPERATURE
    )
    print("OpenAI response:", response)
    return response['choices'][0]['message']['content'].strip()

def generate_review_nearby_activities():
    response = openai.ChatCompletion.create(
        model=CHATBOT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates positive hotel reviews."},
            {"role": "user", "content": "Generate a positive review for the nearby activities at Residence Inn Istanbul Atasehir. Make it sound natural and include specific details about the activities. Keep it under 80 words."}
        ],
        max_tokens=CHATBOT_MAX_TOKENS_PER_REQUEST,
        temperature=CHATBOT_TEMPERATURE
    )
    print("OpenAI response:", response)
    return response['choices'][0]['message']['content'].strip()

def generate_review_safety():
    response = openai.ChatCompletion.create(
        model=CHATBOT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates positive hotel reviews."},
            {"role": "user", "content": "Generate a positive review for the safety measures at Residence Inn Istanbul Atasehir. Make it sound natural and include specific details about the safety features. Keep it under 80 words."}
        ],
        max_tokens=CHATBOT_MAX_TOKENS_PER_REQUEST,
        temperature=CHATBOT_TEMPERATURE
    )
    print("OpenAI response:", response)
    return response['choices'][0]['message']['content'].strip()

def generate_review_walkability():
    response = openai.ChatCompletion.create(
        model=CHATBOT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates positive hotel reviews."},
            {"role": "user", "content": "Generate a positive review for the walkability around Residence Inn Istanbul Atasehir. Make it sound natural and include specific details about the area. Keep it under 80 words."}
        ],
        max_tokens=CHATBOT_MAX_TOKENS_PER_REQUEST,
        temperature=CHATBOT_TEMPERATURE
    )
    print("OpenAI response:", response)
    return response['choices'][0]['message']['content'].strip()

def generate_review_drinks_and_food():
    response = openai.ChatCompletion.create(
        model=CHATBOT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates positive hotel reviews."},
            {"role": "user", "content": "Generate a positive review for the drinks and food at Residence Inn Istanbul Atasehir. Make it sound natural and include specific details about the dining experience. Keep it under 80 words."}
        ],
        max_tokens=CHATBOT_MAX_TOKENS_PER_REQUEST,
        temperature=CHATBOT_TEMPERATURE
    )
    print("OpenAI response:", response)
    return response['choices'][0]['message']['content'].strip()

def generate_review_noteworthy_details():
    response = openai.ChatCompletion.create(
        model=CHATBOT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates positive hotel reviews."},
            {"role": "user", "content": "Generate a positive review for the noteworthy details at Residence Inn Istanbul Atasehir. Make it sound natural and include specific details about the hotel experience. Keep it under 80 words."}
        ],
        max_tokens=CHATBOT_MAX_TOKENS_PER_REQUEST,
        temperature=CHATBOT_TEMPERATURE
    )
    print("OpenAI response:", response)
    return response['choices'][0]['message']['content'].strip()

def open_chrome_and_navigate():
    url = "https://www.google.com/maps/place/Residence+Inn+Istanbul+Atasehir/@40.9752683,29.1505552,642m/data=!3m1!1e3!4m24!1m12!3m11!1s0x14cac5257aca9e61:0x6a0b4e4e6f2b380c!2sResidence+Inn+Istanbul+Atasehir!5m2!4m1!1i2!8m2!3d40.9753169!4d29.150528!9m1!1b1!16s%2Fg%2F11mqlvm6b_!3m10!1s0x14cac5257aca9e61:0x6a0b4e4e6f2b380c!5m2!4m1!1i2!8m2!3d40.9753169!4d29.150528!9m1!1b1!16s%2Fg%2F11mqlvm6b_!5m1!1e2?entry=ttu&g_ep=EgoyMDI1MDcyOC4wIKXMDSoASAFQAw%3D%3D"
    # Initialize the rating generator   
    rating_generator = InteractiveRatingGenerator("ratings_data.json")
    rnd_overall = rating_generator.generate_rating()
    print(f"Generated rating for tab presses: {rnd_overall}")
    subprocess.Popen(f'start chrome "{url}"', shell=True)

    if rnd_overall == 5:
        def weighted_room_rating():
            import random
            return 5 if random.random() < 0.9 else 4
        rnd_room = weighted_room_rating()
        def weighted_service_rating():
            import random
            return 5 if random.random() < 0.9 else 4
        rnd_service = weighted_service_rating()
        def weighted_location_rating():
            import random
            return 5 if random.random() < 0.9 else 4
        rnd_location = weighted_location_rating()

    elif rnd_overall == 4:
        def weighted_room_rating():
            import random
            return 4 if random.random() < 0.8 else 3
        rnd_room = weighted_room_rating()
        def weighted_service_rating():
            import random
            return 4 if random.random() < 0.8 else 3
        rnd_service = weighted_service_rating()
        def weighted_location_rating():
            import random
            return 4 if random.random() < 0.8 else 3
        rnd_location = weighted_location_rating()

    elif rnd_overall == 3:
        def weighted_room_rating():
            import random
            return 3 if random.random() < 0.7 else 2
        rnd_room = weighted_room_rating()
        def weighted_service_rating():
            import random
            return 3 if random.random() < 0.7 else 2
        rnd_service = weighted_service_rating()
        def weighted_location_rating():
            import random
            return 3 if random.random() < 0.7 else 2
        rnd_location = weighted_location_rating()

    elif rnd_overall == 2:
        def weighted_room_rating():
            import random
            return 2 if random.random() < 0.7 else 1
        rnd_room = weighted_room_rating()
        def weighted_service_rating():
            import random
            return 2 if random.random() < 0.7 else 1
        rnd_service = weighted_service_rating()
        def weighted_location_rating():
            import random
            return 2 if random.random() < 0.7 else 1
        rnd_location = weighted_location_rating()

    elif rnd_overall == 1:
        def weighted_room_rating():
            import random
            return 1 if random.random() < 0.7 else 2    
        rnd_room = weighted_room_rating()
        def weighted_service_rating():
            import random
            return 1 if random.random() < 0.7 else 2
        rnd_service = weighted_service_rating()
        def weighted_location_rating():
            import random
            return 1 if random.random() < 0.7 else 2
        rnd_location = weighted_location_rating()

    time.sleep(2.5)
    pyautogui.press('esc')
    time.sleep(1)
    pyautogui.press('tab', presses=3)
    pyautogui.press('enter')
    time.sleep(1.5)
    pyautogui.press('esc')
    pyautogui.press('tab', presses=1 + rnd_overall)
    pyautogui.press('enter')
    pyautogui.press('tab', presses=5 - rnd_overall)
    
    # Generate random number to determine which enters to execute
    rand_choice = random.random()

    # Determine which enters to execute based on percentages
    execute_room_enter = False
    execute_service_enter = False
    execute_location_enter = False

    if rand_choice <= 0.6:  # 60% - execute all enters
        execute_room_enter = True
        execute_service_enter = True
        execute_location_enter = True
    elif rand_choice <= 0.7:  # 10% - execute room and service enters only
        execute_room_enter = True
        execute_service_enter = True
    elif rand_choice <= 0.77:  # 7% - execute room and location enters only
        execute_room_enter = True
        execute_location_enter = True
    elif rand_choice <= 0.8:  # 3% - execute service and location enters only
        execute_service_enter = True
        execute_location_enter = True
    # else: 20% - execute no enters (all remain False)

    # Execute the code with conditional enters
    pyautogui.press('tab', presses=rnd_room)
    if execute_room_enter:
        pyautogui.press('enter')
    pyautogui.press('tab', presses=5 - rnd_room)

    pyautogui.press('tab', presses=rnd_service)
    if execute_service_enter:
        pyautogui.press('enter')
    pyautogui.press('tab', presses=5 - rnd_service)

    pyautogui.press('tab', presses=rnd_location)
    if execute_location_enter:
        pyautogui.press('enter')
    pyautogui.press('tab', presses=5 - rnd_location)
    
    pyautogui.press('tab')
    review_text = generate_review()
    pyautogui.write(review_text)
    pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.press('tab')
    review_text_rooms = generate_review_rooms()
    pyautogui.write(review_text_rooms)
    pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.press('tab')
    review_text_nearby = generate_review_nearby_activities()
    pyautogui.write(review_text_nearby)
    pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.press('tab')
    review_text_safety = generate_review_safety()
    pyautogui.write(review_text_safety)
    pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.press('tab')
    review_text_walkability = generate_review_walkability()
    pyautogui.write(review_text_walkability)
    pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.press('tab')
    review_text_drinks_and_food = generate_review_drinks_and_food()
    pyautogui.write(review_text_drinks_and_food)
    pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.press('tab')
    review_text_noteworthy = generate_review_noteworthy_details()
    pyautogui.write(review_text_noteworthy)
    pyautogui.press('tab')
    pyautogui.press('tab')
    
if __name__ == "__main__":
    open_chrome_and_navigate()