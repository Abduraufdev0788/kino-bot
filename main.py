import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from config.config import TOKEN
from database.db import init_db
from users.users import start, check_subscription_callback, handle_message, handle_stats, contact_admin
from admin.admin import add_movie_start, get_code, get_video, get_title, save_movie, cancel, edit_movie_start, get_edit_code, get_new_title, save_updated_movie, broadcast_start, broadcast_send, delete_movie_start, delete_movie_confirm

from state import VIDEO, CODE, TITLE, DESCRIPTION, EDIT_CODE, NEW_TITLE, NEW_DESC, BROADCAST_MSG, DELETE_CODE


async def post_init(application):
    await init_db()


def main():
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()


    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("add", add_movie_start),
            MessageHandler(filters.Regex("^➕ Kino qo'shish$"), add_movie_start)
        ],
        states={
            VIDEO: [MessageHandler(filters.VIDEO, get_video)],
            CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_code)],
            TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_title)],
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_movie)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )

    app.add_handler(conv_handler)


    edit_conv = ConversationHandler(
    entry_points=[CommandHandler("edit", edit_movie_start)],
    states={
        EDIT_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_edit_code)],
        NEW_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_new_title)],
        NEW_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_updated_movie)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    allow_reentry=True,
)

    app.add_handler(edit_conv)
    
    delete_conv = ConversationHandler(
        entry_points=[
            CommandHandler("delete", delete_movie_start),
            MessageHandler(filters.Regex("^🗑 Kino o'chirish$"), delete_movie_start)
        ],
        states={
            DELETE_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_movie_confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )
    app.add_handler(delete_conv)
    
    broadcast_conv = ConversationHandler(
        entry_points=[
            CommandHandler("reklama", broadcast_start), 
            CommandHandler("broadcast", broadcast_start),
            MessageHandler(filters.Regex("^📣 Reklama joylash$"), broadcast_start)
        ],
        states={
            BROADCAST_MSG: [MessageHandler(filters.ALL & ~filters.COMMAND, broadcast_send)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )
    app.add_handler(broadcast_conv)
    

 
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_subscription_callback, pattern="check_sub"))
    app.add_handler(MessageHandler(filters.Regex("^📊 Statistika$"), handle_stats))
    app.add_handler(MessageHandler(filters.Regex("^📞 Admin bilan bog‘lanish$"), contact_admin))
    from users.users import movie_codes, advertise_contact
    app.add_handler(MessageHandler(filters.Regex("^🎬 Kino kodlari$"), movie_codes))
    app.add_handler(MessageHandler(filters.Regex("^💰 Reklama yuborish$"), advertise_contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


    print("Bot Running...")

    app.run_polling()


if __name__ == "__main__":
    main()