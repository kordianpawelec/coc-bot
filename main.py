import pyautogui
import time
import random
import cv2 as cv
import mss
import numpy as np
import winsound
import threading

#set vm display to 640, 480

class ReloadRequest(Exception):
    pass

class FarmingBot:
    def __init__(self):
        self.TIMEOUT = 220
        self.str_time = time.time()
        self.cooef = 0.7
        self.spawn_area = 'dfghjk'
        self.funnel = 'al'
        self.heroes_drop = 'fghj'
        self.heroes = '234'
        self.dragon = '1'
        self.lighting_spell = '5'
        self.attack_1 = 'e'
        self.find_match = 'r'
        self.attack_2 = 't'
        self.next_battle = 'y'
        self.return_base = 'w'
        self.reset_app = 'zxcv'

        self.reload_flag = threading.Event()
        self.watchdog = 0
        self.reload_pos = None
        self.all_img = []
        self.reload_img = self.img_load('reload.png')
        self.attack_img_2 = self.img_load('attack_2_img.png')
        self.find_match_img = self.img_load('find_match.png')
        self.return_img = self.img_load('return.png')
        self.ok_img = self.img_load('ok.png')
        self.maxed_img = self.img_load('maxed.png')
        self.star_army_img = self.img_load('start_army.png')
        self.attack_img = self.img_load('attack_img.png')
        self.try_again_img = self.img_load('try_again.png')
        self.air_defences = [
            self.img_load('air_def1.png'),
            self.img_load('air_def2.png'),
            self.img_load('air_def3.png'),
            self.img_load('air_def4.png'),
            self.img_load('air_def5.png'),
            self.img_load('air_def6.png')
            ]
    def __del__(self):
        for img in self.all_img:
            del img

    def img_load(self, img_path):
        return cv.cvtColor(np.array(cv.imread(img_path)), cv.COLOR_BGR2GRAY)

    def check_reload(self):
        if self.reload_flag.is_set():
            raise ReloadRequest('reloading game please wait 2min')

    def sleep(self, sec, step=0.2):
        end = time.monotonic() + sec
        while time.monotonic() < end:
            self.check_reload()
            time.sleep(min(step, end - time.monotonic()))

    def detect_object(self, img, amount=1):
        try:
            with mss.mss() as sct:
                screen_img = sct.grab(sct.monitors[1])
                screen_img = cv.cvtColor(np.array(screen_img), cv.COLOR_BGRA2GRAY)
                
                result = cv.matchTemplate(screen_img, img, cv.TM_CCOEFF_NORMED)
                matches: list[tuple[int, int]] = []
                counter = 0
                while counter < amount:
                    _, max_val, _, max_loc = cv.minMaxLoc(result)
                    if max_val < self.cooef:
                        break
                    x, y = max_loc
                    counter += 1
                    if (x, y) in matches and counter < 20:
                        result[y, x] = -1.0
                        continue
                    matches.append((x, y))
                    result[y, x] = -1.0
                return matches if matches else None
                
        except IOError as e:
            print('io error', e)

    def air_defence(self):
        count = 0
        self.sleep(3)
        print('checking for air deffence')
        pyautogui.typewrite(self.lighting_spell)
        for img in self.air_defences:
            coords = self.detect_object(img, amount=3)
            if coords is not None:
                print('found some air deffence')
                print('dropping ls at:', coords)
                for coord in coords:
                    count += 1
                    pyautogui.moveTo(coord)
                    for _ in range(3):
                        self.sleep(random.uniform(0.06, 0.12))
                        pyautogui.click()
                if count >= 3:
                    return
        return

    def handel_timeout(self):
        pass

    def spawn_army(self):
        print('army sequance staring...')
        if time.time() - self.str_time > 200:
            print('leaving loop, timeout')
            return
        
        self.air_defence()
        self.sleep(5)
        pyautogui.typewrite(self.dragon)
        for i in range(2):
            pyautogui.press(self.funnel[i])
            self.sleep(random.uniform(0.04, 0.09))

        self.sleep(random.uniform(17, 27))
        for _ in range(13):
            pyautogui.press(random.choice(self.spawn_area))
            self.sleep(random.uniform(0.04, 0.09))

        for hero in self.heroes:
            pyautogui.press(hero)
            self.sleep(0.12)
            pyautogui.press(random.choice(self.heroes_drop))
            self.sleep(random.uniform(0.06, 0.12))
        pyautogui.typewrite('4')
        self.sleep(random.uniform(17, 20))
        for hero in self.heroes:
            pyautogui.press(hero)

        self.sleep(4)
        pyautogui.typewrite(self.lighting_spell)
        for _ in range(11):
            self.sleep(random.uniform(0.06, 0.12))
            pyautogui.typewrite('0')

    def end_battle(self):
        if self.detect_object(self.return_img, amount=1) is not None:
            pyautogui.typewrite(self.return_base)
            self.sleep(3)
            print('game end found, ENDING!')
            return True
        else:
            return False

    def reload_watchdog(self):
        while True:
            if self.reload_flag.is_set():
                time.sleep(1)
                continue
            
            if pos:=self.detect_object(self.reload_img):
                self.reload_pos = pos[0]
                self.reload_flag.set()
            elif pos:=self.detect_object(self.try_again_img):
                self.reload_pos = pos[0]
                self.reload_flag.set()

            time.sleep(3)


    def find_new(self):
        print('waiting for attack img')
        while not self.detect_object(self.attack_img):
            if time.time() - self.str_time > self.TIMEOUT:
                print('leaving loop, timeout')
                return
            self.sleep(1)
        print('Staring battle search')
        
        pyautogui.typewrite(self.attack_1)
        self.sleep(1)
        
        print('waiting for find find match img')
        while not self.detect_object(self.find_match_img):
            if time.time() - self.str_time > self.TIMEOUT:
                print('leaving loop, timeout')
                return
            self.sleep(1)
        print('found match img')
        pyautogui.typewrite(self.find_match)
        self.sleep(1)
        print('waiting for attack two to load...')
        while not self.detect_object(self.attack_img_2):
            if time.time() - self.str_time > self.TIMEOUT:
                print('leaving loop, timeout')
                return
            self.sleep(1)
        print('attack found beginning battle...')
        pyautogui.typewrite(self.attack_2)

        self.sleep(1)
        print('beginning search...')

    def handle_reload(self):
        if self.reload_pos is not None:
            pyautogui.moveTo(self.reload_pos)
            pyautogui.click()
        time.sleep(15)
        self.reload_pos = None


    def check_maxed(self):
        print('checking if storage is maxed')
        if self.detect_object(self.maxed_img):
            winsound.Beep(1200, 30000)
            self.sleep(230)
            return True
        else:
            print('storage is not maxed yet...')
            return False

    def game_loop(self):
        if self.watchdog == 0:
            thread = threading.Thread(target=self.reload_watchdog, daemon=True)
            thread.start()
            self.watchdog += 1
        while True:
            try:
                # self.check_maxed()
                self.str_time = time.time()
                print('beginning of the game loop...')
                self.find_new()
                self.spawn_army()
                print('checking if the game ended')
                while not self.end_battle():
                    if time.time() - self.str_time > 220:
                        print('solving timeout')
                        self.handel_timeout()
                        break
                    self.sleep(3)
                print('battle ended, beginning game sequance again')
            except ReloadRequest:
                print('game relaoded')
                try:
                    self.handle_reload()
                finally:
                    self.reload_flag.clear()
                continue



if __name__ == '__main__':
    time.sleep(5)
    FarmingBot().game_loop()