# from handler import fetch_articles
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import contractions

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

test_string = """Nvidia (NVDA) stock slipped into correction territory Monday, but analysts are still bullish on the chipmaking giant.

Nvidia shares fell 2% intraday Monday to $131.48 and are down about 12% since their record closing high of $148.88 on Nov. 7. A technical correction is considered to have occurred when shares dropped 10% from their peak.

Despite the recent slump, investors don't seem to be worried in the long term. Analysts at Bank of America and Bernstein each called Nvidia a "top pick" Monday, posting price targets of $190 and $175, respectively. The consensus price target among 20 brokers covering Nvidia tracked by Visible Alpha is about $176."""

financial_terms = {
    "eps": "earnings per share",
    "roi": "return on investment",
    "ipo": "initial public offering"
}

# accepts data as a string "text", returns cleaned data
# designed to take full articles to individual phrases
def clean_unstructured_data(text: str):
    # text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.lower()
    text = text.encode('utf-8', 'ignore').decode('utf-8')
    text = contractions.fix(text)

    text = word_tokenize(text)

    filtered_words = [w for w in text if not w in stop_words]
    lemmatized_words = [lemmatizer.lemmatize(w) for w in filtered_words]
    
    processed_sentence_tokens = lemmatized_words
    
    return processed_sentence_tokens

# print(clean_unstructured_data(test_string))
