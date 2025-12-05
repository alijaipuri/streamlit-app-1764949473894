import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import time

st.set_page_config(page_title='Text Analyzer', page_icon='📊')

st.title('📊 Text Analyzer')
st.markdown('Welcome! This app analyzes text and provides insights into word count, character count, sentence count, reading time, and most common words with a word cloud.')

# Sidebar inputs
with st.sidebar:
    st.header('Settings')
    text_input = st.text_area('Enter or paste your text here')

# Main content
if st.button('Analyze', type='primary'):
    if text_input:
        # Preprocessing
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text_input.lower())
        words = [lemmatizer.lemmatize(word) for word in words if word.isalpha() and word not in stop_words]

        # Word count
        word_count = len(words)
        st.metric('Word Count', word_count)

        # Character count
        char_count = len(text_input)
        st.metric('Character Count', char_count)

        # Sentence count
        sentences = sent_tokenize(text_input)
        sentence_count = len(sentences)
        st.metric('Sentence Count', sentence_count)

        # Reading time
        reading_time = word_count / 200  # assuming 200 words per minute
        st.metric('Reading Time (minutes)', reading_time)

        # Most common words
        common_words = Counter(words).most_common(10)
        st.header('Most Common Words')
        st.write(pd.DataFrame(common_words, columns=['Word', 'Frequency']))

        # Word cloud
        wordcloud = WordCloud(width=800, height=400, max_words=100).generate(' '.join(words))
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.header('Word Cloud')
        st.pyplot(fig)

    else:
        st.error('Please enter or paste some text')

# Show example
with st.expander('See example'):
    example_text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
    st.write(example_text) 

# Download nltk data if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')