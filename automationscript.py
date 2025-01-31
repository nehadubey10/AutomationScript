from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from selenium.webdriver.support.ui import Select
import re
from datetime import datetime


excel_file = "/home/externlabs/extern_projects/seleniumautomate/userinformation.xlsx"  # Path to your Excel file
data = pd.read_excel(excel_file)
data = data.dropna(how="all")
data.columns = data.columns.str.strip().str.lower()
data = data.reset_index(drop=True)  
MAX_RETRIES= 5 


if "date" in data.columns:
    if not pd.isna(data.loc[0, "date"]):
        currentdate = data.loc[0, "date"]
        currentdate = str(currentdate).split(" ")[0]
    else:
        currentdate= '2025-06-11'
else:
    currentdate= '2025-06-11'
    
if "shift2" in data.columns:
    if not pd.isna(data.loc[0, "shift2"]):
        shift2_value = data.loc[0, "shift2"]
    else:
        shift2_value = ""
else:
    shift2_value = ""
    
SHIFT_FILE = "shift_status.txt"
def save_shift_num(value):
    """Save shift_num to file"""
    with open(SHIFT_FILE, "w") as f:
        f.write(str(value))

def load_shift_num():
    """Load shift_num from file"""
    try:
        with open(SHIFT_FILE, "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0  
shift_num = load_shift_num()

def check_available_seat_zone(driver , zone, ):
        zone_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(),'{zone}')]"))  # Adjust XPath for date cells
        )
        zone_button.click()
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Next']"))  # Adjust XPath for date cells
        )
        next_button.click()
        seat_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/div/div/div[3]/div/div[1]/button/div[2]"))
        )
        match = re.search(r'Available Seats\s*:\s*(\d+)', seat_div.text)
        available_seats = int(match.group(1))
        return available_seats
        
