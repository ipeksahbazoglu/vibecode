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
    if flesch_score >= 70:
        readability_score = 10
    elif flesch_score >= 50:
        readability_score = 7
    elif flesch_score >= 30:
        readability_score = 4
    else:
        readability_score = 1

    # 2. Sentence length
    avg_sentence_length = textstat.avg_sentence_length(text)
    if avg_sentence_length <= 12:
        sentence_score = 10
    elif avg_sentence_length <= 17:
        sentence_score = 7
    elif avg_sentence_length <= 25:
        sentence_score = 4
    else:
        sentence_score = 1

    # 3. Jargon detection
    words_in_text = [word.strip(string.punctuation).lower() for word in text.split()]
    uncommon_words = [word for word in words_in_text if word and word not in common_words]
    jargon_ratio = len(uncommon_words) / max(len(words_in_text), 1)
    if jargon_ratio < 0.05:
        jargon_score = 5
    elif jargon_ratio < 0.10:
        jargon_score = 3
    else:
        jargon_score = 1

    # Total score out of 25
    total_score = readability_score + sentence_score + jargon_score
    return total_score

# Example usage
if __name__ == "__main__":
    input_text = input("Enter the text to analyze:\n")
    score = calculate_inclusivity_score(input_text)
    print(f"\nInclusivity Score (out of 25): {score}")
