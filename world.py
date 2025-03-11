from item import Key, Antidote, Ammo, MedKit
import random
import time

class Event:
    def __init__(self, description, choices, consequences):
        self.description = description
        self.choices = choices  # Lista de strings descrevendo as escolhas
        self.consequences = consequences  # Lista de funções para cada escolha
        self.triggered = False
        
    def trigger(self, player, room):
        if self.triggered:
            return
            
        print(f"\n{self.description}")
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")
            
        while True:
            try:
                choice = int(input("\nEscolha uma opção: ")) - 1
                if 0 <= choice < len(self.choices):
                    self.consequences[choice](player, room)
                    self.triggered = True
                    break
                else:
                    print("Opção inválida!")
            except ValueError:
                print("Por favor, digite um número válido!")

class Room:
    def __init__(self, name, description, detailed_description=""):
        self.name = name
        self.description = description
        self.detailed_description = detailed_description or description
        self.items = []
        self.connections = {}
        self.locked_doors = set()
        self.has_zombie = False
        self.has_teammate = False
        self.teammate_infected = False
        self.events = []
        self.visited = False
        self.notes = []  # Documentos e anotações encontradas na sala
        
    def add_connection(self, direction, room, locked=False):
        self.connections[direction] = room
        if locked:
            self.locked_doors.add(direction)
            
    def add_item(self, item):
        self.items.append(item)
        
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
        
    def add_event(self, event):
        self.events.append(event)
        
    def add_note(self, note):
        self.notes.append(note)
        
    def examine(self):
        if not self.visited:
            print(f"\n{self.detailed_description}")
            self.visited = True
        else:
            print(f"\n{self.description}")
        
        if self.notes:
            print("\nDocumentos encontrados nesta sala:")
            for i, note in enumerate(self.notes, 1):
                print(f"{i}. {note['title']}")
            
            try:
                choice = input("\nDigite o número do documento para ler (ou ENTER para pular): ")
                if choice.isdigit() and 0 < int(choice) <= len(self.notes):
                    note = self.notes[int(choice)-1]
                    print(f"\n=== {note['title']} ===")
                    print(note['content'])
                    input("\nPressione ENTER para continuar...")
            except:
                pass
        
        if self.items:
            print("\nVocê vê os seguintes itens:")
            for item in self.items:
                print(f"- {item.name}")
                
        if self.has_zombie:
            print("\nCuidado! Há um zumbi nesta sala!")
            
        if self.has_teammate:
            if self.teammate_infected:
                print("\nVocê encontrou um membro da equipe, mas ele está infectado!")
            else:
                print("\nVocê encontrou um membro da equipe são e salvo!")
                
        # Trigger eventos não ativados
        for event in self.events:
            if not event.triggered:
                event.trigger(None, self)
                break
                
    def has_locked_door(self, direction):
        return direction in self.locked_doors
        
    def unlock_door(self, direction):
        if direction in self.locked_doors:
            self.locked_doors.remove(direction)
            
    def has_infected_npc(self):
        return self.has_teammate and self.teammate_infected
        
    def cure_infected_npc(self):
        if self.has_teammate and self.teammate_infected:
            self.teammate_infected = False
            
    def kill_zombie(self):
        self.has_zombie = False

