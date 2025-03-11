class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        
    def use(self, player, room):
        pass
        
class Key(Item):
    def __init__(self, door_id):
        super().__init__("Chave", "Uma chave que pode abrir portas trancadas")
        self.door_id = door_id
        
    def use(self, player, room):
        if room.has_locked_door(self.door_id):
            room.unlock_door(self.door_id)
            print("\nVocê destrancou uma porta!")
            return True
        print("\nNão há portas trancadas que esta chave possa abrir aqui.")
        return False
        
class Antidote(Item):
    def __init__(self):
        super().__init__("Antídoto", "Um antídoto que pode curar a infecção")
        
    def use(self, player, room):
        if player.is_infected:
            player.is_infected = False
            print("\nVocê usou o antídoto e se curou da infecção!")
            return True
        if room.has_infected_npc():
            room.cure_infected_npc()
            print("\nVocê curou um membro infectado da equipe!")
            return True
        print("\nNão há ninguém infectado para curar.")
        return False
        
class Ammo(Item):
    def __init__(self, amount=10):
        super().__init__("Munição", f"Munição para sua arma ({amount} balas)")
        self.amount = amount
        
    def use(self, player, room):
        if room.has_zombie():
            room.kill_zombie()
            print("\nVocê eliminou um zumbi!")
            self.amount -= 1
            if self.amount <= 0:
                print("\nSua munição acabou!")
                return True
            self.description = f"Munição para sua arma ({self.amount} balas)"
            return False
        print("\nNão há zumbis para atirar aqui.")
        return False
        
class MedKit(Item):
    def __init__(self):
        super().__init__("Kit Médico", "Um kit médico que recupera sua vida")
        
    def use(self, player, room):
        if player.health < 100:
            player.heal(50)
            return True
        print("\nSua vida já está cheia!")
        return False 