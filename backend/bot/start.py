from aiotg import Chat

from singletons.emanews import EmaNews

bot = EmaNews().bot


class TelegramLinkError(Exception):
    """
    Classe che rappresenta un errore di collegamento
    dell'account EmaNews a Telegram
    """
    pass


@bot.command(r"/start (.+)")
async def echo(chat: Chat, match):
    """
    Handler comando `/start` del bot telegram.
    Collega un account EmaNews ad un account Telegram.

    :param chat:
    :param match:
    :return:
    """
    try:
        token = match.group(1)
        async with EmaNews().db.acquire() as conn:
            async with conn.cursor() as cur:
                # Recupero user id da token
                await cur.execute("SELECT user_id FROM telegram_link_tokens WHERE token = %s LIMIT 1", (token,))
                activation_record = await cur.fetchone()
                if activation_record is None:
                    # Token non valido
                    raise TelegramLinkError("Token non valido o scaduto. Per favore, ripeti la procedura.")

                # Token valido, eliminalo e collega account EmaNews a Telegram
                await cur.execute("DELETE FROM telegram_link_tokens WHERE token = %s LIMIT 1", (token,))
                await cur.execute(
                    "UPDATE users SET telegram_user_id = %s WHERE id = %s LIMIT 1",
                    (chat.id, activation_record["user_id"])
                )
                await conn.commit()

        # Ok!
        await chat.send_text(
            "*👏 Congratulazioni!*\n"
            "Il tuo account EmaNews è stato collegato a questo account Telegram.\n"
            "Puoi scollegare i due account o quando e dove ricevere le notifiche dalla sezione 'Impostazioni notifiche'",
            parse_mode="markdown"
        )
    except TelegramLinkError as e:
        # Errore
        await chat.send_text(
            "*☹️ Si è verificato un errore!*\n"
            "Non è stato possibile completare la procedura a causa del seguente errore:\n"
            "```\n"
            "{}"
            "\n```".format(e),
            parse_mode="markdown"
        )
