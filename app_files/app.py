import time


class App:
    def __init__(self, game_lcd, menu, keyboard):
        self.app_closed = False
        self.lcd = game_lcd
        self.menu_items = menu
        self.keyboard = keyboard

    def display_menu(self, menu):
        # TODO: fix display menu which contains many items.
        selected_menu_items = 0
        menu_items_len = len(menu)
        previous_time = time.ticks_ms()
        end_menu_level = False

        while not end_menu_level:
            self.lcd.fill(0)

            for index, element in enumerate(menu):
                self.lcd.text(element[0], 7, index*8)

            self.lcd.rect(2, 8 * selected_menu_items + 2, 3, 3, 1)
            self.lcd.show()

            time_passed = time.ticks_diff(time.ticks_ms(), previous_time)
            if time_passed >= 200:

                if not self.keyboard.button_up.value():
                    selected_menu_items -= 1
                    previous_time = time.ticks_ms()

                if not self.keyboard.button_down.value():
                    selected_menu_items += 1
                    previous_time = time.ticks_ms()

                if selected_menu_items == -1:
                    selected_menu_items = menu_items_len - 1

                elif selected_menu_items == menu_items_len:
                    selected_menu_items = 0

                if not self.keyboard.button_right.value():
                    previous_time = time.ticks_ms()

                    if callable(menu[selected_menu_items][1]):
                        menu[selected_menu_items][1]()
                    else:
                        self.display_menu(menu[selected_menu_items][1])

                if not self.keyboard.button_arrow_left.value():
                    end_menu_level = True
                    time.sleep_ms(500)

                if not self.keyboard.button_arrow_back.value():
                    end_menu_level = True
                    self.app_closed = True

    def run(self):
        while not self.app_closed:
            self.display_menu(self.menu_items)
        else:
            self.lcd.fill(0)
            self.lcd.text("Good Bye!", 7, 20)
            self.lcd.show()

    def exit(self):
        self.app_closed = True
