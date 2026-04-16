import os

f = 'thesode.html'
try:
    with open(f, 'r', encoding='utf-8') as file:
        text = file.read()
except UnicodeDecodeError:
    with open(f, 'r', encoding='latin-1') as file:
        text = file.read()

# Fix the corrupt arrow
text = text.replace('â†’', '→')

# Ensure it writes proper UTF-8
with open(f, 'w', encoding='utf-8') as file:
    file.write(text)

print("Arrow repair completed.")
