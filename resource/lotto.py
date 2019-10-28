import datetime
import resource.utility as optim

class Ticket_Lotto:
    def __init__(self,guild_id):
        lotto_dict = optim.loader()
        
        class Ticket:
            def __init__(self):
                self.draw_date = datetime.datetime.now()
                self.ticket_number = lotto_dict.tickets_sold + 1*/
                self.draw_pick = lotto_dict
