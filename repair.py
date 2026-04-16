import os

f = 'thesode.html'
try:
    with open(f, 'r', encoding='utf-8') as file:
        text = file.read()
except UnicodeDecodeError:
    with open(f, 'r', encoding='latin-1') as file:
        text = file.read()

# Fix image extensions
text = text.replace('sode_office.png', 'sode_office.jpg')

# Fix corrupted characters (Windows-1252/Latin-1 double encoded as UTF-8)
corrections = {
    'Ã¢â‚¬â€': '—',
    'Ã¢â‚¬â€': '—',
    'â€”': '—',
    'Â·': '·',
    'â€¦': '…',
    'â€™': "'",
    'â€˜': "'",
    'â€œ': '"',
    'â€': '"',
    'â€?': '"'
}

for bad, good in corrections.items():
    text = text.replace(bad, good)

# Ensure it writes proper UTF-8 with BOM
with open(f, 'w', encoding='utf-8') as file:
    file.write(text)

print("Repair completed.")
