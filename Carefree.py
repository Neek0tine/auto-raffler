import time
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

print('==============================================================================================')
print('=  ________      ________      ________  ________  ___           _______       ________      =')
print('= |\   __  \    |\   __  \    |\  _____\|\  _____\|\  \         |\  ___ \     |\   __  \     =')
print('= \ \  \|\  \   \ \  \|\  \   \ \  \__/ \ \  \__/ \ \  \        \ \   __/|    \ \  \|\  \    =')
print('=  \ \   _  _\   \ \   __  \   \ \   __\ \ \   __\ \ \  \        \ \  \_|/__   \ \   _  _\   =')
print('=   \ \  \\  \|    \ \  \ \  \   \ \  \_|  \ \  \_|  \ \  \____    \ \  \_|\ \   \ \  \\  \|   =')
print('=    \ \__\\ _\     \ \__\ \__\   \ \__\    \ \__\    \ \_______\   \ \_______\   \ \__\\ _\   =')
print('=     \|__|\|__|    \|__|\|__|    \|__|     \|__|     \|_______|    \|_______|    \|__|\|__| =')
print('=                Scrap TF Raffler                                                            =')
print('=                           by Neek0tine                                                     =')
print('==============================================================================================')

# Initialize WebDriver
options = EdgeOptions()
options.use_chromium = True
options.add_argument('user-data-dir=C:\\Users\\nicho\\AppData\\Local\\Microsoft\\Edge\\TEST')
options.add_argument('profile-directory=Profile 2')
# options.add_argument('--headless')

driver = Edge(options=options, executable_path='C:\\Users\\nicho\\Documents\\Program Data\\msedgedriver.exe')


# Web scraping available raffles
def get_data():
    raffle_count = 0
    try:
        driver.get('https://scrap.tf/raffles')
        driver.minimize_window()
        stat = driver.find_element_by_tag_name('h1').text
        stat = str(stat)
        raffle_count = stat.split('/')
        joined_count = int(raffle_count.pop(0))
        raffle_count = "".join(raffle_count)
        raffle_count = int(raffle_count)
        raffle_count = raffle_count

        if joined_count == raffle_count - 1:

            def overseer():
                print('[!] Entered all raffles! Enabling overseer mode!')
                time.sleep(20)
                driver.get('https://scrap.tf/raffles')

                while True:
                    stat1 = driver.find_element_by_tag_name('h1').text
                    stats = str(stat1)
                    print(f'[+] Raffle count : {stats}')
                    raffle_count_ov = stat.split('/')
                    if raffle_count_ov[0] > raffle_count_ov[-1]:
                        get_data()
                    else:
                        time.sleep(20)
                        driver.refresh()

            overseer()

        else:
            pass
        print(f'[+] Raffle count : {stat}')

    except:
        print('[!] Error: Failed to open site')

    links = []

    def collect_data():

        print('[+] Collecting raffles data ...')

        def pick():
            elems = driver.find_elements_by_class_name("raffle-name [href]")
            for elem in elems:
                href = elem.get_attribute('href')
                if href in links:
                    pass
                else:
                    links.append(href)

        pick()

        while len(links) < raffle_count:
            print(f'[+] Collected {len(links)} data, trying to get more ... ')
            if len(links) > raffle_count - 5:
                driver.refresh()
                pick()
                break
            else:
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                pick()
                time.sleep(1)
        print(f'[+] Collected {len(links)} raffles data!')

    collect_data()

    n = len(links)

    def enter_raffle():
        z = 1
        for link in links:
            driver.get(link)
            print(f'Entering Raffle {z} of {n} ...')
            try:
                wait = WebDriverWait(driver, 1)
                wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                                                    '#pid-viewraffle > div.container > div > div.well.raffle-well > div.row.raffle-opts-row > div.col-xs-7.enter-raffle-btns > button:nth-child(3)'))).click()
                time.sleep(2.2)
            except:
                pass
            z += 1

    enter_raffle()


get_data()
