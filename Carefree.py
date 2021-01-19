import config
import random
import time
import os
from winreg import *
from urllib.request import urlretrieve
from msedge.selenium_tools import Edge, EdgeOptions

#  TODO: ERROR 216, FIX, NOW

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

    def tutorial():
        print('\n[!] What to do after you downloaded the browser engine? [!]')
        time.sleep(1)
        print(
            '1. The WebDriver is downloaded in consideration of your browser version and is located at your "Downloads" folder')
        time.sleep(1)
        print(
            '2. To enable the program, the engine "msedgedriver.exe" needs to be placed in PATH. If you"re not sure which directory in your system is PATH, put "msedgedriver.exe" to "System32"')
        time.sleep(1)
        print(
            'I understand your worry about doing something with System32, or you could add PATH yourself if you feel uncomfortable')
        time.sleep(0.5)
        print('Documentation regarding adding folder to path: "https://docs.alfresco.com/4.2/tasks/fot-addpath.html" ')
        print()
        print(
            'If you"re wondering why I do not automate adding PATH in this program, I do not want to do system wide changes in your system. Everything that happens here is within your consent.')
        exit()

    def get_engine():
        with OpenKey(HKEY_CURRENT_USER, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
            Downloads = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]

        keyPath1 = r"Software\Microsoft\Edge\BLBeacon"
        key1 = OpenKey(HKEY_CURRENT_USER, keyPath1, 0, KEY_READ)
        edgeVersion1 = QueryValueEx(key1, "version")[0]
        edgeVersion1 = str(edgeVersion1)

        #  localappdata = os.getenv('LOCALAPPDATA') <- Nick's installation folder
        install_dir = str('C:\\Windows\\System32')
        files_list = os.listdir(install_dir)

        if 'msedgedriver.exe' in files_list:
            pass
        else:
            print('[!] Browser engine not found, downloading ...')
            ms_site = f'https://msedgedriver.azureedge.net/{edgeVersion1}/edgedriver_win32.zip'
            destination = str(Downloads + '\\edgedriver_win32.zip')
            urlretrieve(ms_site, destination)
            y = 0
            while y < 100:
                time.sleep(2)
                y += 10 + random.randint(1, 6)
                if y > 100:
                    print("\r Download progress :  100 %")
                    break
                else:
                    print("\r Download progress :  {}".format(y), '%', end="")
            tutorial()

    get_engine()

    def get_profile():
        if 'Auto-raffler' in os.listdir('C:\\Users\\nicho\\AppData\\Local\\Microsoft\\Edge'):
            options.add_argument('user-data-dir=C:\\Users\\nicho\\AppData\\Local\\Microsoft\\Edge\\Auto-raffler')
            options.add_argument('profile-directory=Profile 1')
        else:
            os.mkdir('C:\\Users\\nicho\\AppData\\Local\\Microsoft\\Edge\\Auto-raffler')
            get_profile()

    get_profile()

    driver = Edge(options=options, executable_path='C:\\Windows\\System32\\msedgedriver.exe')

    """
    try:
        driver = Edge(options=options,
                      executable_path='C:\\Users\\nicho\\AppData\\Local\\Microsoft\\Edge\\Auto-raffler\\msedgedriver.exe')
    except OSError:
        os.remove(os.getenv('LOCALAPPDATA')+'\\Microsoft\\Edge\\Auto-raffler\\msedgedriver.exe')
        print()
        print('[!] Unsupported browser engine! Please check the readme file on how to fix this!')
        exit()
    driver = Edge(options=options,
                  executable_path='C:\\Users\\nicho\\AppData\\Local\\Microsoft\\Edge\\Auto-raffler\\msedgedriver.exe')
    """

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
        print('\n[+] All raffle links collected!')

        return joined, total, available

    def enter_raffle():
        joined, total, available = get_links()
        for raffle in available:
            print("\r {}".format(len(available)), 'Raffles left', end="")
            driver.get(url=raffle)
            desc = ''
            try:
                driver.find_element_by_css_selector(
                    '#pid-viewraffle > div.container > div > div.well.raffle-well > div.row.raffle-opts-row > div.col-xs-7.enter-raffle-btns > button:nth-child(3)').click()
            except:
                try:
                    desc = driver.find_element_by_class_name('raffle-row-full-width').text
                except:
                    print('[!]Uknown error occured, pleas contact the developer!')
                if 'raffle ended' in desc:
                    print('[!] A raffle has ended and I failed to join it on time!')

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
