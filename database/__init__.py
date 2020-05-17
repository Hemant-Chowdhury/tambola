from database.boards_table import Boards
from database.groups_table import Groups
from database.participants_table import Participants
from database.tickets_table import Tickets


groups_table = Groups.get_instance()
participants_table = Participants.get_instance()
tickets_table = Tickets.get_instance()
boards_table = Boards.get_instance()
