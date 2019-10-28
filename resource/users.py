import resource.utility as optim
from discord import TextChannel

class User:
    def __init__(self,discord_user):

        user_dict = optim.loader("dmb", discord_user.id, "users")
        
        if user_dict != {}:
            self.reputation = user_dict["reputation"]
            self.warnings = user_dict["warnings"]
            self.message_count = user_dict["message_count"]
            self.level = user_dict["level"]
            self.time_on_server = user_dict["time_on_server"]
        else:
            self.reputation = 0
            self.warnings = []
            self.message_count = 0
            self.level = 0
            if
            self.time_on_server = 

    def update(self,message):
        self.__init__(message)
        self.message_count += 1
        if self.message_count == (self.level ** 2)*100:
            self.level += 1
        if message.channel is 

    def save(self):
        optim.saver(self.__dict__, "dmb", self.__name__, "users")
