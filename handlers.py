import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from keyboards import main_menu, image_styles, image_sizes, image_formats, cancel_keyboard
from states import GenerateImageStates, ConvertImageStates, ShortenURLStates
from utils import generate_image, convert_image, shorten_url, validate_image_format, get_file_size_limit
from config import config

logger = logging.getLogger(__name__)
router = Router()

# --- Command Handlers ---

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    """Handle /start command"""
    await state.clear()
    await message.answer(
        "🤖 *Welcome to AIGentArtBot!*\n\n"
        "I'm your AI-powered assistant for:\n"
        "🎨 *Image Generation* - Create images from text\n"
        "🖼️ *Image Conversion* - Convert between formats\n"
        "🔗 *URL Shortening* - Make long URLs short\n\n"
        "Use the buttons below to get started!",
        reply_markup=main_menu(),
        parse_mode=ParseMode.MARKDOWN
    )

@router.message(Command("help"))
async def help_command(message: Message, state: FSMContext):
    """Handle /help command"""
    await state.clear()
    help_text = (
        "📖 *Available Commands:*\n\n"
        "/start - Start the bot\n"
        "/help - Show this help\n"
        "/generate - Generate an image\n"
        "/convert - Convert an image\n"
        "/shorten - Shorten a URL\n"
        "/about - About this bot\n"
        "/cancel - Cancel current operation"
    )
    await message.answer(help_text, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu())

@router.message(Command("about"))
async def about_command(message: Message, state: FSMContext):
    """Handle /about command"""
    await state.clear()
    await message.answer(
        "ℹ️ *About AIGentArtBot*\n\n"
        "Version: 1.0.0\n"
        "Created with ❤️ using aiogram 3.x\n"
        "Deployed on Railway\n\n"
        "Features:\n"
        "✅ AI Image Generation\n"
        "✅ Image Format Conversion\n"
        "✅ URL Shortening\n\n"
        "🚀 *Powered by AI*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu()
    )

@router.message(Command("cancel"))
async def cancel_command(message: Message, state: FSMContext):
    """Handle /cancel command"""
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
        await message.answer(
            "❌ Operation cancelled successfully!",
            reply_markup=main_menu()
        )
    else:
        await message.answer(
            "🤔 No operation in progress.",
            reply_markup=main_menu()
        )

# --- Menu Button Handlers ---

@router.message(F.text == "🎨 Generate Image")
async def generate_image_menu(message: Message, state: FSMContext):
    """Handle Generate Image button click"""
    await state.set_state(GenerateImageStates.waiting_for_prompt)
    await message.answer(
        "🎨 *Generate Image*\n\n"
        "Please describe the image you want to create.\n"
        "Example: 'A beautiful sunset over mountains'\n\n"
        "Choose a style below:",
        reply_markup=image_styles(),
        parse_mode=ParseMode.MARKDOWN
    )

