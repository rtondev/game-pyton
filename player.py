import random

class Player:
    def __init__(self):
        self.health = 100
        self.inventory = []
        self.max_inventory = 5
        self.is_infected = False
        self.infection_timer = 0
        self.infection_max_time = 10  # Turnos até a infecção se tornar fatal
        
    def add_item(self, item):
        if len(self.inventory) >= self.max_inventory:
            print("\nInventário cheio! Você não pode carregar mais itens.")
            print("Você precisa descartar algo primeiro.")
            return False
        self.inventory.append(item)
        print(f"\nVocê pegou: {item.name}")
        return True
        
    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
        
    def show_inventory(self):
        if not self.inventory:
            print("Inventário vazio")
            return
            
        for i, item in enumerate(self.inventory, 1):
            print(f"{i}. {item.name} - {item.description}")
            
    def use_item(self, item, current_room):
        if item.use(self, current_room):
            self.remove_item(item)
            if current_room.has_teammate and not current_room.teammate_infected:
                current_room.has_teammate = False
                print("\nO membro da equipe decide te acompanhar!")
                current_room.world.rescued_teammates += 1
            
    def take_damage(self, amount):
        self.health -= amount
        print(f"\nVocê sofreu {amount} de dano!")
        
        # Chance de infecção ao ser atacado
        if not self.is_infected and random.random() < 0.3:
            self.is_infected = True
            self.infection_timer = self.infection_max_time
            print("\nVocê foi infectado! Precisa encontrar um antídoto rapidamente!")
        
    def heal(self, amount):
        old_health = self.health
        self.health = min(100, self.health + amount)
        healed = self.health - old_health
        print(f"\nVocê recuperou {healed} de vida!")
        
    def update_infection(self):
        if self.is_infected:
            self.infection_timer -= 1
            if self.infection_timer <= 0:
                print("\nA infecção está se espalhando! Você perde 10 de vida!")
                self.take_damage(10)
            elif self.infection_timer <= 3:
                print(f"\nAVISO: Você tem apenas {self.infection_timer} turnos antes da infecção se tornar crítica!") 