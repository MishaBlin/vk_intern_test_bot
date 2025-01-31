import vk_api
from os import getenv
from dotenv import load_dotenv
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def get_formatted_photos(attachments):
    formatted = []
    for atch in attachments:
        if atch["type"] == "photo":
            photo_data = atch["photo"]
            owner_id = photo_data["owner_id"]
            atch_id = photo_data["id"]
            access_key = photo_data["access_key"]
            formatted.append(f"photo{owner_id}_{atch_id}_{access_key}")
    return ",".join(formatted)


def send_photos(vk, user_id, reply_to, photos):
    vk.method("messages.send", {"user_id": user_id, "reply_to": reply_to, "attachment": photos, "random_id": 0})


def main():
    vk_session = vk_api.VkApi(token=getenv("TOKEN"))
    longpoll = VkBotLongPoll(vk_session, group_id=getenv("GROUP_ID"))

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.object["message"]
            user_id = message["from_id"]
            reply_to = message["id"]
            attachments = message.get("attachments")

            formatted_photos = get_formatted_photos(attachments)
            if formatted_photos:
                send_photos(vk_session, user_id, reply_to, formatted_photos)


if __name__ == '__main__':
    load_dotenv()
    main()
