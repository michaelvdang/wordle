from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

driver.get("localhost:5173/wordle")

title = driver.title

print(title)


driver.implicitly_wait(0.5)

username = driver.find_element(by=By.ID, value="username")
username.send_keys("ucohen")

driver.implicitly_wait(0.5)

main_content = driver.find_element(by=By.ID, value="mainId")
main_content.send_keys("house")
main_content.send_keys(Keys.ENTER)
driver.implicitly_wait(0.5)
main_content = driver.find_element(by=By.ID, value="mainId")
main_content.send_keys("blimp")
main_content.send_keys(Keys.ENTER)
driver.implicitly_wait(0.5)
main_content = driver.find_element(by=By.ID, value="mainId")
main_content.send_keys("paint")
main_content.send_keys(Keys.ENTER)
driver.implicitly_wait(0.5)
main_content = driver.find_element(by=By.ID, value="mainId")
main_content.send_keys("flies")
main_content.send_keys(Keys.ENTER)
driver.implicitly_wait(0.5)
main_content = driver.find_element(by=By.ID, value="mainId")
main_content.send_keys("yours")
main_content.send_keys(Keys.ENTER)
driver.implicitly_wait(0.5)
main_content = driver.find_element(by=By.ID, value="mainId")
main_content.send_keys("grand")
main_content.send_keys(Keys.ENTER)
driver.implicitly_wait(0.5)

correct_answer = driver.find_element(by=By.ID, value="correct_answer")
play_new_game_button = driver.find_element(by=By.ID, value="play_new_game_button")
cancel_new_game_button = driver.find_element(by=By.ID, value="cancel_new_game_button")



# submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
# submit_button.click()

# message = driver.find_element(by=By.ID, value="message")
# text = message.text

driver.quit()