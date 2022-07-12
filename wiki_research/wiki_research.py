# Import the wikipedia library
import wikipedia as wiki
import re

print("Welcome to the Wikipedia research tool!")

user_input = input("Enter a topic: ")

results = wiki.search(user_input)

page_name = None
if len(results) > 1:
    while page_name is None:
        # Iterate through the results, print them with their index and then ask the user to select one
        for i, result in enumerate(results):
            print(i, result)
        user_input = int(input("Select a topic: "))
        # Check if the user input is valid
        if user_input >= 0 and user_input < len(results):
            page_name = results[user_input]
        else:
            print("\nInvalid input\n")
elif len(results) == 1:
    page_name = results[0]
else:
    print("No results found")
    exit()


# Get a page from Wikipedia
# If auto_suggest is True, it does not always return the correct page
result = wiki.page(title=page_name, auto_suggest=False)
# This fixes any sentences that have a period at the end.Immediately after the period, there should be a space.As demonstrated here.
summary_fixed = re.sub(r'(\w\.)([a-zA-Z])', r'\1 \2', result.summary)
summary_fixed = re.sub(r' \(\)', '', summary_fixed)
print(result.title)
print(summary_fixed)
print(result.references)

# Save the page to a file
with open("wiki_research/output.txt", "w") as f:
    f.write(result.title + "\n")
    f.write(summary_fixed)