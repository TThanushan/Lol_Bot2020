import time
import random
import image_functions as imf
import directkeys as dk

class ItemBuild:
	#index : [name, price]
    current_index = 0
    build_order = {
        0 : ["cloth armor", 450],
        1 : ["warding totem", 0],
        2 : ["ninja tabi", 800],
        3 : ["phage", 1250],
        4 : ["sheen", 1050],
        5 : ["stinger", 1100],
        6 : ["trinity force", 333],
        7 : ["jaurim's fist", 1200],
        8 : ["pickaxe", 875],
        9 : ["sterak's gage", 725],
        10 : ["spirit visage", 2800],
        11 : ["dead man's plat", 2900],
        12 : ["thornmail", 2900],
    }

    def get_current_item_name(self):
        return self.build_order[self.current_index][0]
    
    def get_current_item_price(self):
        return self.build_order[self.current_index][1]
    
    def open_shop(self):
        dk.PressKey('p')
    
    def select_search_bar():
        dk.MaintainKey('ctrl')
        dk.PressKey('l')
        dk.ReleaseKey('ctrl')
    
    def type_current_item_name(self):
        dk.type_text(self.get_current_item_name())
    
    def buy_selected_item():
        dk.PressKey("enter")
        time.sleep(0.1 + random.random())
        dk.PressKey("enter")
        time.sleep(0.1 + random.random())
    
    def close_shop():
        dk.PressKey('esc')
    
    def try_to_buy_current_item(self):
        """
        Try to buy an item from the shop by typing the name.
        """
        current_gold = imf.get_gold()
        if current_gold >= self.get_current_item_price():
            open_shop()
            while current_gold >= self.get_current_item_price():
                self.select_search_bar()
                self.type_current_item_name()
                self.buy_selected_item()
                current_gold -= self.get_current_item_price()
                self.current_index += 1
                if self.current_index not in self.build_order:
                    break
            self.close_shop()


class ScreenInfos:
    def get_all_properties(self):
        return {
            "Health" : str(self.current_health) + " / " + str(self.max_health),
            "Mana" : str(self.current_mana) + " / " + str(self.max_mana),        
            "Allied minions" : self.allied_minions_nb,
            "Allied champions" : self.allied_champions_nb,
            "Enemy minions" : self.enemy_minions_nb,
            "Enemy champions" : self.enemy_champions_nb,
            "is low life" : self.current_health < 200,
            "is at fountain" : self.is_at_fountain,
            "gold" : self.gold
            }
    
    current_health = 0
    max_health = 0
    current_mana = 0
    max_mana = 0
    allied_minions_nb = 0
    allied_champions_nb = 0
    enemy_minions_nb = 0
    enemy_champions_nb = 0
    is_at_fountain = False
    gold = 0


class Shortcut:
	spell_1 = 'q'
	spell_2 = 'w'
	spell_3 = 'e'
	spell_4 = 'r'
	summoners_spell_1 = 'd'
	summoners_spell_2 = 'f'
	attack_move = ' '
	toggle_shop = 'p'