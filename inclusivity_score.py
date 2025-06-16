import textstat
import nltk
from nltk.corpus import words
import string

# Download word list if not already present
nltk.download('words')
common_words = set(words.words())

def calculate_inclusivity_score(text):
    # 1. Readability using Flesch Reading Ease
    flesch_score = textstat.flesch_reading_ease(text)
    if flesch_score >= 50:
        readability_score = 10
    elif flesch_score >= 20:
        readability_score = 7
    elif flesch_score >= 10:
        readability_score = 5
    else:
        readability_score = 1

    # 2. Sentence length
    avg_sentence_length = textstat.avg_sentence_length(text)

    if avg_sentence_length <= 17:
        sentence_score = 10
    elif avg_sentence_length <= 25:
        sentence_score = 7
    else:
        sentence_score = 4

    # 3. Jargon detection
    words_in_text = [word.strip(string.punctuation).lower() for word in text.split()]
    uncommon_words = [word for word in words_in_text if word and word not in common_words]
    jargon_ratio = len(uncommon_words) / max(len(words_in_text), 1)
    if jargon_ratio < 0.50:
        jargon_score = 5
    elif jargon_ratio < 0.20:
        jargon_score = 3
    else:
        jargon_score = 1

    # Total score out of 25
    total_score = readability_score + sentence_score + jargon_score
    return total_score