def start_process():
    # Step 1: Set up Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    global shift_num  
    try:
        # Step 2: Open a website
        driver.get("https://obms-tourist.rajasthan.gov.in/")  
        driver.maximize_window()
        print("Website opened successfully.")

        ##login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="mobile-menu-2"]/div[3]/ul/li[5]/button'))
        )
        login_button.click()

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="Login-with"]/div[2]/button[2]'))
        )
        login_button.click()

        # Step 3: Locate the email input field and enter the email
        email_field = driver.find_element(By.XPATH, '//*[@id="Login-with"]/form/div[3]/div/div/input')  # Adjust XPath as needed
        email_field.send_keys("neha56@yopmail.com")  # Replace with your email
        print("Email entered.")

        # Step 4: Locate the Submit button and click it
        get_otp_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="Login-with"]/form/div[4]/button'))
        )
        get_otp_button.click()

        # Step 5: Pause for human intervention to enter OTP
        input("Please enter the OTP manually and press Enter to continue...")

        explore_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='header-link active']"))
        )
        actions = ActionChains(driver)
        # Step 5: Perform the hover action
        actions.move_to_element(explore_button).perform()

        time.sleep(2)  # Adjust based on the delay observed
        
            # Step 6: Wait for the anchor tags to appear
        anchor_tags = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="mobile-menu-2"]/div[3]/ul/li[1]/div/div/div/div[2]/div/div/div/div[2]'))  # Adjust XPath for anchor tags
        )

        specific_anchor = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="mobile-menu-2"]/div[3]/ul/li[1]/div/div/div/div[2]/div/div/div/div[2]/a[1]'))
        )
        specific_anchor.click()

        book_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space()='Book Now'])[1]"))
        )
        book_now_button.click()


        click_to_proceed_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[3]/div/div/div[3]/div/button'))
        )
        click_to_proceed_button.click()


        click_to_proceed_second_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[3]/div/div/div[3]/div/button'))
        )
        click_to_proceed_second_button.click()

        date_obj = datetime.strptime(str(currentdate), "%Y-%m-%d")
        month_name = date_obj.strftime("%B") 
        month_name = month_name.capitalize() 
        day = date_obj.day
        
        while True:
            # Locate the current displayed month and year
            current_month_year = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div").text  
            if month_name in current_month_year and "2025" in current_month_year:  # Adjust comparison logic
                break


            # Click the "Next" button to navigate to the next month
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div/div[1]/div[2]/button[2]"))  # Adjust XPath for the "Next" button
            )
            next_button.click()
            time.sleep(1)  

        specific_date = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[normalize-space()={str(day)}]"))  # Adjust XPath for date cells
        )
        # //button[normalize-space()='1']
        specific_date.click()

        
        ok_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div/div[2]/div/div/div[3]/button[2]"))  # Adjust XPath for date cells
        )
        ok_button.click()
        

        advance_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Advance']"))  # Adjust XPath for date cells
        )
        advance_button.click()
    
        
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Next']"))  # Adjust XPath for date cells
        )
        next_button.click()
        if shift_num == 0:
            shift_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[normalize-space()='Morning Shift']"))  # Adjust XPath for date cells
            )
            shift_button.click()
        else :
            shift_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[normalize-space()='Evening Shift']"))  # Adjust XPath for date cells
            )
            shift_button.click() 
        
        
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Next']"))  # Adjust XPath for date cells
        )
        next_button.click()
        if shift_num == 0:
            available_seats = check_available_seat_zone(driver,"Zone 2")
        else:
            available_seats = check_available_seat_zone(driver,"Zone 3")

        if available_seats > 0:
            vehicle_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[normalize-space()='Gypsy']"))  # Adjust XPath for date cells
            )
            vehicle_button.click()
        else:
            back_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Back']"))  # Adjust XPath for date cells
                )
            back_button.click()
            if shift_num == 0:
                available_seats = check_available_seat_zone(driver,"Zone 3")
            else:
                available_seats = check_available_seat_zone(driver,"Zone 2")

            if available_seats > 0:
                vehicle_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[normalize-space()='Gypsy']"))  # Adjust XPath for date cells
                )
                vehicle_button.click()
            else:
                print("No seats available")
                

        
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Next']"))  # Adjust XPath for date cells
        )
        next_button.click()

        wait = WebDriverWait(driver, 10)
        
        ##filling info
        # Step 3: Loop through each row in the Excel file
        for index, row in data.iterrows():
            
            tourist_type_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div/div/div/div[1]/div[2]/form/div[1]/div/div/div/div/div/div"))
            )
            tourist_type_input.click()
 
            if str(row["type"]).lower().strip() == "indian":
                tourist_type_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/ul/li[1]'))
                )
                tourist_type_input.click()
            else:
                tourist_type_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/ul/li[2]'))
                )
                tourist_type_input.click()

            time.sleep(2)
            name_field = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div/div/div/div[1]/div[2]/form/div[2]/div[1]/div[1]/div/div/input")))
            name_field.send_keys(row['fullname'])

            # Fill in the "Email" field
            if index == 0:
                mobile_field = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div/div/div/div[1]/div[2]/form/div[2]/div[1]/div[2]/div/div/input")))
                mobile_field.send_keys("7014232300")

            identity_proof_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div/div/div/div[1]/div[2]/form/div[2]/div[1]/div[3]/div"))
            )
            identity_proof_input.click()
            identity_map = {
                "ad": "//li[normalize-space()='Aadhar']",
                "dl": "//li[normalize-space()='Driving License']",
                "pss": "//li[normalize-space()='Passport']",
                "vi": "//li[normalize-space()='Voter Id']",
                "pc": "//li[normalize-space()='Pan Card']",
                "oi": "//li[normalize-space()='Office ID']",
                "si": "//li[normalize-space()='Student Id']",  # Changed key to avoid duplicate "oi"
            }

            identity_key = str(row["identiy"]).lower().strip()
            identity_xpath = identity_map.get(identity_key)

            if identity_xpath:
                identity_proof_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, identity_xpath))
                )
                identity_proof_input.click()
                
            identity_no_field = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div/div/div/div[1]/div[2]/form/div[2]/div[1]/div[5]/div/div/input")))
            identity_no_field.send_keys(row["identityno"])
            
            
            gender_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div/div/div/div[1]/div[2]/form/div[2]/div[1]/div[7]/div/div/div/div/div"))
            )
            gender_input.click()

            gender_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/ul/li[1]'))
            )
            gender_input.click()

            # Step 4: Allow human intervention for file upload on the first iteration
            if index == 0:
                print("Please upload the file manually and press Enter to continue...")
                input()
            time.sleep(5)
            # Step 5: Submit the form (or move to the next step in your form)
            add_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div/div/div/div[1]/div[2]/form/div[2]/div[3]/button[1]"))  # Adjust XPath for date cells
            )
            add_button.click()

            # Optional: Wait for the form to reset or navigate to the next form
            time.sleep(15)
            
        time.sleep(5)
        term_condition_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div/div/div/div[2]/div[5]/input"))  # Adjust XPath for date cells
            )
        term_condition_button.click()
        
        term_condition_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div/div/div/div[2]/div[6]/input"))  # Adjust XPath for date cells
            )
        term_condition_button.click()
        
        div_element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div[3]/div/div/div/div/div[2]/div[7]/div')))  # Adjust the XPath to match your div
        # Get the text from the div
        div_text = div_element.text

        captcha_field = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div/div/div/div[2]/input")))
        captcha_field.send_keys(div_text)
        
        make_payment_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div/div/div/div[2]/div[9]/button"))  # Adjust XPath for date cells
            )
        make_payment_button.click()
        
        
        confrim_payment_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div/div[2]/button[2]"))  # Adjust XPath for date cells
            )
        confrim_payment_button.click()

        # input()
        if shift2_value.lower() == "pm":
            user_input = input("Enter shift preference (eve/morning/end to quit): ").strip().lower()
            if user_input == "eve":
                print("Restarting script with Evening Shift...")
                driver.quit()  
                time.sleep(2)  
                # Restart script with "Evening Shift"
                shift_num = 1
                save_shift_num(shift_num) 
                exec(open("automationticketbookingscript.py").read()) 
        element = driver.find_element(By.TAG_NAME, "h6")

    except Exception as e:
        print(f"Error occurred: {e}")
        user_input = input("Enter shift preference (eve/morning/end to quit): ").strip().lower()
        if  user_input == "end":               
            shift_num = 0
            save_shift_num(shift_num)  
            
        driver.quit()
        raise e  # Raising an exception to trigger the retry mechanism

    finally:
        user_input = input("Enter shift preference (eve/morning/end to quit): ").strip().lower()
        if  user_input == "end":               
            shift_num = 0
            save_shift_num(shift_num)  
            
        driver.quit()
        
# Retry mechanism
attempt = 0
while attempt < MAX_RETRIES:
    try:
        start_process()
        break  
    except Exception as e:
        attempt += 1
        print(f"Retrying... Attempt {attempt} of {MAX_RETRIES}")

if attempt == MAX_RETRIES:
    print("Max retries reached. Exiting.")
