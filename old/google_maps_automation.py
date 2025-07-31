import time
import os
import subprocess
import pyautogui
import openai
from dotenv import load_dotenv

load_dotenv()

class GoogleMapsReviewAutomation:
    def __init__(self):
        self.setup_openai()
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.3
    
    def setup_openai(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
    
    def generate_review(self):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4.1-nano -preview",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates positive hotel reviews."},
                    {"role": "user", "content": "Generate a positive review for Residence Inn Istanbul Atasehir. Make it sound natural and include specific details about the hotel experience. Keep it around 100-150 words."}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating review: {e}")
            return "Great hotel with excellent service and comfortable rooms. The location is perfect and the staff is very friendly. Highly recommended!"
    
    def open_chrome_and_navigate(self):
        url = "https://www.google.com/maps/place/Residence+Inn+Istanbul+Atasehir/@40.9752683,29.1505552,642m/data=!3m1!1e3!4m22!1m12!3m11!1s0x14cac5257aca9e61:0x6a0b4e4e6f2b380c!2sResidence+Inn+Istanbul+Atasehir!5m2!4m1!1i2!8m2!3d40.9753169!4d29.150528!9m1!1b1!16s%2Fg%2F11mqlvm6b_!3m8!1s0x14cac5257aca9e61:0x6a0b4e4e6f2b380c!5m2!4m1!1i2!8m2!3d40.9753169!4d29.150528!16s%2Fg%2F11mqlvm6b_?entry=ttu&g_ep=EgoyMDI1MDcyOC4wIKXMDSoASAFQAw%3D%3D     "
        
        subprocess.Popen(f'start chrome "{url}"', shell=True)
        time.sleep(5)
    
    def send_tab(self, count=1):
        for _ in range(count):
            pyautogui.press('tab')
    
    def send_key(self, key):
        pyautogui.press(key)
    
    def send_arrow_right(self, count=1):
        for _ in range(count):
            pyautogui.press('right')
    
    def type_text(self, text):
        pyautogui.write(text)
        
    def run_automation(self):
        
        # Open Chrome and navigate to Google Maps
        print("Opening Chrome and navigating to Google Maps...")
        self.open_chrome_and_navigate()
        
        # Step 1: 58 tab till write review
        print("Step 1: Navigating to write review button (59 tabs)...")
        self.send_tab(58)
        
        # Step 2: 1 esc press to get rid of info
        print("Step 2: Pressing ESC to dismiss info...")
        self.send_key('escape')
        
        # Step 3: 6 tab to 5 star the overall points
        print("Step 3: Setting 5 stars for overall rating (6 tabs)...")
        self.send_tab(6)
        
        # Step 4: 5 tab to rooms
        print("Step 4: Setting 5 stars for rooms (5 tabs)...")
        self.send_tab(5)
        
        # Step 5: 5 tab to service
        print("Step 5: Setting 5 stars for service (5 tabs)...")
        self.send_tab(5)
        
        # Step 6: 5 tab to location
        print("Step 6: Setting 5 stars for location (5 tabs)...")
        self.send_tab(5)
        
        # Step 7: 1 tab to write the review
        print("Step 7: Writing the review (1 tab)...")
        self.send_tab(1)
        review_text = self.generate_review()
        self.type_text(review_text)
        time.sleep(1)
        
        # Step 8: 1 tab to answer business right arrow key to answer Vacation
        print("Step 8: Selecting 'Vacation' for trip type (1 tab + 1 right arrow)...")
        self.send_tab(1)
        self.send_arrow_right(1)
        
        # Step 9: 1 tab to answer "Who did you travel with?" - selecting Family
        print("Step 9: Selecting 'Family' for travel companion (1 tab + 1 right arrow)...")
        self.send_tab(1)
        self.send_arrow_right(1)
        
        # Step 10: 1 tab to answer "How would you describe the hotel?" - selecting Luxury
        print("Step 10: Selecting 'Luxury' for hotel description (1 tab + 1 right arrow)...")
        self.send_tab(1)  
        self.send_arrow_right(1)
        
        # Step 11: 1 tab + enter + tab to tell more about "Rooms"
        print("Step 11: Adding details about Rooms (1 tab + enter + 1 tab)...")
        self.send_tab(1)
        self.send_key('enter')
        self.send_tab(1)
        
        # Step 12: 1 tab + enter + tab to tell more about "Nearby Activities"
        print("Step 12: Adding details about Nearby Activities (1 tab + enter + 1 tab)...")
        self.send_tab(1)
        self.send_key('enter')
        self.send_tab(1)
        
        # Step 13: 1 tab + enter + tab to tell more about "Safety"
        print("Step 13: Adding details about Safety (1 tab + enter + 1 tab)...")
        self.send_tab(1)
        self.send_key('enter')
        self.send_tab(1)
        
        # Step 14: 1 tab + enter + tab to tell more about "Walkability"
        print("Step 14: Adding details about Walkability (1 tab + enter + 1 tab)...")
        self.send_tab(1)
        self.send_key('enter')
        self.send_tab(1)
        
        # Step 15: 1 tab + enter + tab to tell more about "Food & Drinks"
        print("Step 15: Adding details about Food & Drinks (1 tab + enter + 1 tab)...")
        self.send_tab(1)
        self.send_key('enter')
        self.send_tab(1)
        
        # Step 16: 1 tab + enter + tab to tell more about "Noteworthy Details"
        print("Step 16: Adding details about Noteworthy Details (1 tab + enter + 1 tab)...")
        self.send_tab(1)
        self.send_key('enter')
        self.send_tab(1)
        
        # Step 17: 2 tab + enter to submit
        print("Step 17: Submitting the review (2 tabs + enter)...")
        self.send_tab(2)
        self.send_key('enter')
        
        print("Review automation completed!")
        print("Note: Move your mouse to the top-left corner to stop the script if needed (failsafe).")

if __name__ == "__main__":
    automation = GoogleMapsReviewAutomation()
    automation.run_automation()