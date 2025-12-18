# Dictionary to expand contractions in text to their full forms
contraction_mapping2 = {"ain’t": "is not", "aren’t": "are not", "can’t": "cannot", "‘cause": "because",
                        "could’ve": "could have", "couldn’t": "could not",
                        # ... (many more contractions)
                        "you’ve": "you have"}

# Another version of contraction mapping with lowercase and apostrophes normalized
contraction_mapping = {
    "ain't": "is not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    # ... (many more contractions)
    "you're": "you are",
    "you've": "you have"
}

import re
import nltk
from nltk.corpus import stopwords


# Set of English stopwords to remove from text

try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))



# -----------------------------
# Function: text_cleaner_heavy
# -----------------------------
# Performs aggressive text cleaning:
#   - Lowercases text
#   - Removes quotes, parentheses, and punctuation
#   - Expands contractions
#   - Removes stopwords
#   - Removes short or repeated words
def text_cleaner_heavy(text):
    newString = text.lower()  # lowercase
    newString = re.sub('"', '', newString)  # remove double quotes
    newString = re.sub(r'\([^)]*\)', '', newString)  # remove text inside parentheses

    # Expand contractions using mapping
    newString = ' '.join([contraction_mapping[t] if t in contraction_mapping else t for t in newString.split(' ')])

    newString = re.sub(r"’s\b", "", newString)  # remove possessive 's
    newString = re.sub('[^a-zA-Z\s\-]', '', newString)  # keep letters, spaces, hyphens
    newString = re.sub('[^a-zA-Z\s]', ' ', newString)  # remove any leftover non-letter characters

    # Tokenize and remove stopwords
    tokens = [word for word in newString.split() if word not in stop_words]

    # Keep only unique words with length >= 3
    long_words = []
    prev_word = []
    for i in tokens:
        if i not in prev_word and len(i) >= 3:
            long_words.append(i)
            prev_word = [i]

    return (" ".join(long_words)).strip()


# -----------------------------
# Function: text_cleaner
# -----------------------------
# Medium cleaning function:
#   - Lowercases text
#   - Removes quotes, parentheses
#   - Expands contractions
#   - Removes URLs, mentions, and non-letter characters
def text_cleaner(text):
    newString = text.lower()
    newString = re.sub('"', '', newString)
    newString = re.sub(r'\([^)]*\)', '', newString)

    # Expand contractions
    newString = ' '.join([contraction_mapping[t] if t in contraction_mapping else t for t in newString.split(' ')])

    # Remove URLs
    newString = re.sub(r"(?i)http(s):\/\/[a-z0-9.~_\-\/]+", '', newString)
    # Remove Twitter/Instagram mentions
    newString = re.sub(r"(?i)@[a-z0-9_]+", '', newString)
    # Remove punctuation
    newString = re.sub('[^a-zA-Z\s]', ' ', newString)

    return newString


# -----------------------------
# Function: text_cleaner_light
# -----------------------------
# Light cleaning function:
#   - Lowercases text
#   - Removes quotes, parentheses
#   - Expands contractions
#   - Keeps most of the original text intact
def text_cleaner_light(text):
    newString = text.lower()
    newString = re.sub('"', '', newString)
    newString = re.sub(r'\([^)]*\)', '', newString)

    # Expand contractions
    newString = ' '.join([contraction_mapping[t] if t in contraction_mapping else t for t in newString.split(' ')])

    newString = re.sub(r"’s\b", "", newString)  # remove possessive 's

    return newString
