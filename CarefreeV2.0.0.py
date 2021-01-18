import config
import os
import time
from msedge.selenium_tools import Edge, EdgeOptions

print('==============================================================================================')
print('=  ________      ________      ________  ________  ___           _______       ________      =')
print('= |\   __  \    |\   __  \    |\  _____\|\  _____\|\  \         |\  ___ \     |\   __  \     =')
print('= \ \  \|\  \   \ \  \|\  \   \ \  \__/ \ \  \__/ \ \  \        \ \   __/|    \ \  \|\  \    =')
print('=  \ \   _  _\   \ \   __  \   \ \   __\ \ \   __\ \ \  \        \ \  \_|/__   \ \   _  _\   =')
print('=   \ \  \\  \|    \ \  \ \  \   \ \  \_|  \ \  \_|  \ \  \____    \ \  \_|\ \   \ \  \\  \|   =')
print('=    \ \__\\ _\     \ \__\ \__\   \ \__\    \ \__\    \ \_______\   \ \_______\   \ \__\\ _\   =')
print('=     \|__|\|__|    \|__|\|__|    \|__|     \|__|     \|_______|    \|_______|    \|__|\|__| =')
print('=                Scrap TF Raffler       V2.0                                                 =')
print('=                           by Neek0tine                                                     =')
print('==============================================================================================')

tolerance = config.tolerance
delay = config.delay
headless = config.headless
chk_frq = config.chk_frq


def initialize():  # Initialize the webdriver engine
    options = EdgeOptions()
    options.use_chromium = True
    if headless is False:
        pass
    else:
        options.add_argument(argument='--headless')

    def get_profile():
        try:
            pass
        except FileNotFoundError:
            os.mkdir('C:\\Users\\nicho\\AppData\\Local\\Microsoft\\Edge\\Auto-raffler')

        if 'Auto-raffler' in os.listdir('C:\\Users\\nicho\\AppData\\Local\\Microsoft\\Edge'):
            options.add_argument('user-data-dir=C:\\Users\\nicho\\AppData\\Local\\Microsoft\\Edge\\Auto-raffler')
            options.add_argument('profile-directory=Profile 1')
        else:
            os.mkdir('C:\\Users\\nicho\\AppData\\Local\\Microsoft\\Edge\\Auto-raffler')
            get_profile()

    get_profile()

    driver = Edge(options=options, executable_path='C:\\Users\\nicho\\Documents\\Program Data\\msedgedriver.exe')

    def get_stat():
        # Get raffle info
        driver.get("https://scrap.tf/raffles")
        try:
            stat = driver.find_element_by_tag_name('h1').text
            stat = str(stat)
            stat = stat.split('/')
            entered_count = stat[0]
            entered_count = int(entered_count)
            total_count = stat[-1]
            total_count = int(total_count)
            available_count = total_count - entered_count

            print(f'[+] You have entered : {entered_count} raffles')
            print(f'[+] Raffles available : {total_count} raffles')
            print(f'[+] Raffles to be joined : {available_count} raffles\n')
            return [entered_count, total_count, available_count]
        except:
            print('Unable to get website data. Are you logged in?')
            driver.find_element_by_class_name('sits-login').click()
            cfm = ''
            while cfm != 'y':
                print(
                    'Feel free to login or not to login. This program saves its data on your local laptop and is not connected to the internet')
                cfm = str(input('Have you logged in? (Y/N) : '))
                cfm = cfm.casefold()

    def get_links():  # Collecting raffle links
        stat = get_stat()
        joined = []
        available = []
        total = []

        while len(joined) < stat[0] - tolerance and len(available) != stat[2]:
            z = 0
            while driver.find_element_by_class_name('panel-body.raffle-pagination-done').text != "That's all, no more!":
                z += 1
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                if z == 12:
                    driver.refresh()

            joined_class = driver.find_elements_by_class_name("panel-raffle.raffle-entered [href]")
            joined = [elem.get_attribute('href') for elem in joined_class]
            total_class = driver.find_elements_by_class_name("panel-raffle  [href]")
            total = [elem0.get_attribute('href') for elem0 in total_class]

            for x in joined:
                if 'profile' in x:
                    joined.remove(x)
            for y in total:
                if 'profile' in y:
                    total.remove(y)

            available = list(set(total) - set(joined))
            print('[+] Getting raffle links ...')
            print(f'[+] Collected {len(joined)} links to joined raffles')
            print(f'[+] Collected {len(total)} links to all raffles')
            print(f'[+] Collected {len(available)} links to join-able raffles')


        return joined, total, available

    def enter_raffle():
        print('\n[+] All raffle links collected!')
        joined, total, available = get_links()

        for raffle in available:
            print("\r {}".format(len(available)), 'Raffles left', end="")
            driver.get(url=raffle)

            driver.find_element_by_css_selector(
                '#pid-viewraffle > div.container > div > div.well.raffle-well > div.row.raffle-opts-row > div.col-xs-7.enter-raffle-btns > button:nth-child(3)').click()
            joined.append(raffle)
            available.remove(raffle)
            time.sleep(delay)

    def overwatch():
        while True:
            stat = get_stat()
            if stat[0] >= stat[1]:
                print('\n[!] All raffles joined, monitoring new raffles ...')
                print('====================================================')
                time.sleep(chk_frq)
                driver.refresh()
            else:
                enter_raffle()

    enter_raffle()
    overwatch()
    driver.quit()


initialize()
