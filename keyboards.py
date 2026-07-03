from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu() -> ReplyKeyboardMarkup:
    """Main menu keyboard"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🎨 Generate Image"),
                KeyboardButton(text="🖼️ Convert Image")
            ],
            [
                KeyboardButton(text="🔗 Shorten URL"),
                KeyboardButton(text="📊 Stats")
            ],
            [
                KeyboardButton(text="❓ Help"),
                KeyboardButton(text="ℹ️ About")
            ]
        ],
        resize_keyboard=True
    )

def image_styles() -> InlineKeyboardMarkup:
    """Image style selection keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎨 Artistic", callback_data="style_artistic"),
                InlineKeyboardButton(text="📸 Realistic", callback_data="style_realistic")
            ],
            [
                InlineKeyboardButton(text="🖌️ Anime", callback_data="style_anime"),
                InlineKeyboardButton(text="🌌 Surreal", callback_data="style_surreal")
            ],
            [
                InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_menu")
            ]
        ]
    )

def image_sizes() -> InlineKeyboardMarkup:
    """Image size selection keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📱 Square (512x512)", callback_data="size_512"),
                InlineKeyboardButton(text="🖥️ HD (1024x1024)", callback_data="size_1024")
            ],
            [
                InlineKeyboardButton(text="📺 Widescreen (1792x1024)", callback_data="size_1792"),
                InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_menu")
            ]
        ]
    )

def image_formats() -> InlineKeyboardMarkup:
    """Image format selection keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="PNG", callback_data="format_png"),
                InlineKeyboardButton(text="JPG", callback_data="format_jpg"),
                InlineKeyboardButton(text="WEBP", callback_data="format_webp")
            ],
            [
                InlineKeyboardButton(text="GIF", callback_data="format_gif"),
                InlineKeyboardButton(text="BMP", callback_data="format_bmp"),
                InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_menu")
            ]
        ]
    )

def cancel_keyboard() -> ReplyKeyboardMarkup:
    """Cancel operation keyboard"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Cancel")]
        ],
        resize_keyboard=True
    )
