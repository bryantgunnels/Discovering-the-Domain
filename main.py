import asyncio
from pathlib import Path
import pygame

WIDTH, HEIGHT = 900, 600
BASE_DIR = Path(__file__).parent
ASSET_DIR = BASE_DIR / "assets"


class NPC:
    def __init__(self, name, speech, value):
        self.name = name
        self.speech = speech
        self.value = value

class Treasure:
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

class Book:
    def __init__(self, name, description, value):
            self.name = name
            self.description = description

class Bell:
   def __init__(self, name, value):
            self.name = name
            self.value = value


class Food:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Room:
    def __init__(self, name, description, enter_sound=None):
        self.name = name
        self.description = description
        self.enter_sound = enter_sound
        self.neighbors = {}
        self.treasure = []
        self.monster = None
        self.weapon = None
        self.npc = []
        self.food = []
        self.book = []

    def add_neighbor(self, direction, room):
        self.neighbors[direction] = room

    def get_neighbor(self, direction):
        return self.neighbors.get(direction)

    def list_exits(self):
        return ", ".join(self.neighbors.keys())

class TextAdventure:
    def __init__(self):
        self.messages = []
        self.current_input = ""
        self.score = 0
        self.best_weapon_damage = 3
        self.game_over = False

        self.sounds = {
            "Open": pygame.mixer.Sound(ASSET_DIR / "move.ogg"),
            "move": pygame.mixer.Sound(ASSET_DIR / "move.ogg"),
            "pickup": pygame.mixer.Sound(ASSET_DIR / "pickup.ogg"),
            "danger": pygame.mixer.Sound(ASSET_DIR / "danger.ogg"),
            "win": pygame.mixer.Sound(ASSET_DIR / "win.ogg"),
            "organ": pygame.mixer.Sound(ASSET_DIR / "organ.ogg"),
            "bell": pygame.mixer.Sound(ASSET_DIR / "bell.ogg"),
        }

        #add Rooms
        chaple = Room(
            "All Saints Chaple",
            "The sheer scale of the gothic architecture presses in: soaring stone archways stretch upward, gorgeous stained glass glows as the sun hits the windows at the right angle, and the ambient scent of old hymnals and polished wood fills your lungs. Your attention fades from the building towards the person playing the organ.")
        quad = Room(
            "The Quad",
            "You step onto the Quad, a wide grassy space surrounded by Sewanee’s stone buildings. With the campus empty, the paths and benches are completely still, making the Quad feel peaceful but a little strange. A few benches sit beneath the trees, and academic buildings surround the open lawn. On one bench, you notice a single person with a notebook beside a small sign that reads “Riddle of the Day. There is also a painter who is hard a work on her next piece")
        library = Room(
            "DuPont Library",
            "a beautiful 3 story library")
        breslin = Room(
            "Breslin Tower",
            "As you walk up to the front door and you quickly realize the door handles have a chain around them with a lock that has a number key pad. hint: what year was The University of the South founded")
        behil = Room(
            "Behli Commons",
            "the living room of campus")
        clurg = Room(
            "You are in Mclurg Dining Hall",
            "The smell of fresh food and the view of rows of completely empty tables, and the usual sounds of conversation and dishes are gone. The food stations are still up around the room, making the silence feel even stranger. Near the entrance, one person sits at a desk with computers and an ID scanner, waiting he adons a name tag stating his name is Jack.")
        svfd = Room(
            "Sewanee Fire Station",
            "The Sewanee Volunteer Fire Department. One of 2 student ran fire departments in the country")
        bishop = Room(
            "Bishop's Common",
            "You approach Bishop Commons and briskly walk inside, excited to see what dorm you will be living in! As you walk inside you follow the signs directing you to talk to the reslife office.")
        benny = Room(
            "Benedict Hall",
            "The best dorm on campus. Be careful it can get a little rowdy in the courtyard.")
        delt = Room(
            "Delt",
            "Delta Tau Delta Fraternity. The band comes on in 10 mins and the dancefloor inside is packed!")
        ka = Room(
            "KA",
            "The Kappa Alpha Order.")
        snu = Room(
            "SNU",
            "Sigma Nu Fraternity. The party is going strong in the frontyard!")
        fowler = Room(
            "Fowler Center",
            "The athletics center. Vollyball is about to play in Juhan gym and football is practicing on the field. \
            and make sure to check out the state of the art equestrian facility!")
        alley = Room(
            "Abo's Alley",
            "Abo's Alley. The entrance to the wilderness. Make sure to check out the trails and the beautiful view of the valley!")
        downtown = Room(
            "Downtown Sewanee",
            "our tiny downtown. Make sure to check out the bookstore or grab an burger at shananagains.")
        cross = Room(
            "The War Memorial Cross",
            "The Most Beautiful Place on the Domain")
        homestyle = Room(
            "the Homestyle line today we are serving, Halal Baked Chicken, Jerk Pork Chops, Basmati Ride, Steamed Green Beans, and Local Sauteed Squash. Make sure you go check out the Pasta line!", "")
        pasta = Room(
            "the Pasta line today we are serving, Daily Pasta, Halal Chicken, Meatballs, Alfredo Sauce, and Marinara Sauce. Make sure you go check out the Vegan line!", "")
        vegan = Room(
            "the Vegan line today we are serving, Fried Rice, Coconut Curry Plant Based Meatballs, Agave Roasted Carrots, Fingerling Potatoes, Roasted Chickpeas, Rice noodles, and Vegetable Broth. Make sure you go check out the soup line!", "")
        soup = Room(
            "the Soup line today we are serving, Thai Curry Pork and Cowboy Chili. Go show Jack your meal! He always loves to see what people put together!", "")

        #add Map
        chaple.add_neighbor("west", quad)
        chaple.add_neighbor("northeast", clurg)
        chaple.add_neighbor("east", downtown)
        chaple.add_neighbor("southeast", behil)
        quad.add_neighbor("east", chaple)
        quad.add_neighbor("northwest", library)
        quad.add_neighbor("southwest", breslin)
        quad.add_neighbor("south", behil)
        library.add_neighbor("north", svfd)
        library.add_neighbor("south", breslin)
        library.add_neighbor("east", bishop)
        library.add_neighbor("southeast", quad)
        svfd.add_neighbor("southeast", clurg)
        svfd.add_neighbor("southwest", bishop)
        bishop.add_neighbor("northeast", svfd)
        bishop.add_neighbor("west", benny)
        bishop.add_neighbor("south", fowler)
        bishop.add_neighbor("southeast", breslin)
        bishop.add_neighbor("east", library)
        benny.add_neighbor("east", bishop)
        benny.add_neighbor("west", delt)
        benny.add_neighbor("south", snu)
        benny.add_neighbor("southeast", fowler)
        delt.add_neighbor("west", ka)
        delt.add_neighbor("east", benny)
        ka.add_neighbor("west", delt)
        snu.add_neighbor("north", benny)
        snu.add_neighbor("south", fowler)
        fowler.add_neighbor("north", benny)
        fowler.add_neighbor("east", alley)
        fowler.add_neighbor("northeast", bishop)
        fowler.add_neighbor("northwest", snu)
        fowler.add_neighbor("northeast", breslin)
        alley.add_neighbor("west", fowler)
        alley.add_neighbor("north", behil)
        alley.add_neighbor("northwest", breslin)
        alley.add_neighbor("northeast", downtown)
        alley.add_neighbor("east", cross)
        downtown.add_neighbor("west", chaple)
        downtown.add_neighbor("southwest", alley)
        downtown.add_neighbor("northwest", clurg)
        downtown.add_neighbor("south", cross)
        behil.add_neighbor("north", quad)
        behil.add_neighbor("south", alley)
        behil.add_neighbor("northwest", breslin)
        behil.add_neighbor("northeast", chaple)
        breslin.add_neighbor("north", library)
        breslin.add_neighbor("south", alley)
        breslin.add_neighbor("northeast", quad)
        breslin.add_neighbor("southeast", behil)
        breslin.add_neighbor("southwest", fowler)
        breslin.add_neighbor("northwest", bishop)
        clurg.add_neighbor("southwest", chaple)
        clurg.add_neighbor("northwest", svfd)
        clurg.add_neighbor("southeast", downtown)
        clurg.add_neighbor("homestyle", homestyle)
        homestyle.add_neighbor("pasta", pasta)
        pasta.add_neighbor("vegan", vegan)
        vegan.add_neighbor("soup", soup)
        soup.add_neighbor("northeast", chaple)
        soup.add_neighbor("northwest", svfd)
        soup.add_neighbor("southeast", downtown)

        #add NPCs
        chaple.npc.append(NPC("organist", "You’re finally awake. You’re in All Saints’ chapel at Sewanee: the University of the South! This Chapel sits near the center of campus, so it’s a good place to get your bearings. There are two exits out of here: McClurg to the Northeast and the Quad to the West; each place has a task for you to complete and you must complete all of the tasks.", 1))
        clurg.npc.append(NPC("jack", "Welcome to McClurg. This is Sewanee’s main dining hall. Campus is empty right now. Usually this place is packed. Since you’re here, I’ve got a challenge for you I’ll give you a meal to put together. You’ll need to find each station that has each part of the meal Find one item from Homestyle, Pasta, Salad, and Vegan. Bring all four back to me, finish the meal and your McClurg task is complete.", 0))
        soup.npc.append(NPC("jack", "Would you look at that! That’s quite the spread!! I love the variety from each line!", 1))
        quad.npc.extend([
            NPC("person", "Welcome to the Quad. People usually come out here to study, relax, or just take a break between classes. Your Quad task is simple. Slow down for a minute and solve the riddle of the day: What has many keys but can’t open a single lock?", 0,),
            NPC("painter", "Hey there, welcome to the Quad. I’ve been here for a few hours working on my painting of Breslin Tower. Have you explored inside yet? If not, go have a look. It's an interesting place. What dorm are you in? If you haven’t been to res-life go to bishops commons which is in the Northwest.",0 ,)])
        breslin.npc.append(NPC("bellman", "Welcome to Breslin Tower, trust me the stairs are not going to break. They may look like they are a thousand years old but they’ve been holding me up for the past 20 years. To get your achievement you have to ring the bell at 4:30pm. ", 0))
        bishop.npc.append(NPC("reslife", "Welcome to Sewanee! You are (player name) right? Ive got your room key and student id right here! you will be living in benidict hall, or as most students call it benny! its just west of here.", 0))

        #add book
        quad.book = Book("notebook", "Your Quad task is simple. Slow down for a minute and solve the riddle of the day: What has many keys but can’t open a single lock?", 0)

        #add bell
        breslin.bell = Bell("bell", 1)

        quad.treasure.extend([
            Treasure("diamond", "text here", 1),
            Treasure("coin", "Text here", 1),])
        bishop.treasure.append(Treasure("key", "", 0))

        self.current_room = chaple
        self.say("**** This is a beta version of our game. The whole map is avaliable to the player but only All Saints, The Quad, Mcclurg, bishop's common and Breslin have achievements in them. Enjoy!")
        self.play_sound("organ")
        self.say("You wake up gasping against the polished oak of a front pew, the crisp, mountain air tasting faintly of aged candle wax and old books. The silence of the chapel is absolute, broken only by the rhythmic sounds of the organ. As you sit up, your hand brushes against a paper name tag stuck to your jacket, revealing the name you had previously forgotten, _____.")
        self.say("")
        self.say("Try: look or talk organist")

        #add items
        chaple.treasure = Treasure("key", "a key to an organ here", 1)


    def say(self, message):
        self.messages.append(message)

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def announce_room(self):
        self.say(f"Welcome to {self.current_room.name}")
        room = self.current_room.name
        #if room != homestyle or room != pasta or room != vegan: I want these specific rooms to not announce their exits but cannot figure out how to.
        self.say(f"Exits: {self.current_room.list_exits()}")

    def look(self):
        self.say(f"{self.current_room.description}")

    def go(self, direction):
        destination = self.current_room.get_neighbor(direction)
        if destination is None:
            self.say("You can't go that way from here.")
            return
        self.current_room = destination
        self.play_sound("move")
        if self.current_room.enter_sound is not None:
            self.play_sound(self.current_room.enter_sound)
        self.announce_room()

    def talk(self, name):
        for npc in self.current_room.npc:
           if npc is not None and npc.name == name:
                self.say(f"{npc.speech}")
           if npc is not None and npc.name == name:
                self.score += npc.value
           if npc.value > 0:
                self.play_sound("pickup")
                self.say(f"Your score is now {self.score} out of 16.")
                npc.value = 0
           if self.score == 16:
                self.say("YOU WIN!")
                self.play_sound("win")
                self.game_over = True
           return self.current_room.npc == True
        else:
            self.say(f"There is no one with that name talk to here.")

    def take(self, name):
        for treasure in self.current_room.treasure:
            if treasure.name == name:
                self.current_room.treasure.remove(treasure)
                self.score += treasure.value
                self.play_sound("pickup")
                self.say(f"You take the {treasure.name}.")
                self.say(f"Your score is now {self.score} out of 16.")
                if self.score == 16:
                    self.say("YOU WIN!")
                    self.play_sound("win")
                    pygame.mixer.music.stop()
                    self.game_over = True
                return
        else:
            self.say(f"There is no {name} here.")

    def read(self, name):
        book = self.current_room.book
        if book is not None and book.name == name:
            self.say(f"{self.current_room.book.description}")
        else:
            self.say(f"I dont see that type of book here!")

    def ring(self, name):
       bell = self.current_room.bell
       if bell is not None and bell.name == name:
            self.say("You scramble up the spiral stairs, even though they are supposedly safe they still wiggle as you walk up them. You see skinnier ropes and then one bigger one that looks like it connects to a huge bell so you give it a good tug.")
            self.play_sound("bell")
            self.score += bell.value
            if self.current_room.bell.value > 0:
                self.play_sound("pickup")
                self.say(f"Your score is now {self.score} out of 16.")
                bell.value = 0
            if self.score == 16:
                self.say("YOU WIN!")
                self.play_sound("win")
                self.game_over = True
            return self.current_room.bell == True
       else:
            self.say(f"There is no one with that name talk to here.")

    def handle_command(self, line):
        self.say(f"> {line}")
        words = line.lower().split()

        if not words:
            return

        command = words[0]
        piano_value = 1
        if self.current_room.monster is not None and command not in ["attack", "look"]:
            self.say("You can't do that with unfriendlies about.")
            return

        if command == "look":
            self.look()
        elif command == "go" and len(words) > 1:
            self.go(words[1])
        elif command == "attack" and len(words) > 1:
            self.attack(words[1])
        elif command == "take" and len(words) > 1:
            self.take(words[1])
        elif command == "help":
            self.say("Commands: look, go DIRECTION, talk CHARACHER, read BOOK, ")
        elif command == "talk" and len(words) > 1:
            self.talk(words[1])
        elif command == "visit" and len(words) > 1:
            self.visit(words[1])
        elif command == "read" and len(words) > 1:
            self.read(words[1])
        elif command == "piano":
            piano = False
            if piano == False:
                self.say("Correct, great job!")
                self.score += piano_value
                piano == True
                self.play_sound("pickup")
                self.say(f"Your score is now {self.score} out of 16.")
            if self.score == 16:
                self.say("YOU WIN!")
                self.play_sound("win")
                self.game_over = True
        elif command == "1857":
            self.say("The doors creak open as you step foot inside the tower. You see an ornate spiral staircase that looks like it is going to break as soon as you put on foot on the first stair rung. The stairs look like they lead to a trapped door. You also see a bellman standing in the tower.")
        elif command == "ring" and len(words) > 1:
            self.ring(words[1])


        else:
            self.say("I don't understand that.")

def wrap_text(text, font, max_width):
    if not text:
        return [""]
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = word if not current else current + " " + word
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def draw_game(screen, font, small_font, game):
    screen.fill((88, 44, 131))
    screen.blit(font.render("Discovering The Domain", True, (235, 235, 240)), (30, 20))

    lines = []
    for message in game.messages:
        lines.extend(wrap_text(message, small_font, WIDTH - 60))
    lines = lines[-20:]

    y = 70
    for line in lines:
        screen.blit(small_font.render(line, True, (206, 184, 136)), (30, y))
        y += 23

    pygame.draw.line(screen, (100, 100, 110), (30, HEIGHT - 70), (WIDTH - 30, HEIGHT - 70), 2)
    screen.blit(small_font.render("> " + game.current_input, True, (255, 255, 255)), (30, HEIGHT - 50))

async def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Discovering the Domain")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 22)

    game = TextAdventure()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    if not game.game_over:
                        command = game.current_input.strip()
                        game.current_input = ""
                        game.handle_command(command)
                elif event.key == pygame.K_BACKSPACE:
                    game.current_input = game.current_input[:-1]
                elif event.unicode and event.unicode.isprintable():
                    game.current_input += event.unicode

        draw_game(screen, font, small_font, game)
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())