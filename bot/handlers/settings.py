import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest

from bot.core.constants import (
    CMD_SETTINGS, TXT_SETTINGS_MAIN, TXT_SETTINGS_PRESETS, 
    TXT_SETTINGS_CLOSED, TXT_ERR_ADMIN_ONLY, BTN_AUTO_ON, 
    BTN_AUTO_OFF, BTN_TONE, BTN_BACK, BTN_CLOSE, PROMPT_PRESETS
)
from bot.core.callbacks import SettingsCB
from bot.service.settings import get_or_create_settings, toggle_auto_mode, update_preset

logger = logging.getLogger(__name__)
router = Router()

async def is_admin(message: Message, bot: Bot) -> bool:
    if message.chat.type == "private":
        return True
    if not message.from_user:
        return False
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in ["administrator", "creator"]

def get_main_keyboard(is_auto: bool, current_tone: str):
    builder = InlineKeyboardBuilder()
    
    mode_text = BTN_AUTO_ON if is_auto else BTN_AUTO_OFF
    builder.button(text=mode_text, callback_data=SettingsCB(action="toggle_mode"))
    
    tone_text = BTN_TONE.format(tone=current_tone.capitalize())
    builder.button(text=tone_text, callback_data=SettingsCB(action="menu_tone"))
    
    builder.button(text=BTN_CLOSE, callback_data=SettingsCB(action="close"))
    
    builder.adjust(1)
    return builder.as_markup()

def get_presets_keyboard():
    builder = InlineKeyboardBuilder()
    
    for preset_key in PROMPT_PRESETS.keys():
        builder.button(
            text=preset_key.capitalize(), 
            callback_data=SettingsCB(action="set_tone", value=preset_key)
        )
        
    builder.button(text=BTN_BACK, callback_data=SettingsCB(action="main"))
    builder.adjust(2, 2, 1)
    return builder.as_markup()


@router.message(Command(CMD_SETTINGS))
async def cmd_settings(message: Message, bot: Bot):
    if not await is_admin(message, bot):
        await message.answer(TXT_ERR_ADMIN_ONLY)
        return

    settings = await get_or_create_settings(message.chat.id)
    keyboard = get_main_keyboard(settings.is_auto_mode, settings.prompt_preset)
    
    await message.answer(TXT_SETTINGS_MAIN, reply_markup=keyboard, parse_mode="HTML")

@router.callback_query(SettingsCB.filter(F.action == "toggle_mode"))
async def cb_toggle_mode(query: CallbackQuery, callback_data: SettingsCB, bot: Bot):
    if not isinstance(query.message, Message):
        return
    
    if not await is_admin(query.message, bot):
        await query.answer(TXT_ERR_ADMIN_ONLY, show_alert=True)
        return

    new_state = await toggle_auto_mode(query.message.chat.id)
    settings = await get_or_create_settings(query.message.chat.id)
    
    keyboard = get_main_keyboard(new_state, settings.prompt_preset)
    
    try:
        await query.message.edit_reply_markup(reply_markup=keyboard)
    except TelegramBadRequest:
        pass
    
    await query.answer()

@router.callback_query(SettingsCB.filter(F.action == "menu_tone"))
async def cb_menu_tone(query: CallbackQuery, callback_data: SettingsCB, bot: Bot):
    if not isinstance(query.message, Message):
        return
    
    if not await is_admin(query.message, bot):
        await query.answer(TXT_ERR_ADMIN_ONLY, show_alert=True)
        return

    keyboard = get_presets_keyboard()
    await query.message.edit_text(TXT_SETTINGS_PRESETS, reply_markup=keyboard, parse_mode="HTML")
    await query.answer()

@router.callback_query(SettingsCB.filter(F.action == "set_tone"))
async def cb_set_tone(query: CallbackQuery, callback_data: SettingsCB, bot: Bot):
    if not isinstance(query.message, Message):
        return
    
    if not await is_admin(query.message, bot):
        await query.answer(TXT_ERR_ADMIN_ONLY, show_alert=True)
        return


    await update_preset(query.message.chat.id, callback_data.value)
    
    settings = await get_or_create_settings(query.message.chat.id)
    keyboard = get_main_keyboard(settings.is_auto_mode, settings.prompt_preset)
    
    await query.message.edit_text(TXT_SETTINGS_MAIN, reply_markup=keyboard, parse_mode="HTML")
    await query.answer(f"Tone set to: {callback_data.value.capitalize()}")

@router.callback_query(SettingsCB.filter(F.action == "main"))
async def cb_back_to_main(query: CallbackQuery, callback_data: SettingsCB, bot: Bot):
    if not isinstance(query.message, Message):
        return
    
    if not await is_admin(query.message, bot):
        await query.answer(TXT_ERR_ADMIN_ONLY, show_alert=True)
        return

    settings = await get_or_create_settings(query.message.chat.id)
    keyboard = get_main_keyboard(settings.is_auto_mode, settings.prompt_preset)
    
    await query.message.edit_text(TXT_SETTINGS_MAIN, reply_markup=keyboard, parse_mode="HTML")
    await query.answer()

@router.callback_query(SettingsCB.filter(F.action == "close"))
async def cb_close_settings(query: CallbackQuery):
    if not isinstance(query.message, Message):
        return
    
    await query.message.delete()
    await query.answer(TXT_SETTINGS_CLOSED)