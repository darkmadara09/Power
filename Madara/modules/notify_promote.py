from Madara import pgram

@pgram.on_chat_member_updated()
async def handler(_, cmu):
    txt = ""
    if cmu.old_chat_member:
        if cmu.old_chat_member.status.name == "MEMBER":
            if cmu.new_chat_member:
                if cmu.new_chat_member.status.name == "ADMINISTRATOR":
                    m1 = f"[{cmu.from_user.first_name}](tg://user?id={cmu.from_user.id})"
                    m2 = f"[{cmu.new_chat_member.user.first_name}](tg://user?id={cmu.new_chat_member.user.id})"
                    txt = f"{m2} was promoted by {m1}."
        elif cmu.old_chat_member.status.name == "ADMINISTRATOR":
            if cmu.new_chat_member:
                if cmu.new_chat_member.status.name == "MEMBER":
                    m1 = f"[{cmu.from_user.first_name}](tg://user?id={cmu.from_user.id})"
                    m2 = f"[{cmu.new_chat_member.user.first_name}](tg://user?id={cmu.new_chat_member.user.id})"
                    txt = f"{m2} was demoted by {m1}."
    if txt:
        await _.send_message(cmu.chat.id, txt)
