from database.boards import Boards
from database.groups import Groups
from database.participants import Participants
from database.tickets import Tickets


groups_table = Groups.get_instance()
participants_table = Participants.get_instance()
tickets_table = Tickets.get_instance()
boards_table = Boards.get_instance()
