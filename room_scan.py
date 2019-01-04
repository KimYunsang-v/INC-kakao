from selenium import webdriver
import mysql1 as sql
from selenium.webdriver.common.keys import Keys
import pandas,time
import requests
import upload_file

def room_scan(room, driver):
    driver.switch_to_window(driver.window_handles[1])
    # 상담자
    nickName = driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[1]/div[1]/div/div/strong').text
    nickName = nickName.split('\n')[1]

    # 담당자
    chat_manager = driver.find_element_by_class_name('tit_profile').text

    # 스크롤 올리는 while문 현재는 10번만 올림
    scroll_count = 10
    while scroll_count > 0:  # 50번 반복
        time.sleep(0.2)
        element = driver.find_element_by_tag_name('body')
        element.click()
        element.send_keys(Keys.HOME)  # home키를 누르게 하여 스크롤 올림
        scroll_count -= 1
        if len(driver.window_handles) == 3:
            print('window=====' + str(1) + 'handles======' + str(len(driver.window_handles)))
            driver.switch_to_window(driver.window_handles[2])
            driver.close()
            #window = len(driver.window_handles)
            driver.switch_to_window(driver.window_handles[1])
            print('num ======= ' + str(1))

    # 채팅방에서 item_chat 가져오기
    chats = driver.find_elements_by_class_name('item_chat')
    chat_date = driver.find_element_by_class_name('bg_line').text.split(' ')[0]

    chat_time = ""
    # chatlogs json -> data로 변환
    for chat in chats:

        if (chat_date != driver.find_element_by_class_name('bg_line').text.split(' ')[0]):
            chat_date = driver.find_element_by_class_name('bg_line').text.split(' ')[0]

        print(nickName)  # 닉네임 출력
        chat_msg = ''
        try:
            # 메세지 가져오기
            chat_msg = chat.find_element_by_class_name('set_chat').text
            print(chat_msg)  # 메시지 출력
        except:
            pass

        img_url = ''
        #이미지 태그가 있는지 없는지 확인하는 try/except문
        try:
            print(chat.find_element_by_class_name('link_pic').get_attribute('href'))
            img_url = chat.find_element_by_class_name('link_pic').get_attribute('href')
            filename = img_url.split('/')[-1]
            r = requests.get(img_url, allow_redirects=True)
            open(filename, 'wb').write(r.content)
            img_url = upload_file.saveImage(filename)
        except Exception :
            pass

        # 시간 태그가 있는지 없는지 확인하는 try/except문
        try:
            chat_time = chat.find_element_by_class_name('txt_time').text
        except Exception :
            pass


        print(chat_time)
        print('=========================')
        # 디비 저장 : nickname,날짜,시간,담당자, 메세지, 첨부url
        sql.save_msg(nickName, chat_date, chat_time, chat_manager, chat_msg, img_url)
    driver.close()
    return driver
