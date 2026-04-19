from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from config.config import TOKEN
from users.users import start, check_subscription_callback, handle_message, handle_stats, contact_admin
from admin.admin import add_movie_start, get_code, get_video, get_title, save_movie, cancel, edit_movie_start, get_edit_code, get_new_title, save_updated_movie

from state import VIDEO, CODE, TITLE, DESCRIPTION, EDIT_CODE, NEW_TITLE, NEW_DESC


def main():
    app = ApplicationBuilder().token(TOKEN).build()


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add", add_movie_start)],
        states={
            VIDEO: [MessageHandler(filters.VIDEO, get_video)],
            CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_code)],
            TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_title)],
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_movie)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
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
)

    app.add_handler(edit_conv)

    

 
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_subscription_callback, pattern="check_sub"))
    app.add_handler(MessageHandler(filters.Regex("📊 Statistika"), handle_stats))
    app.add_handler(MessageHandler(filters.Regex("📞 Admin bilan bog‘lanish"), contact_admin))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


    print("Bot Running...")

    app.run_polling()


if __name__ == "__main__":
    main()