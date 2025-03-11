from player import Player
from world import World
from item import Item, Antidote
import os
import time
import sys
import random

# Cores ANSI
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'

def print_slow(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_with_effect(text, color=Colors.ENDC, effect="", delay=0.03):
    print_slow(f"{color}{effect}{text}{Colors.ENDC}", delay)

def animate_title():
    title = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║  ██╗   ██╗███╗   ███╗ █████╗      ██████╗██╗   ██╗██████╗  █████╗         ║
    ║  ██║   ██║████╗ ████║██╔══██╗    ██╔════╝██║   ██║██╔══██╗██╔══██╗        ║
    ║  ██║   ██║██╔████╔██║███████║    ██║     ██║   ██║██████╔╝███████║        ║
    ║  ██║   ██║██║╚██╔╝██║██╔══██║    ██║     ██║   ██║██╔══██╗██╔══██║        ║
    ║  ╚██████╔╝██║ ╚═╝ ██║██║  ██║    ╚██████╗╚██████╔╝██║  ██║██║  ██║        ║
    ║   ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝        ║
    ║                                                                              ║
    ║  ██████╗ ███████╗███████╗ █████╗ ███████╗████████╗██████╗  ██████╗ ███████╗║
    ║  ██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗██╔════╝║
    ║  ██║  ██║█████╗  ███████╗███████║███████╗   ██║   ██████╔╝██║   ██║███████╗║
    ║  ██║  ██║██╔══╝  ╚════██║██╔══██║╚════██║   ██║   ██╔══██╗██║   ██║╚════██║║
    ║  ██████╔╝███████╗███████║██║  ██║███████║   ██║   ██║  ██║╚██████╔╝███████║║
    ║  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝║
    ║                                                                              ║
    ║                    🧪 SOBREVIVA AO APOCALIPSE ZUMBI 🧟                      ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """
    colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.HEADER]
    for color in colors:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{color}{title}{Colors.ENDC}")
        time.sleep(0.2)
    time.sleep(1)

def animate_death():
    death_screen = """
      ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄       ▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░▌     ▐░░▌▐░░░░░░░░░░░▌
     ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░▌░▌   ▐░▐░▌▐░█▀▀▀▀▀▀▀▀▀ 
     ▐░▌          ▐░▌       ▐░▌▐░▌▐░▌ ▐░▌▐░▌▐░▌          
     ▐░▌ ▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░▌ ▐░▐░▌ ▐░▌▐░█▄▄▄▄▄▄▄▄▄ 
     ▐░▌▐░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌  ▐░▌▐░░░░░░░░░░░▌
     ▐░▌ ▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌   ▀   ▐░▌▐░█▀▀▀▀▀▀▀▀▀ 
     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          
     ▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄ 
     ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌
      ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀ 
    """
    for _ in range(3):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Colors.RED}{death_screen}{Colors.ENDC}")
        time.sleep(0.5)
        os.system('cls' if os.name == 'nt' else 'clear')
        time.sleep(0.5)

def animate_victory():
    victory_screen = """
    ██╗   ██╗██╗████████╗ ██████╗ ██████╗ ██╗ █████╗ ██╗
    ██║   ██║██║╚══██╔══╝██╔═══██╗██╔══██╗██║██╔══██╗██║
    ██║   ██║██║   ██║   ██║   ██║██████╔╝██║███████║██║
    ╚██╗ ██╔╝██║   ██║   ██║   ██║██╔══██╗██║██╔══██║╚═╝
     ╚████╔╝ ██║   ██║   ╚██████╔╝██║  ██║██║██║  ██║██╗
      ╚═══╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝
    """
    colors = [Colors.GREEN, Colors.CYAN, Colors.YELLOW]
    for _ in range(5):
        for color in colors:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{color}{victory_screen}{Colors.ENDC}")
            time.sleep(0.2)

class Game:
    def __init__(self):
        self.player = Player()
        self.world = World()
        self.is_running = True
        self.turn_count = 0
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_header(self):
        print(f"\n{Colors.CYAN}{'=' * 50}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.YELLOW}=== Uma Cura Desastrosa ==={Colors.ENDC}".center(50))
        print(f"{Colors.CYAN}{'=' * 50}{Colors.ENDC}")
        
    def print_status(self):
        health_color = Colors.GREEN if self.player.health > 70 else Colors.YELLOW if self.player.health > 30 else Colors.RED
        print(f"\n{Colors.BOLD}Vida:{Colors.ENDC} {health_color}{'♥' * (self.player.health // 10)}{Colors.ENDC}")
        
        status_text = "INFECTADO!" if self.player.is_infected else "Saudável"
        status_color = Colors.RED if self.player.is_infected else Colors.GREEN
        print(f"{Colors.BOLD}Status:{Colors.ENDC} {status_color}{status_text}{Colors.ENDC}")
        
        print(f"{Colors.BOLD}Localização:{Colors.ENDC} {Colors.CYAN}{self.world.current_room.name}{Colors.ENDC}")
        print(f"{Colors.BOLD}Membros da equipe resgatados:{Colors.ENDC} {Colors.GREEN}{self.world.rescued_teammates}{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}Inventário:{Colors.ENDC}")
        self.player.show_inventory()
        
    def show_intro(self):
        self.clear_screen()
        animate_title()
        
        print_with_effect("\nO ano é 2024. A Empresa X, uma corporação farmacêutica secreta,", Colors.CYAN)
        print_with_effect("estava próxima de desenvolver a cura para o câncer.", Colors.CYAN)
        time.sleep(1)
        
        print_with_effect("\nMas algo deu terrivelmente errado...", Colors.RED, Colors.BOLD)
        time.sleep(1)
        
        print_with_effect("\nOs pacientes de teste se transformaram em criaturas violentas,", Colors.YELLOW)
        print_with_effect("e a infecção começou a se espalhar pelo complexo.", Colors.YELLOW)
        time.sleep(1)
        
        print_with_effect("\nVocê é parte de uma equipe de forças especiais enviada para investigar.", Colors.CYAN)
        print_with_effect("Mas ao entrar no complexo, você se separa do resto da equipe.", Colors.CYAN)
        time.sleep(1)
        
        print_with_effect(f"\n{Colors.BOLD}Sua missão:{Colors.ENDC}")
        print_with_effect("- Encontrar e resgatar sua equipe", Colors.GREEN)
        print_with_effect("- Descobrir o que aconteceu", Colors.GREEN)
        print_with_effect("- Impedir que a infecção se espalhe", Colors.GREEN)
        print_with_effect("- Sobreviver...", Colors.RED, Colors.BOLD)
        time.sleep(1)
        
        input(f"\n{Colors.YELLOW}Pressione ENTER para começar sua missão...{Colors.ENDC}")
        
    def get_input(self):
        print(f"\n{Colors.BOLD}Ações disponíveis:{Colors.ENDC}")
        actions = [
            "Mover",
            "Examinar sala",
            "Pegar item",
            "Usar item",
            "Ver inventário",
            "Ler documentos",
            "Sair"
        ]
        
        for i, action in enumerate(actions, 1):
            print(f"{Colors.CYAN}{i}. {action}{Colors.ENDC}")
        
        return input(f"\n{Colors.YELLOW}Escolha uma ação (1-7): {Colors.ENDC}")
    
    def handle_movement(self):
        print(f"\n{Colors.BOLD}Direções disponíveis:{Colors.ENDC}")
        directions = self.world.get_available_directions()
        for i, direction in enumerate(directions, 1):
            print(f"{Colors.CYAN}{i}. {direction}{Colors.ENDC}")
        
        choice = input(f"\n{Colors.YELLOW}Escolha uma direção (ou 0 para voltar): {Colors.ENDC}")
        if choice.isdigit() and 0 <= int(choice) <= len(directions):
            if choice == "0":
                return
            damage = self.world.move_player(directions[int(choice) - 1])
            if damage > 0:
                print_with_effect("ATAQUE ZUMBI!", Colors.RED, Colors.BLINK)
                self.player.take_damage(damage)
            
    def handle_examine(self):
        self.world.current_room.examine()
        
    def handle_take_item(self):
        items = self.world.current_room.items
        if not items:
            print(f"\n{Colors.RED}Não há itens para pegar nesta sala.{Colors.ENDC}")
            return
            
        print(f"\n{Colors.BOLD}Itens disponíveis:{Colors.ENDC}")
        for i, item in enumerate(items, 1):
            print(f"{Colors.CYAN}{i}. {item.name}{Colors.ENDC}")
            
        choice = input(f"\n{Colors.YELLOW}Escolha um item para pegar (ou 0 para voltar): {Colors.ENDC}")
        if choice.isdigit() and 0 <= int(choice) <= len(items):
            if choice == "0":
                return
            item = items[int(choice) - 1]
            if self.player.add_item(item):
                self.world.current_room.remove_item(item)
                print_with_effect(f"Você pegou: {item.name}", Colors.GREEN)
                
    def handle_use_item(self):
        if not self.player.inventory:
            print(f"\n{Colors.RED}Você não tem itens para usar.{Colors.ENDC}")
            return
            
        print(f"\n{Colors.BOLD}Itens no inventário:{Colors.ENDC}")
        self.player.show_inventory()
        
        choice = input(f"\n{Colors.YELLOW}Escolha um item para usar (ou 0 para voltar): {Colors.ENDC}")
        if choice.isdigit() and 0 <= int(choice) <= len(self.player.inventory):
            if choice == "0":
                return
            item = self.player.inventory[int(choice) - 1]
            self.player.use_item(item, self.world.current_room)
            
    def handle_read_documents(self):
        if not self.world.current_room.notes:
            print(f"\n{Colors.RED}Não há documentos para ler nesta sala.{Colors.ENDC}")
            return
            
        print(f"\n{Colors.BOLD}Documentos disponíveis:{Colors.ENDC}")
        for i, note in enumerate(self.world.current_room.notes, 1):
            print(f"{Colors.CYAN}{i}. {note['title']}{Colors.ENDC}")
            
        choice = input(f"\n{Colors.YELLOW}Escolha um documento para ler (ou 0 para voltar): {Colors.ENDC}")
        if choice.isdigit() and 0 <= int(choice) <= len(self.world.current_room.notes):
            if choice == "0":
                return
            note = self.world.current_room.notes[int(choice) - 1]
            print(f"\n{Colors.BOLD}=== {note['title']} ==={Colors.ENDC}")
            print_with_effect(note['content'], Colors.CYAN, delay=0.02)
            
    def check_game_over(self):
        if self.player.health <= 0:
            animate_death()
            print_with_effect("\nFINAL RUIM: Você sucumbiu aos seus ferimentos.", Colors.RED, Colors.BOLD)
            print_with_effect("Sua missão falhou, e a infecção continua se espalhando...", Colors.RED)
            return True
            
        if self.player.is_infected and not any(isinstance(item, Antidote) for item in self.player.inventory):
            animate_death()
            print_with_effect("\nFINAL RUIM: Você foi infectado e não tem antídoto.", Colors.RED, Colors.BOLD)
            print_with_effect("Lentamente, você se transforma em mais um dos infectados...", Colors.RED)
            return True
            
        if self.world.check_win_condition(self.player):
            animate_victory()
            return True
            
        return False
    
    def run(self):
        self.show_intro()
        
        while self.is_running:
            self.clear_screen()
            self.print_header()
            self.print_status()
            
            if self.player.is_infected:
                self.player.update_infection()
            
            action = self.get_input()
            
            if action == "1":
                self.handle_movement()
            elif action == "2":
                self.handle_examine()
            elif action == "3":
                self.handle_take_item()
            elif action == "4":
                self.handle_use_item()
            elif action == "5":
                self.player.show_inventory()
            elif action == "6":
                self.handle_read_documents()
            elif action == "7":
                self.is_running = False
                print(f"\n{Colors.YELLOW}Jogo encerrado.{Colors.ENDC}")
                break
                
            self.turn_count += 1
            
            # Eventos aleatórios baseados no número de turnos
            if self.turn_count % 5 == 0 and random.random() < 0.3:
                if random.random() < 0.5:
                    print_with_effect("\nVocê ouve gritos distantes ecoando pelos corredores...", Colors.RED, Colors.DIM)
                else:
                    print_with_effect("\nUm barulho metálico ressoa pelo complexo...", Colors.YELLOW, Colors.DIM)
                
            if self.check_game_over():
                self.is_running = False
                break
                
            input(f"\n{Colors.YELLOW}Pressione ENTER para continuar...{Colors.ENDC}")

if __name__ == "__main__":
    game = Game()
    game.run() 