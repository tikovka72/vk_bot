from constants import MIN_CHAT_PEER_ID, CHIEF_ADMIN
from utils import send_message, get_user_name


def get_admin(self, _, __, peer_id):
    if not peer_id > MIN_CHAT_PEER_ID:
        if peer_id == int(CHIEF_ADMIN) or self.redis.get_admin(peer_id) == 5:
            admins = self.redis.get_all_admins()
            if admins:
                admins_str = f"Всего админов: {len(admins)}\n"
                for (id_temp, access_level_temp) in admins:
                    name = get_user_name(int(id_temp), self.vk)
                    admins_str += f"{'@id'}{id_temp} ({name}) - {access_level_temp}\n"
                send_message(admins_str, self.vk, peer_id=peer_id)
            else:
                send_message("Список пуст", self.vk, peer_id=peer_id)
        else:
            send_message("У вас нет прав для этой команды", self.vk, peer_id=peer_id)