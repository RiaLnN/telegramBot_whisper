from aiogram.filters.callback_data import CallbackData

class SettingsCB(CallbackData, prefix="set"):
    action: str
    value: str = ""