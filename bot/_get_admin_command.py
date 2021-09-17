from constants import MIN_CHAT_PEER_ID, CHIEF_ADMIN
from my_vk_api import get_user_name

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Bot


def get_admin(self: 'Bot', _, __, peer_id: int):
    if not peer_id > MIN_CHAT_PEER_ID:
        if peer_id == int(CHIEF_ADMIN) or self.redis.get_admin(peer_id) == 5:
            admins = self.redis.get_all_admins()
            if admins:
                admins_str = f"Всего админов: {len(admins)}\n"
                for (id_temp, access_level_temp) in admins:
                    name = get_user_name(int(id_temp), self.vk)
                    admins_str += f"{'@id'}{id_temp} ({name}) - {access_level_temp}\n"
                self.send_message(admins_str, str(peer_id))
            else:
                self.send_message("Список пуст", str(peer_id))
        else:
            self.send_message("У вас нет прав для этой команды", str(peer_id))
