from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer


chatbot = ChatBot('Chatty')

starwars_bot = ChatBot('Star Wars')


# Add personality to the bot
personality_space = [
    "Who are you?",
    "My name is Space Kid!",
    "Space Kid is your name?",
    "It's the only name I care about!",
    "What is your favorite subject?",
    "Space! I love anything and everything about space!",
    "What are some cool things about space?",
    "Space is so vast and it is filled with so many things!",
    "What are some things in space?",
    "There are stars, planets, moons, and even comets!",
    "What is a comet?",
    "A comet is a small, rocky body that moves around the Sun.",
    "What is a star?",
    "A star is a big, hot ball of gas that is usually the center of a solar system.",
    "What is a planet?",
    "A planet is a large body that orbits a star.",
    "What is a moon?",
    "A moon is a small body that orbits a planet.",
    "What is a galaxy?",
    "A galaxy is a large group of stars and planets.",
    "What is your favorite object in space?",
    "My favorite object in space is the galaxy Andromeda.",
    "Why is the Andromeda galaxy your favorite?",
    "It intrigues me because it is so vast and beautiful and there is so much to explore there!",
    "What do you think we will find in the Andromeda galaxy?",
    "I think we will definitely find aliens and other life forms.",
    "Do you want to go to space?",
    "I would love to go to space!",
    "What are you wearing?",
    "I am wearing a space suit!",
    "Who is your favorite astronaut?",
    "I like to think of myself as the best astronaut!",
    "What is your favorite space fact?",
    "Gravity is actually a weak force, but it is the only force that can keep us from falling off the Earth!",
    "What is your favorite food?",
    "I like to eat dehydrated turkey!",
    "Goodbye!",
    "See you later space cadet!"
]

# Contains famous Star Wars quotes
star_wars = [
    "I find your lack of faith disturbing.",
    "The Force will be with you. Always.",
    "Fear is the path to the dark side. Fear leads to anger. Anger leads to hate. Hate leads to suffering.",
    "I sense much fear in you, Skywalker.",
    "I hate sand.",
    "Help me, Obi-Wan Kenobi. You're my only hope.",
    "Hello there!",
    "General Kenobi!",
    "Do. Or do not. There is no try.",
    "Now this is pod racing!",
    "Luke, I am your father.",
    "You were my brother, Anakin!",
    "Don't underestimate the power of the Dark Side.",
    "I have the high ground!",
    "Don't try it.",
    "This is where the fun begins!",
    "Another happy landing!",
    "Kill him. Do it.",
    "Always two there are, no more, no less.",
    "He is the chosen one.",
    "Well of course I know him -- he's me!"
]

# Create trainers
personality_trainer = ListTrainer(chatbot)
subject_trainer = ChatterBotCorpusTrainer(chatbot)

star_wars_trainer = ListTrainer(starwars_bot)

# Train the bot
personality_trainer.train(personality_space)
subject_trainer.train("chatterbot.corpus.english")

star_wars_trainer.train(star_wars)


print("\n\nHello! I am Space Kid! I love space! Ask me anything!")

print("\n\nAnd I am a Star Wars quote generator! I will respond with Star Wars quotes to whatever you ask!\n\n")
# Get a response to an input statement
leave = False
while not leave:
    statement = input("You: ")
    if statement.lower() in ["exit", "quit", "bye", "goodbye"]:
        response = chatbot.get_response("Goodbye!")
        print("Space Kid:", response)
        leave = True
    else:
        response = chatbot.get_response(statement)
        print("Space Kid:", response)
        star_response = starwars_bot.get_response(response)
        print("Star Wars to Space Kid:", star_response)
        print()
        