class World:
    def __init__(self):
        self.rooms = self.create_map()
        self.current_room = self.rooms[0]  # Começa na entrada
        self.rescued_teammates = 0
        self.story_progress = 0
        
    def create_map(self):
        # Criar salas com descrições mais detalhadas
        rooms = [
            Room("Entrada", 
                "Você está na entrada do complexo da Empresa X. O lugar parece abandonado.",
                "A entrada da Empresa X é sombria e silenciosa. Papéis espalhados e manchas de sangue no chão sugerem que algo terrível aconteceu aqui. As luzes piscam intermitentemente, criando sombras inquietantes nas paredes."),
            
            Room("Recepção",
                "Uma recepção abandonada com um balcão de atendimento.",
                "A recepção está em completo caos. Computadores quebrados e documentos espalhados por todo lado. Atrás do balcão, uma tela ainda funciona, mostrando mensagens de erro em vermelho."),
            
            Room("Corredor Principal", 
                "Um longo corredor com várias portas. Há manchas de sangue no chão.",
                "O corredor se estende na penumbra, com portas em ambos os lados. O cheiro de produtos químicos mistura-se com um odor metálico. Manchas escuras no chão formam um rastro perturbador."),
            
            Room("Laboratório A", 
                "Um laboratório com equipamentos médicos. Tubos de ensaio quebrados por todo lado.",
                "Este laboratório parece ter sido palco de uma luta intensa. Equipamentos caros estão destruídos e substâncias químicas derramadas formam poças coloridas no chão. Em uma bancada, um microscópio ainda está ligado."),
            
            Room("Sala de Segurança", 
                "Uma sala com monitores mostrando diferentes partes do complexo.",
                "A sala de segurança oferece uma visão privilegiada do complexo através de dezenas de monitores. Alguns ainda funcionam, mostrando imagens perturbadoras de corredores vazios e laboratórios destruídos."),
            
            Room("Refeitório",
                "Um grande refeitório com mesas viradas e comida apodrecendo.",
                "O refeitório está em completo caos. Bandejas de comida abandonadas às pressas ainda estão nas mesas. Um cheiro pútrido vem da cozinha. Nas paredes, marcas de arranhões e sangue contam uma história terrível."),
            
            Room("Laboratório B", 
                "Outro laboratório, este com containeres de substâncias perigosas.",
                "Este laboratório parece ter sido usado para experimentos mais perigosos. Containeres com símbolos de risco biológico estão espalhados, alguns vazando um líquido fluorescente. Uma câmara de contenção quebrada sugere que algo escapou."),
            
            Room("Sala de Testes", 
                "Uma sala assustadora com macas médicas e equipamentos estranhos.",
                "A sala de testes é um pesadelo médico. Macas com correias de contenção manchadas de sangue alinham-se nas paredes. Equipamentos cirúrgicos e seringas usadas estão espalhados por todo lado. Um arquivo médico semi-queimado revela experimentos horríveis."),
            
            Room("Depósito", 
                "Um depósito escuro cheio de suprimentos médicos.",
                "O depósito está parcialmente escuro, iluminado apenas por uma luz de emergência vermelha. Prateleiras altas contêm suprimentos médicos e químicos. No fundo, uma porta de segurança pesada está entreaberta."),
            
            Room("Centro de Pesquisa", 
                "O centro principal de pesquisa, com documentos espalhados.",
                "O centro de pesquisa é um labirinto de estações de trabalho destruídas. Telas de computador piscam mostrando dados incompreensíveis. Uma parede de vidro rachada revela uma área de quarentena, e dentro dela, sinais de uma luta violenta."),
            
            Room("Laboratório Secreto",
                "Um laboratório oculto com equipamentos avançados.",
                "Este laboratório secreto claramente não constava nas plantas oficiais. Equipamentos de última geração e documentos confidenciais sugerem experimentos além dos limites éticos. Uma grande câmara criogênica domina o centro da sala."),
            
            Room("Sala do Reator", 
                "Uma sala com um grande reator no centro. Parece perigoso.",
                "A sala do reator é impressionante e aterrorizante. O reator principal pulsa com uma energia estranha, emitindo um zumbido baixo. Painéis de controle piscam alertas em vermelho. Este deve ser o local onde tudo começou.")
        ]
        
        # Adicionar documentos e notas em várias salas
        rooms[1].add_note({
            "title": "E-mail Urgente",
            "content": "Para: Todos os funcionários\nDe: Direção\nAssunto: EVACUAÇÃO IMEDIATA\n\nDevido a um incidente no Laboratório B, todos os funcionários devem evacuar o prédio imediatamente. Não tente levar pertences pessoais. Siga os protocolos de contenção. Este não é um exercício."
        })
        
        rooms[3].add_note({
            "title": "Relatório de Pesquisa #127",
            "content": "Os resultados são promissores. A cura para o câncer está próxima, mas os efeitos colaterais são... preocupantes. Os pacientes do teste mostram sinais de agressividade aumentada e deterioração mental. Precisamos de mais testes antes de..."
        })
        
        rooms[6].add_note({
            "title": "Diário do Dr. Martinez",
            "content": "Dia 45: Algo deu terrivelmente errado. O vírus mutou de uma forma que não previmos. Os pacientes... eles não são mais humanos. Precisamos conter isso antes que... [o resto está manchado de sangue]"
        })
        
        # Criar eventos
        def event_refeitorio(player, room):
            print("\nAo explorar o refeitório, você ouve um barulho vindo da cozinha.")
            print("1. Investigar o barulho")
            print("2. Ignorar e continuar")
            choice = input("O que você quer fazer? ")
            if choice == "1":
                print("\nVocê encontra um sobrevivente escondido! Ele te entrega um kit médico antes de fugir.")
                room.add_item(MedKit())
            else:
                print("\nVocê decide não arriscar. O barulho eventualmente para.")
                
        def event_lab_secreto(player, room):
            print("\nVocê encontra um computador desbloqueado com informações cruciais.")
            print("1. Baixar os dados (demora alguns minutos)")
            print("2. Continuar procurando")
            choice = input("O que você quer fazer? ")
            if choice == "1":
                print("\nEnquanto os dados são baixados, um zumbi te ataca!")
                room.has_zombie = True
            else:
                print("\nVocê decide que não há tempo a perder.")
                
        # Adicionar eventos às salas
        rooms[5].add_event(Event(
            "Você ouve um grito de socorro vindo de um armário trancado!",
            ["Arrombar o armário", "Ignorar e seguir em frente"],
            [
                lambda p, r: (print("\nVocê encontra um cientista ferido que te dá informações importantes sobre o antídoto."), r.add_note({
                    "title": "Anotações do Cientista",
                    "content": "O antídoto precisa ser liberado através do sistema de ventilação do reator. É a única forma de atingir todo o complexo!"
                })),
                lambda p, r: print("\nVocê decide não arriscar. Os gritos eventualmente param...")
            ]
        ))
        
        # Conectar salas
        rooms[0].add_connection("norte", rooms[1])
        rooms[1].add_connection("sul", rooms[0])
        rooms[1].add_connection("norte", rooms[2])
        rooms[1].add_connection("leste", rooms[5])
        
        rooms[2].add_connection("sul", rooms[1])
        rooms[2].add_connection("leste", rooms[3])
        rooms[2].add_connection("oeste", rooms[4], True)
        
        rooms[3].add_connection("oeste", rooms[2])
        rooms[3].add_connection("norte", rooms[6])
        
        rooms[4].add_connection("leste", rooms[2])
        rooms[4].add_connection("norte", rooms[8])
        
        rooms[5].add_connection("oeste", rooms[1])
        rooms[5].add_connection("norte", rooms[6])
        
        rooms[6].add_connection("sul", rooms[3])
        rooms[6].add_connection("sul", rooms[5])
        rooms[6].add_connection("leste", rooms[7], True)
        
        rooms[7].add_connection("oeste", rooms[6])
        rooms[7].add_connection("norte", rooms[9])
        
        rooms[8].add_connection("sul", rooms[4])
        rooms[8].add_connection("leste", rooms[9])
        
        rooms[9].add_connection("oeste", rooms[8])
        rooms[9].add_connection("sul", rooms[7])
        rooms[9].add_connection("leste", rooms[10], True)
        
        rooms[10].add_connection("oeste", rooms[9])
        rooms[10].add_connection("norte", rooms[11], True)
        
        rooms[11].add_connection("sul", rooms[10])
        
        # Adicionar itens estrategicamente
        rooms[1].add_item(MedKit())
        rooms[3].add_item(Key("oeste"))  # Chave para a Sala de Segurança
        rooms[4].add_item(Ammo())
        rooms[6].add_item(Key("leste"))  # Chave para a Sala de Testes
        rooms[7].add_item(Antidote())
        rooms[8].add_item(MedKit())
        rooms[9].add_item(Key("leste"))  # Chave para o Lab Secreto
        rooms[10].add_item(Key("norte"))  # Chave para a Sala do Reator
        
        # Adicionar zumbis e membros da equipe
        rooms[3].has_zombie = True
        rooms[5].has_zombie = True
        rooms[7].has_zombie = True
        rooms[10].has_zombie = True
        
        rooms[4].has_teammate = True
        rooms[6].has_teammate = True
        rooms[8].has_teammate = True
        rooms[9].has_teammate = True
        rooms[9].teammate_infected = True
        
        return rooms
        
    def get_available_directions(self):
        return [direction for direction in self.current_room.connections.keys()
                if direction not in self.current_room.locked_doors]
                
    def move_player(self, direction):
        if direction in self.current_room.locked_doors:
            print("\nEsta porta está trancada! Você precisa de uma chave.")
            return 0
            
        if direction in self.current_room.connections:
            self.current_room = self.current_room.connections[direction]
            print(f"\nVocê se moveu para: {self.current_room.name}")
            
            if self.current_room.has_zombie:
                damage = random.randint(10, 25)
                print("\nUm zumbi te atacou!")
                return damage
                
            # Chance de encontrar um item escondido
            if not self.current_room.visited and random.random() < 0.3:
                if random.random() < 0.5:
                    self.current_room.add_item(MedKit())
                    print("\nVocê encontrou um kit médico escondido!")
                else:
                    self.current_room.add_item(Ammo())
                    print("\nVocê encontrou munição escondida!")
        return 0
        
    def check_win_condition(self, player):
        if self.current_room == self.rooms[-1]:  # Sala do Reator
            for item in player.inventory:
                if isinstance(item, Antidote):
                    # Verifica diferentes condições para diferentes finais
                    if self.rescued_teammates >= 3:
                        print("\nFINAL PERFEITO: Você salvou a maioria da sua equipe e liberou o antídoto!")
                        print("O complexo inteiro é curado, e sua equipe sobrevive para contar a história.")
                    elif self.rescued_teammates >= 1:
                        print("\nFINAL BOM: Você liberou o antídoto e salvou alguns membros da equipe.")
                        print("A cura se espalha pelo complexo, mas o custo em vidas foi alto.")
                    else:
                        print("\nFINAL AGRIDOCE: Você liberou o antídoto, mas não conseguiu salvar sua equipe.")
                        print("A humanidade está a salvo, mas a que custo?")
                    return True
        return False 