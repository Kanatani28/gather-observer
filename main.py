from selenium import webdriver
from selenium.webdriver.common.by import By
import click
from get_chrome_driver import GetChromeDriver
from pyvirtualdisplay import Display
import re

from discord.client import DiscordClient

CONST_MEMBERS = "MEMBERS - "
CONST_GUESTS = "GUESTS - "

@click.command()
@click.argument('url')
@click.argument('password')
@click.argument('discord_secret')
@click.argument('discord_channel_id')
@click.option('--name', help='login user name', default='gather observer')
def cmd(url, password, discord_secret, discord_channel_id, name):
    setup_display()
    driver = setup_driver()
    
    # 画面に遷移
    driver.get(url)
    driver.execute_script("Object.defineProperty(document, 'visibilityState', {value: 'visible', writable: true});")
    driver.execute_script("Object.defineProperty(document, 'hidden', {value: false, writable: true});")
    driver.execute_script('document.dispatchEvent(new Event("visibilitychange"));')

    driver.implicitly_wait(30)
   
    # パスワード入力
    driver.find_element(By.CSS_SELECTOR, 'input[type="password"]').send_keys(password)
    driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

    # キャラメイク
    driver.find_element(By.XPATH, '//button[text()="Next Step"]').click()

    # 名前入力
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter your name"]').send_keys(name)
    driver.find_element(By.XPATH, '//button[text()="Finish"]').click()

    # Join
    driver.find_element(By.XPATH, '//button[text()="Join the Gathering"]').click()

    try:
        # チュートリアル画面に飛ばされることがあるのでその時はスキップ
        driver.find_element(By.XPATH, '//button[text()="Skip Tutorial"]').click()
        print('tutorial skipped')
    except:
        print('no tutorial')
    
    # 部屋に入った時の状態確認用にキャプチャを取得する
    driver.save_screenshot('screenshot.png')

    members_text_el = driver.find_element(By.XPATH, f'//span[contains(text(),"{CONST_MEMBERS}")]')
    guests_text_el = driver.find_element(By.XPATH, f'//span[contains(text(),"{CONST_GUESTS}")]')
    
    print(members_text_el.text)
    print(guests_text_el.text)
    
    members_count = int(members_text_el.text.split(CONST_MEMBERS)[-1])
    # Bot自身がカウントに入ってしまうので -1 する
    guests_count = int(guests_text_el.text.split(CONST_GUESTS)[-1]) - 1

    match (members_count, guests_count):
        case (1, 0) | (0, 1):
            members_el = members_text_el.find_element_by_xpath('../..')
            guests_el = guests_text_el.find_element_by_xpath('../..')

            notification_user_name = ""
            if members_count == 1:
                print(members_el)
                print('------------------')
                print(members_el.text)

                
                members = members_el.text.split('\n')
                # minutesと CONST_MEMBERS 文字列 を削除する
                filtered = filter(lambda member: (not CONST_MEMBERS in member) and (not re.fullmatch(r'^\d+m$', member)), members)
                notification_user_name = list(filtered)[-1]
                print(members)


            if guests_count == 1:            
                print(guests_el)
                print('------------------')
                print(guests_el.text)

                guests = guests_el.text.split('\n')
                # minutesと CONST_GUESTS 文字列 と このBotのユーザー名 を削除する
                filtered = filter(lambda guest: (not CONST_GUESTS in guest) and (not re.fullmatch(r'^\d+m$', guest)) and (not name == guest), guests)
                notification_user_name = list(filtered)[-1]
                print(guests)

            
            discord_client = DiscordClient(discord_secret, discord_channel_id)
            embeds = [{
                "title": "Gatherに集まる",
                "description": f"{notification_user_name}さんが居るみたい！Gatherに入って会いに行こう！",
                "color": 0x00ff00,
                "url": url,
                "image": {
                    "url": "https://user-images.githubusercontent.com/16130443/154839020-cbe6d843-f957-4013-81d9-7e62b74cadaa.png"
                }
            }]
            discord_client.send_message({ "embeds": embeds })
    


    # ブラウザーを終了
    driver.quit()



def setup_display():
    display = Display(visible=0, size=(800, 600))
    display.start()

def setup_driver():
    get_driver = GetChromeDriver()
    get_driver.install()

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--lang=ja-JP')
    options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36') 
    # ブラウザーを起動
    driver = webdriver.Chrome(options=options)
    return driver    

if __name__ == '__main__':
    cmd()
