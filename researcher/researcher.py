from bs4 import BeautifulSoup
from bs4.element import Comment
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from summa.summarizer import summarize, get_graph, _clean_text_by_sentences as tokenize_sentences
import pyttsx3 as tts
from sumy.parsers.plaintext import PlaintextParser
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import re
import time
import multiprocessing as mp


def speak(my_lines: list):
    speech = tts.init()
    speech.setProperty("rate", 175)
    speech.setProperty("volume", 1.0)
    speech.setProperty("voice", "en-us")
    for line in my_lines:
        speech.say(line)
    speech.runAndWait()


def main():
    # Construct Speech engine
    speech = tts.init()

    speech.setProperty("rate", 175)
    speech.setProperty("volume", 1.0)
    speech.setProperty("voice", "en-us")

    sumos_lines = []

    print("\n\nGreetings! I am Sumo, the Summarizer. I can summarize your research for you!")
    sumos_lines.append("Greetings! I am Sumo, the Summarizer. I can summarize your research for you!")

    print("Sumo does take longer to process very long websites. Give Sumo one minute to process a website's text.\n")
    sumos_lines.append(
        "I do take longer to process very long websites. Give me one minute to process a website's text."
    )

    sumos_lines.append("Please use ONE sentence to describe what you want to know, and be as specific as possible.")

    # Spawn a new process which will speak the lines concurrently with the main process
    process1 = mp.Process(target=speak, args=(sumos_lines,))
    process1.start()

    sumos_lines.clear()

    # Ask the user what their question is
    question = input("Please use ONE sentence to describe what you want to know, and be as specific as possible.\n")

    # Tell Chrome to ignore the certificate errors
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-site-isolation-trials")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    # suppress the output of the webdriver
    options.add_argument("--headless")

    # Start up a new Chrome session
    driver = webdriver.Chrome("./chromedriver")
    driver.get("https://www.google.com/")

    # Use the driver to select the input with the autocomplete="off" attribute
    search_box = driver.find_element(By.XPATH, "//input[@autocomplete='off']")

    # just a bit of fun
    search_box.send_keys("SUMO!!")
    time.sleep(1.5)

    search_box.clear()

    search_box.send_keys("If Sumo gets stuck, reword your query and try again.")
    time.sleep(3)

    mp.Process(target=speak, args=(["Alright, let's see what the Internet has to say about your query!"],)).start()

    search_box.clear()

    # Search!
    search_box.send_keys(question, Keys.ENTER)

    # Create a BeautifulSoup object
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Get the page link by accessing the h3 tag
    def get_page_link(h3):
        # Check that the parent is an 'a' tag
        if h3.parent.name == "a":
            a = h3.parent
        else:
            return None

        # Check if this tag contains a 'data-ved' attribute and does NOT contain a 'data-hveid' attribute
        if a.has_attr("data-ved") and not a.has_attr("data-hveid"):
            # No attribute in the 'a' tag can contain "googleadservices"
            if "googleadservices" not in a["href"]:
                # return the link
                return a["href"]

    # Return the first three main hyperlinks
    links = []
    while len(links) < 3:
        # Find the first h3 tag
        h3 = soup.find("h3")
        # Check if the h3 tag is not None
        if h3:
            # Get the page link
            link = get_page_link(h3)
            # Check if the link is not None
            if link:
                # Add the link to the list
                links.append(link)
                # Remove the h3 tag
            h3.extract()

    def tag_visible(element):
        if element.name in ["style", "script", "head", "title", "meta", "[document]", "cite"]:
            return False
        if element.parent.name in ["style", "script", "head", "title", "meta", "[document]", "cite"]:
            return False
        if isinstance(element, Comment):
            return False

        def contains(original, items: list) -> bool:
            for item in items:
                if item in original:
                    return True
            return False

        while element.parent.name != "html":
            if element.parent.get("class"):
                if contains(element.parent.get("class"), ["reference", "refbegin", "footer"]):
                    return False
            element = element.parent
        return True

    # Use the summa library to get the summary of the web page passed in
    def get_page_summary(page_soup, question, raw: bool = False):
        text = ""
        if not raw:
            # Dump all the text from the page into a string
            text = page_soup.findAll(text=True)

            # Filter out all the unhelpful text
            text: list[str] = filter(tag_visible, text)

            # Join the text
            text: str = "\n".join(t.strip() for t in text)

            # Prepend the question to the text
            text = question + "\n" + text
        else:
            text = question + "\n" + page_soup

        # Get the summary of the text
        summary: list[str] = summarize(text, words=300, split=True)

        # tokenize the sentences
        sentences = tokenize_sentences(text)

        def get_sentence_index(tokenized_sentence) -> list:
            for s in sentences:
                if s.token == tokenized_sentence:
                    return [s.text, s.index]

        # Get a graph containing how similar each sentence is to every other sentence in the text
        graph = get_graph(text)
        # Get the node containing the question the user gave
        question_node = graph.nodes()[0]

        def get_question_edges(edge):
            if question_node in edge:
                if edge[1] is question_node:
                    temp = get_sentence_index(edge[0])
                    return [temp[0], temp[1], graph.edge_weight(edge)]
                else:
                    temp = get_sentence_index(edge[1])
                    return [temp[0], temp[1], graph.edge_weight(edge)]

        # Get a list of all edges to the question node and their weights
        question_edges = [item for item in map(get_question_edges, graph.edges()) if item][::2]

        minmax = {"min": min(question_edges, key=lambda x: x[2])[2], "max": max(question_edges, key=lambda x: x[2])[2]}

        return summary, question_edges, minmax, {sentence.text: sentence.index for sentence in sentences}

    def get_terminal_color_code(code: int):
        return f"\033[38;5;{code}m" if code != -1 else "\u001b[0m"

    def get_color_for_sentence(weight: float, minmax: dict):
        min_color_code = 87
        max_color_code = 82

        # Map the given weight to a color code given the min and max weights
        color_code = round(
            ((weight - minmax["min"]) / (minmax["max"] - minmax["min"])) * (max_color_code - min_color_code)
            + min_color_code
        )
        return get_terminal_color_code(color_code)

    # Holds all sentences that will be valued important by the summarizer
    cream_of_the_crop = []

    # Construct sumy summarizer
    LANG = "english"

    summarizer = LsaSummarizer(stemmer=Stemmer(LANG))
    summarizer.stop_words = get_stop_words(LANG)

    SENTENCE_COUNT = 30

    # Use the driver to visit all the links and get the page summaries
    for i, link in enumerate(links):
        # Visit the link
        driver.get(link)
        # Let it breath for a few seconds
        time.sleep(2)

        parser = HtmlParser.from_string(driver.page_source, link, Tokenizer(LANG))
        summary = summarizer(parser.document, SENTENCE_COUNT)

        # for s in summary:
        #     cream_of_the_crop.append((str(s), i))

        # Create a BeautifulSoup object
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # Get the page summary
        summary, question_rank, minmax, sentence_indexes = get_page_summary(soup, question)
        qr_index = 0
        # Print the summary coloring the sentences that are similar to the question
        for sentence in summary:
            # See if this sentence's index is at or past the index of the currently selected sentence that is similar to the question
            if qr_index < len(question_rank) and sentence_indexes[sentence] >= question_rank[qr_index][1]:
                while sentence_indexes[sentence] >= question_rank[qr_index][1]:
                    # The closer to green the color is, the more similar the sentence is to the question
                    print(
                        get_color_for_sentence(question_rank[qr_index][2], minmax)
                        + question_rank[qr_index][0]
                        + get_terminal_color_code(-1)
                    )
                    cream_of_the_crop.append((question_rank[qr_index][0], i, question_rank[qr_index][2]))
                    qr_index += 1
                    if qr_index >= len(question_rank):
                        break
            # else:
            #     print(sentence)
            #     cream_of_the_crop.append((sentence, i, 0))

        # # Print the link and newline
        # print(link+'\n')

    driver.close()

    print("\nSummarizing...\n\n")

    # Summarize the cream of the crop
    parser = PlaintextParser.from_string("\n".join(s[0] for s in cream_of_the_crop), Tokenizer(LANG))
    summary = summarizer(parser.document, 5)

    # Create a summary without duplicates
    final_summary = []
    [final_summary.append(s) for s in summary if s not in final_summary]

    # grandminmax = {"min": min(s[2] for s in cream_of_the_crop if s[2] > 0), "max": max(s[2] for s in cream_of_the_crop)}

    # Strip the main website out of the links using regex
    sources = [re.sub(r"^\w+:\/\/([\w\.-]+).+", r"\1", link) for link in links]

    def get_source_id(sentence):
        for s in cream_of_the_crop:
            if s[0] == str(sentence):
                return s[1]

    # Print and say one sentence at a time
    for sentence in summary:
        id = get_source_id(sentence)
        if id is None:
            print(sentence)
        else:
            print(str(sentence) + " - " + sources[id])
        speech.say(sentence)
        speech.runAndWait()

    print()
    # Print the links
    for link in links:
        print(link)

    print("\nIf you would like to read the full article, visit the links above.")
    print("I have gone through the links above and displayed the sentences most similar to your query above.")
    print(
        get_terminal_color_code(82)
        + "Green is more similar to your query, "
        + get_terminal_color_code(87)
        + "while blue is less similar.\n"
        + get_terminal_color_code(-1)
    )
    speech.say("If you would like to read the full articles, visit the links above.")
    speech.say("I have gone through the links above and displayed the sentences most similar to your query above.")
    speech.say("Green is more similar to your query, while blue is less similar.")
    speech.say("Thank you for using my program, come back whenever you need to do more research!")
    speech.runAndWait()


if __name__ == "__main__":
    main()
