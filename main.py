from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_binary
import click

@click.command()
@click.argument('url')
@click.argument('password')
@click.option('--name', help='login user name', default='gather observer')
def cmd(url, password, name):
    driver = setup_driver()
    # 画面に遷移
    driver.get(url)

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

    members_text_el = driver.find_element(By.XPATH, '//span[contains(text(),"MEMBERS -")]')
    guests_text_el = driver.find_element(By.XPATH, '//span[contains(text(),"GUESTS -")]')

    print(members_text_el.text)
    print(guests_text_el.text)

    members_el = members_text_el.find_element_by_xpath('../..')
    guests_el = guests_text_el.find_element_by_xpath('../..')

    print(members_el)
    print('------------------')
    print(members_el.text)
    print('------------------')
    print(guests_el)
    print('------------------')
    print(guests_el.text)

    # ブラウザーを終了
    driver.quit()

def setup_driver():
    options = Options()
    # options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    # options.add_argument('--headless')
    # ブラウザーを起動
    driver = webdriver.Chrome(options=options)
    return driver

if __name__ == '__main__':
    cmd()