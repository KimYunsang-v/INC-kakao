from selenium import webdriver
import room_scan
import time
from selenium.webdriver.common.keys import Keys

window = 1
driver = webdriver.Chrome('C:/chromedriver')

# 웹 자원 로드를 위해 3초 대기
driver.implicitly_wait(3)

# 평생교육원 채팅방 url 호출
driver.get('https://center-pf.kakao.com/_EvRij/chats')

# 로그인하기
# 아이디/패스워드 입력하기
driver.find_element_by_id('loginEmail').send_keys('skuinc.internship@skuniv.ac.kr') #아이디 보안상 삭제함
driver.find_element_by_id('loginPw').send_keys('!@#$intern12') #비번은 보안상 삭제함

# 로그인 버튼 클릭하기
driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/button').click()

chat_room = driver.find_element_by_xpath('//*[@id="mArticle"]/div[2]/div[3]/div/div').find_element_by_tag_name('li')
#list_size = len(chat_list)
main_window = driver.window_handles[0] # 부모창

chat_items = []

count = 0
chat_count= 1

chat_room.click()
driver = room_scan.room_scan(chat_room,driver)

#driver.switch_to_window(main_window)
#chat_list_scroll = driver.find_element_by_xpath('//*[@id="mArticle"]/div[2]/div[3]/div')
#chat_list_scroll.click()
#driver.switch_to_window(driver.window_handles[1])
#driver.close()
#driver.switch_to_window(driver.window_handles[0])
#chat_list_scroll.send_keys(Keys.ARROW_DOWN)
#chat_list_scroll.send_keys(Keys.ARROW_DOWN)
driver.switch_to_window(driver.window_handles[0])
new_chat_room = driver.find_element_by_xpath('//*[@id="mArticle"]/div[2]/div[3]/div').find_elements_by_tag_name('li')

current_chat = chat_room
while True:
    new_count = 0
    test = False
    for chat in new_chat_room:
        if chat_room == chat and test is False:
            test = True
            continue
        elif chat_room != chat and test is False:
            #current_chat = chat
            continue
        else:
            current_chat = chat
            break

    if chat_room == current_chat:
        break

    print('window ====' + str(window))
#    print('current window======' + str(driver.current_window_handle))
    print('new count=======' + str(new_count))
    print(current_chat.text)
    current_chat.click()
    driver = room_scan.room_scan(current_chat, driver)
    chat_room = current_chat
    driver.switch_to_window(driver.window_handles[0])


    chat_list_scroll = driver.find_element_by_xpath('//*[@id="mArticle"]/div[2]/div[3]/div')
    chat_list_scroll.click()
    driver.switch_to_window(driver.window_handles[1])
    driver.close()
    driver.switch_to_window(driver.window_handles[0])
    if chat_count % 2 == 0:
        chat_list_scroll.send_keys(Keys.ARROW_DOWN)
        chat_list_scroll.send_keys(Keys.ARROW_DOWN)
    else:
        chat_list_scroll.send_keys(Keys.ARROW_DOWN)
    time.sleep(2)
    driver.switch_to_window(driver.window_handles[0])
    new_chat_room = driver.find_element_by_xpath('//*[@id="mArticle"]/div[2]/div[3]/div').\
        find_elements_by_tag_name('li')
    chat_count += 1
