import pyautogui
import time
import random
import cv2 as cv
import mss
import numpy as np
import winsound
from pyautogui import KEYBOARD_KEYS

#set vm display to 640, 480

class FarmingBot:
    def __init__(self):
        pyautogui.failSafeCheck = True
        pyautogui.PAUSE = 0.01
        self.TIMEOUT = 220
        self.str_time = time.time()
        self.cooef = 0.7
        self.spawn_area = 'dfghjk'
        self.funnel = 'als'
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
        
        self.attack_img_2 = self.img_load('attack_2_img.png')
        self.find_match_img = self.img_load('find_match.png')
        self.return_img = self.img_load('return.png')
        self.ok_img = self.img_load('ok.png')
        self.maxed_img = self.img_load('maxed.png')
        self.star_army_img = self.img_load('start_army.png')
        self.attack_img = self.img_load('attack_img.png')
        self.air_defences = [
            self.img_load('air_def1.png'),
            self.img_load('air_def2.png'),
            self.img_load('air_def3.png'),
            self.img_load('air_def4.png'),
            self.img_load('air_def5.png')
            ]
    def img_load(self, img_path):
        return cv.cvtColor(np.array(cv.imread(img_path)), cv.COLOR_BGR2GRAY)

    def detect_object(self, img, amount=1):
        try:
            with mss.mss() as sct:
                screen_img = sct.grab(sct.monitors[0])
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
        time.sleep(3)
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
                        time.sleep(random.uniform(0.06, 0.12))
                        pyautogui.click()
                if count >= 3:
                    return
        return

    def handel_timeout(self):
        pyautogui.hotkey('ctrl', 'shift', '5')
        time.sleep(15)
        pyautogui.typewrite('z')
        time.sleep(15)
        pyautogui.typewrite('x')
        time.sleep(120)
        pyautogui.typewrite('w')

    def spawn_army(self):
        print('army sequance staring...')
        if time.time() - self.str_time > 200:
            print('leaving loop, timeout')
            return
        
        self.air_defence()
        time.sleep(5)
        pyautogui.typewrite(self.dragon)
        for i in range(3):
            pyautogui.press(self.funnel[i])
            time.sleep(random.uniform(0.04, 0.09))

        time.sleep(random.uniform(17, 27))
        for _ in range(12):
            pyautogui.press(random.choice(self.spawn_area))
            time.sleep(random.uniform(0.04, 0.09))  

        for hero in self.heroes:
            pyautogui.press(hero)
            time.sleep(0.12)
            pyautogui.press(random.choice(self.heroes_drop))
            time.sleep(random.uniform(0.06, 0.12))

        time.sleep(random.uniform(17, 20))
        for hero in self.heroes:
            pyautogui.press(hero)

        time.sleep(4)
        pyautogui.typewrite(self.lighting_spell)
        for _ in range(11):
            time.sleep(random.uniform(0.06, 0.12))
            pyautogui.typewrite('0')

    def end_battle(self):
        print('checking if the game ended')
        if self.detect_object(self.return_img, amount=1) is not None:
            pyautogui.typewrite(self.return_base)
            time.sleep(3)
            print('game end found, ENDING!')
            return True
        else:
            print('game not ended, contunue!')
            return False

    def find_new(self):
        while not self.detect_object(self.attack_img, amount=1):
            if time.time() - self.str_time > self.TIMEOUT:
                print('leaving loop, timeout')
                return
            print('waiting for attack img')
            time.sleep(1)
        print('Staring battle search')
        
        pyautogui.typewrite(self.attack_1)
        time.sleep(1)
        
        while not self.detect_object(self.find_match_img, amount=1):
            if time.time() - self.str_time > self.TIMEOUT:
                print('leaving loop, timeout')
                return
            print('waiting for find find match img')
            time.sleep(1)

        pyautogui.typewrite(self.find_match)
        time.sleep(1)

        while not self.detect_object(self.attack_img_2, amount=1):
            if time.time() - self.str_time > self.TIMEOUT:
                print('leaving loop, timeout')
                return
            print('waiting for army to load...')
            time.sleep(1)
        pyautogui.typewrite(self.attack_2)

        time.sleep(1)
        print('beginning search...')

    def check_maxed(self):
        print('checking if storage is maxed')
        if self.detect_object(self.maxed_img):
            winsound.Beep(1200, 3000)
            time.sleep(230)
            return True
        else:
            print('storage is not maxed yet...')
            return False

    def check_max(self):
        if self.detect_object(self.maxed_img):
            winsound.Beep(1200, 3000)
            time.sleep(230)

    def game_loop(self):
        while True:
            self.check_maxed()
            self.str_time = time.time()
            print('beginning of the game loop...')
            self.find_new()
            self.spawn_army()
            while not self.end_battle():
                if time.time() - self.str_time > 220:
                    print('solving timeout')
                    self.handel_timeout()
                    break
                time.sleep(3)
            print('battle ended, beginning game sequance again')


if __name__ == '__main__':
    time.sleep(5)
    FarmingBot().game_loop()