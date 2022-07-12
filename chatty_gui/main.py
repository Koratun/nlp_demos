
# import the chatterbot package
# This is the chatbot engine we will use
from chatterbot import ChatBot

# Give our chatbot a name
chatbot = ChatBot("HAL 9000")

# Packages used to Train your chatbot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Add a new personality about Mars here
# Just using a python list
# Format should be question from the user and the response from chatbot
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

# Set the trainers we want train
personality_space_trainer=ListTrainer(chatbot)
star_wars_trainer = ListTrainer(chatbot)
# trainer = ChatterBotCorpusTrainer(chatbot)

# Now here we actually train our chatbot on the corpus
# This is what gives our chatbot its personality 
# Train the personality you want to override should come first

# Standard personality chatterbot comes with
# trainer.train('chatterbot.corpus.english')
personality_space_trainer.train(personality_space)
star_wars_trainer.train(star_wars)

''' ******************* GUI Below Engine Above **************** '''
# Import for the GUI 
from chatbot_gui import ChatbotGUI


def startup(chat: ChatbotGUI):
    chat.send_ai_message("Hello! I am Space Kid! I love space! Ask me anything!")


# create the chatbot app
"""
    Options
    - title: App window title.
    - gif_path: File Path to the ChatBot gif.
    - show_timestamps: If the chat has time-stamps.
    - default_voice_options: The voice options provided to the text-to-speech engine by default if not specified
                             when calling the send_ai_message() function.
"""
app = ChatbotGUI(
    title="Cape Canaveral",
    gif_path="chatty_gui/Space Kid.gif",
    show_timestamps=True,
    default_voice_options={
        "rate": 200,
        "volume": 1.0,
        "voice": "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
    },
    startup_callback=startup
)


# define the function that handles incoming user messages
@app.event
def on_message(chat: ChatbotGUI, text: str):
    """
    This is where you can add chat bot functionality!

    You can use chat.send_ai_message(text, callback, voice_options) to send a message as the AI.
        params:
            - text: the text you want the bot to say
            - callback: a function which will be executed when the AI is done talking
            - voice_options: a dictionary where you can provide options for the AI's speaking voice
                default: {
                   "rate": 100,
                   "volume": 0.8,
                   "voice": "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
                }

    You can use chat.start_gif() and chat.stop_gif() to start and stop the gif.
    You can use chat.clear() to clear the user and AI chat boxes.

    You can use chat.process_and_send_ai_message to offload chatbot processing to a thread to prevent the GUI from
    freezing up.
        params:
            - ai_response_generator: A function which takes a string as it's input (user message) and responds with
                                     a string (AI's response).
            - text: The text that the ai is responding to.
            - callback: a function which will be executed when the AI is done talking
            - voice_options: a dictionary where you can provide options for the AI's speaking voice
                default: {
                   "rate": 100,
                   "volume": 0.8,
                   "voice": "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
                }

    :param chat: The chat box object.
    :param text: Text the user has entered.
    :return:
    """
    # this is where you can add chat bot functionality!
    # text is the text the user has entered into the chat
    # you can use chat.send_ai_message("some text") to send a message as the AI, this will do background
    # you can use chat.start_gif() and chat.stop_gif() to start and stop the gif
    # you can use chat.clear() to clear the user and AI chat boxes

    # print the text the user entered to console
    print("User Entered Message: " + text)             
    
    ''' Here you can intercept the user input and override the bot
    output with your own responses and commands.'''
    # if the user send the "clear" message clear the chats
    if text.lower().find("erase chat") != -1:
        chat.clear()
    # user can say any form of bye to close the chat.
    elif text.lower() in ["exit", "quit", "bye", "goodbye"]:
        # define a callback which will close the application
        def close():
            chat.exit()

        # send the goodbye message and provide the close function as a callback
        chat.process_and_send_ai_message(chatbot.get_response, text, callback=close)
    else:
        # offload chat bot processing to a worker thread and also send the result as an ai message
        chat.process_and_send_ai_message(chatbot.get_response, text)


# run the chat bot application
app.run()
