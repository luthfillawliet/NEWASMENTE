from telegram import ReplyKeyboardMarkup, KeyboardButton,replykeyboardmarkup
from telegram.ext import ConversationHandler, MessageHandler, Filters

brand_type_mapping = {
    "EDMI": ["MK6N", "MK6E", "MK10E", "MK7B", "MK7C", "MK10", "MK6", "MK7MI", "MK11"],
    "ACTARIS": ["SL7000"],
    "ITRON": ["CENTIAN", "SL6000", "SL7000A", "NIAS DC", "NIAS CT", "ACE6000"],
    "WASION": ['iMeter 318', 'iMeter 310', 'aMeter 100'],
    "HEXING": ['HXE313-KP', 'HXE320', 'HXT300'],
    "SMI": ['SMI-3000'],
    "LANDIS+GYR": ['E550(ZMG)', 'E850(ZMD)'],
    "SCHENEIDER": ['ION7400', 'ION860'],
    "CEWE": ['PROMETER 100']
}
class AmiconBot():

    
    def get_first_choice(self,message:str):
        self.first_choice = message

    def set_asset_choice(self):
        keyboard = [
            [KeyboardButton("LOCATION")],
            [KeyboardButton("METER")],
            [KeyboardButton("MODEM")],
            [KeyboardButton("SIMCARD")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        return  reply_markup
    def get_selected_asset(self,selected_aset:str):
        self.selected_asset = selected_aset
    
    def set_meter_brand(self):
        # Get the keys from the dictionary and convert them into a list of lists
        keyboard = [[KeyboardButton(key)] for key in brand_type_mapping.keys()]
        
        # Create the ReplyKeyboardMarkup
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        return reply_markup
    def get_selected_brand(self,selected_brand:str):
        self.selected_brand = selected_brand
    def set_brand_type(self, selected_brand: str):
        # Create a list of lists for keyboard buttons from the values in the list
        keyboard = [[KeyboardButton(key)] for key in brand_type_mapping[selected_brand]]

        # Create the ReplyKeyboardMarkup
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)

        return reply_markup
    
    def set_comissioning(self,location_code:str):
        print("comissioning location code : "+location_code)
        

    @staticmethod
    def start():
        # Define the custom keyboard
        keyboard = [
            [KeyboardButton("ASSET")],
            [KeyboardButton("COMISSIONING")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        return reply_markup