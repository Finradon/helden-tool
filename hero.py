from utilities.dice import xd6, d20, roll
from utilities.formatting import roll_tuple_to_string
import math
import json

class hero:
    
    def __init__(self, name, at, pa, ini_dice: int, ini_bonus: int, tp: tuple, lep, mu, kl, intu, ch, ff, ge, ko, kk, gs, mr, rs, eisern):
        self.name:str = name
        self.max_at = at
        self.max_pa = pa
        self.at: int = at
        self.pa: int = pa
        self.tp: tuple = tp # tuple containing number of d6s on index 0, and base tp on index 1
        self.lep: int = lep
        self.max_lep: int = lep
        self.mu: int = mu
        self.kl: int = kl
        self.intu: int = intu
        self.ch: int = ch
        self.ff: int = ff
        self.ge: int = ge
        self.ko: int = ko
        self.kk: int = kk
        self.gs: int = gs
        self.mr: int = mr
        self.rs: int = rs
        self.eisern: bool = eisern 
        self.ini_base: int = round((mu+mu+intu+ge)/5)
        self.ini: int = self.ini_roll(ini_bonus, ini_dice)
        self.wound_count = 0
        self.state = "☑️"

    @classmethod
    def from_json(cls, file: str):
        json_data = json.loads(file)
        return cls(
            json_data["Name"],
            json_data["AT"],
            json_data["PA"],
            json_data["INI"]["W6"],
            json_data["INI"]["BONUS"],
            (
                json_data["TP"]["W6"],
                json_data["TP"]["Basis"]
            ),
            json_data["LeP"],
            json_data["MU"],
            json_data["KL"],
            json_data["INTU"],
            json_data["CH"],
            json_data["FF"],
            json_data["GE"],
            json_data["KO"],
            json_data["KK"],
            json_data["GS"],
            json_data["MR"],
            json_data["RS"],
            json_data["Eisern"]
        )
    def tp_roll(self) -> int:
        """
        Roll for damage
        @return: TP value
        """
        return xd6(self.tp[0]) + self.tp[1]

    def ini_roll(self, ini_bonus, ini_dice):
        """
        Roll for initiative
        """
        return xd6(ini_dice) + self.ini_base + ini_bonus
    
    def attack_roll(self) -> str:
        """
        Roll on the attack value, create a tuple from the results and format them
        @return: string representation of the roll
        """
        res = d20()

        if res == 20:
            if d20() > self.at:
                success = roll.FAIL_CONF
            else:
                success = roll.FAIL
        elif res <= self.at:
            if res == 1:
                if d20() < self.at:
                    success = roll.CRIT_CONF
                else:
                    success = roll.CRIT
            else:
                success = roll.SUCCESS    
            
        else: 
            success = roll.FAIL

        res_tuple = (res, success, self.tp_roll())
        return roll_tuple_to_string(res_tuple)
    
    def parry_roll(self) -> str:
        """
        Roll on the parry value, create a tuple from the results and format them
        @return: string representation of the roll
        """
        res = d20()

        if res == 20:
            if d20() > self.pa:
                success = roll.FAIL_CONF
            else:
                success = roll.FAIL
        elif res <= self.pa:
            if res == 1:
                if d20() < self.pa:
                    success = roll.CRIT_CONF
                else:
                    success = roll.CRIT
            else:
                success = roll.SUCCESS    
            
        else: 
            success = roll.FAIL

        res_tuple = (res, success)
        return roll_tuple_to_string(res_tuple)
    
    def receive_damage(self, value: int, tp: bool):
        """
        Receive damage, under consideration of armor. Also adds wounds, if applicable
        @param value: the TP to be added
        """
        if value is None:
            return
        sp_correction = 0
        if not tp:
            sp_correction = self.rs

        damage = value - self.rs + sp_correction
        if damage < 0:
            damage = 0
        self.lep -= damage

        if self.eisern:
            eisern = 2
        else:
            eisern = 0
        
        nr_wounds = math.floor((damage-1)/(self.ko + eisern))
        for _ in range(nr_wounds):
            self.add_wound()

        if self.lep <= 0:
            if "☠️" not in self.name:
                self.name = self.name + "☠️" 

        self.check_low_lep()

    def receive_healing(self, value: int):
        self.lep += value

        if self.lep > self.max_lep:
            self.lep = self.max_lep

        wounds_healed = math.floor(value/7)
        for _ in range(wounds_healed):
            self.remove_wound()

        self.check_low_lep()

    def add_wound(self):
        """
        Add a wound, automatically reduce appropriate values
        """
        self.wound_count += 1
        self.at -= 3
        self.pa -= 3
        self.max_at -= 3
        self.max_pa -= 3
        self.ini -= 3
        self.ge -= 3
    
    def remove_wound(self):
        """
        Remove a wound, if at least one exists
        """
        if self.wound_count > 0:
            self.wound_count -= 1
            self.at += 3
            self.pa += 3
            self.max_at += 3
            self.max_pa += 3
            self.ini += 3
            self.ge += 3     

    def set_ini(self, value):
        """
        Set the initiative value manually, so that players can roll themselves
        """
        self.ini = value

    def check_low_lep(self):

        if self.lep < math.floor(self.max_lep/4):
            self.at = self.max_at
            self.pa = self.max_pa
            self.at -= 3
            self.pa -= 3
            self.state = "‼️"
        elif self.lep < math.floor(self.max_lep/3):
            self.at = self.max_at
            self.pa = self.max_pa
            self.at -= 2
            self.pa -= 2
            self.state = "❗"
        elif self.lep < math.floor(self.max_lep/2):
            self.at = self.max_at
            self.pa = self.max_pa
            self.at -= 1
            self.pa -= 1
            self.state = "❕"
        else:
            self.at = self.max_at
            self.pa = self.max_pa
            self.state = "☑️"