@router.message(F.text == "🖼️ Convert Image")
async def convert_image_menu(message: Message, state: FSMContext):
    """Handle Convert Image button click"""
    await state.set_state(ConvertImageStates.waiting_for_image)
    await message.answer(
        "🖼️ *Convert Image*\n\n"
        "Please send me an image you want to convert.\n"
        f"Supported formats: {', '.join(config.SUPPORTED_FORMATS)}\n"
        f"Max file size: {get_file_size_limit() // (1024*1024)}MB",
        reply_markup=cancel_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

@router.message(F.text == "🔗 Shorten URL")
async def shorten_url_menu(message: Message, state: FSMContext):
    """Handle Shorten URL button click"""
    await state.set_state(ShortenURLStates.waiting_for_url)
    await message.answer(
        "🔗 *Shorten URL*\n\n"
        "Please send me the URL you want to shorten.\n"
        "Example: https://example.com/very/long/url/that/needs/shortening",
        reply_markup=cancel_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

@router.message(F.text == "📊 Stats")
async def stats_menu(message: Message, state: FSMContext):
    """Handle Stats button click"""
    await state.clear()
    await message.answer(
        "📊 *Bot Stats*\n\n"
        "👥 Active Users: 0\n"
        "🎨 Images Generated: 0\n"
        "🔄 Images Converted: 0\n"
        "🔗 URLs Shortened: 0\n\n"
        "✨ More features coming soon!",
        reply_markup=main_menu(),
        parse_mode=ParseMode.MARKDOWN
    )

@router.message(F.text == "❓ Help")
async def help_menu(message: Message, state: FSMContext):
    """Handle Help button click"""
    await help_command(message, state)

@router.message(F.text == "ℹ️ About")
async def about_menu(message: Message, state: FSMContext):
    """Handle About button click"""
    await about_command(message, state)

@router.message(F.text == "❌ Cancel")
async def cancel_menu(message: Message, state: FSMContext):
    """Handle Cancel button click"""
    await cancel_command(message, state)

# --- Callback Query Handlers ---

@router.callback_query(F.data.startswith("style_"))
async def handle_style_selection(callback: CallbackQuery, state: FSMContext):
    """Handle image style selection"""
    style = callback.data.split("_")[1]
    await state.update_data(style=style)
    
    await callback.message.edit_text(
        f"🎨 Selected style: *{style.capitalize()}*\n\n"
        "Now, choose the image size:",
        reply_markup=image_sizes(),
        parse_mode=ParseMode.MARKDOWN
    )
    await callback.answer()

@router.callback_query(F.data.startswith("size_"))
async def handle_size_selection(callback: CallbackQuery, state: FSMContext):
    """Handle image size selection"""
    size = callback.data.split("_")[1]
    await state.update_data(size=size)
    await state.set_state(GenerateImageStates.waiting_for_prompt)
    
    await callback.message.edit_text(
        f"✅ Selected size: *{size}x{size}*\n\n"
        "Now, please describe what image you'd like to create.\n"
        "Be detailed for better results! 🎨",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=cancel_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("format_"))
async def handle_format_selection(callback: CallbackQuery, state: FSMContext):
    """Handle image format selection"""
    format_name = callback.data.split("_")[1]
    await state.update_data(target_format=format_name)
    await state.set_state(ConvertImageStates.waiting_for_image)
    
    await callback.message.edit_text(
        f"✅ Selected format: *{format_name.upper()}*\n\n"
        "Now, please send me the image you want to convert.",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=cancel_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    """Handle back to menu"""
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "🏠 Back to main menu!",
        reply_markup=main_menu()
    )
    await callback.answer()

# --- Message Handlers for States ---

@router.message(StateFilter(GenerateImageStates.waiting_for_prompt))
async def handle_generation_prompt(message: Message, state: FSMContext):
    """Handle image generation prompt"""
    if message.text == "❌ Cancel":
        await cancel_command(message, state)
        return
    
    prompt = message.text
    data = await state.get_data()
    style = data.get("style", "realistic")
    size = data.get("size", "1024")
    
    # Send processing message
    processing_msg = await message.answer(
        "🎨 Generating your image...\n"
        "This might take a few moments. Please wait ⏳"
    )
    
    try:
        # Generate the image
        image_data = await generate_image(prompt, style, size)
        
        if image_data:
            # Create a file object from the bytes
            from aiogram.types import BufferedInputFile
            file = BufferedInputFile(image_data, filename="generated_image.png")
            
            await message.answer_photo(
                photo=file,
                caption=f"🎨 *Your AI-generated image*\n\n"
                        f"📝 Prompt: {prompt}\n"
                        f"🎭 Style: {style.capitalize()}\n"
                        f"📐 Size: {size}x{size}\n\n"
                        f"✨ Generated by AIGentArtBot",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=main_menu()
            )
        else:
            await message.answer(
                "❌ Sorry, I couldn't generate the image. Please try again later.",
                reply_markup=main_menu()
            )
    
    except Exception as e:
        logger.error(f"Error in generation: {e}")
        await message.answer(
            "❌ An error occurred during generation. Please try again.",
            reply_markup=main_menu()
        )
    
    await processing_msg.delete()
    await state.clear()

@router.message(StateFilter(ConvertImageStates.waiting_for_image))
async def handle_conversion_image(message: Message, state: FSMContext):
    """Handle image for conversion"""
    if message.text == "❌ Cancel":
        await cancel_command(message, state)
        return
    
    if not message.photo and not message.document:
        await message.answer(
            "⚠️ Please send me an image file or photo.",
            reply_markup=cancel_keyboard()
        )
        return
    
    try:
        # Get the image file
        if message.photo:
            file = await message.photo[-1].get_clean()  # Get the largest photo
        else:
            file = await message.document.get_clean()
        
        # Check file size
        if file.file_size > get_file_size_limit():
            await message.answer(
                f"❌ File is too large! Maximum size is {get_file_size_limit() // (1024*1024)}MB.",
                reply_markup=main_menu()
            )
            await state.clear()
            return
        
        # Download the image
        image_bytes = await file.download_bytes()
        
        # Show format options
        await message.answer(
            "🖼️ *Choose the output format:*",
            reply_markup=image_formats(),
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Store image bytes in state
        await state.update_data(image_bytes=image_bytes)
        
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        await message.answer(
            "❌ Error processing your image. Please try again.",
            reply_markup=main_menu()
        )
        await state.clear()

@router.message(StateFilter(ShortenURLStates.waiting_for_url))
async def handle_url_shortening(message: Message, state: FSMContext):
    """Handle URL shortening"""
    if message.text == "❌ Cancel":
        await cancel_command(message, state)
        return
    
    url = message.text.strip()
    
    # Basic URL validation
    if not url.startswith(('http://', 'https://')):
        await message.answer(
            "⚠️ Please send a valid URL starting with http:// or https://",
            reply_markup=cancel_keyboard()
        )
        return
    
    try:
        # Show processing message
        processing_msg = await message.answer("🔗 Shortening your URL... ⏳")
        
        # Shorten the URL
        short_url = await shorten_url(url)
        
        if short_url:
            await message.answer(
                f"🔗 *URL Shortened*\n\n"
                f"📎 Original: {url}\n"
                f"📏 Short: {short_url}\n\n"
                f"✅ Ready to share!",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=main_menu()
            )
        else:
            await message.answer(
                "❌ Failed to shorten the URL. Please try again.",
                reply_markup=main_menu()
            )
        
        await processing_msg.delete()
        
    except Exception as e:
        logger.error(f"Error shortening URL: {e}")
        await message.answer(
            "❌ Error shortening URL. Please try again.",
            reply_markup=main_menu()
        )
    
    await state.clear()
