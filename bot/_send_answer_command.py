import json

from constants import MIN_CHAT_PEER_ID, HUY_CHANCE, ANSWER_CHANCE, GROUP_ID, KEYBOARDS
from utils import what_answer, generate_huy_word, get_main_pos


def send_answer(self, event, message, peer_id):
    if not peer_id > MIN_CHAT_PEER_ID:
        old = self.redis.check_peer_id(str(peer_id))
        if not old:
            self.redis.add_peer_id(str(peer_id))
            self.send_message("Напиши /help, "
                              "чтобы узнать список команд", peer_id=peer_id,
                              keyboard=json.loads(KEYBOARDS)["help_keyboard"])
        else:
            self.send_message("в лс делаю только "
                              "смешнявки, отвечаю в беседе", peer_id)
    else:
        action = event.obj["message"].get("action", 0)
        if action:
            if action["type"] == "chat_invite_user" and \
                    action["member_id"] == -int(GROUP_ID):
                self.redis.add_peer_id(str(peer_id))
                self.send_message("Дайте права админа пожалуйста "
                                  "а то я вас не слышу я глухой", peer_id=peer_id)
        else:
            self.speaker.add_words(peer_id, message)
            what = what_answer(message, chances={
                ANSWER_CHANCE: self.redis.get_answer_chance(str(peer_id)),
                HUY_CHANCE: self.redis.get_huy_chance(str(peer_id))
            })
            if what == ANSWER_CHANCE:
                text = self.speaker.generate_text(peer_id, "")
                if text:
                    self.send_message(text, peer_id)
            elif what == HUY_CHANCE:
                self.send_message(generate_huy_word(get_main_pos(message)), peer_id)
