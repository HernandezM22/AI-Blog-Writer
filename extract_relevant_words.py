import pandas as pd
import langdetect as lg
import matplotlib.pyplot as plt
import seaborn as sns
import emoji
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np

def load_tweets_data(
        path: str
) -> pd.DataFrame:

    df = pd.read_csv(path)
    df = df[["user/id, full_text"]].dropna()
    return df


def detect_language(
        data: pd.DataFrame,
) -> pd.DataFrame:
    
    langs = []
    for item in data["full_text"]:
        try:
            lang = lg.detect(item)
            langs.append(lang)
        except:
            lang = "unknown"
            langs.append(lang)
    
    data["language"] = langs
    return data


def split_spanish_english(
        data: pd.DataFrame
) -> pd.DataFrame:
    
    eng = data[data["language"]=="en"]
    es = data[data["language"]=="es"]
    remaining = data[(data["language"]!="en") & (data["language"])!="es"]

    return eng, es, remaining


def clean_text(
        data: pd.DataFrame,
        language: str
) -> pd.DataFrame:

    stop_words = set(stopwords.words(language))

    def check_if_not_stopwords(text, stop_words):
        filtered_sentence = [w for w in text if not w.lower() in stop_words]
        return filtered_sentence

    def remove_emojis(text):
        no_emojis = [emoji.replace_emoji(w, '') for w in text]
        return no_emojis

    def remove_special_characters(text):
        no_special = [w for w in text if w.isalnum()]
        return no_special
    
    word_tokens = [word_tokenize(sentence) for sentence in data["full_text"]]
    filtered_sentences = [check_if_not_stopwords(i, stop_words) for i in word_tokens]
    filtered_sentences = [remove_emojis(i) for i in filtered_sentences]
    filtered_sentences = [remove_special_characters(i) for i in filtered_sentences]

    data["filtered_text"] = [" ".join(i) for i in filtered_sentences]

    return data


def convert_column_to_raw_text(
        data: pd.DataFrame
) -> str:

    return " ".join(data["filtered_text"])


def visualize_word_frequencies(
        text: str
) -> pd.DataFrame:

    def get_df(input_text):
        list_words = input_text.split(' ')
        set_words_full = list(set(list_words))
    
        count_words = [list_words.count(i) for i in set_words_full]
    
        df = pd.DataFrame(zip(set_words_full, count_words), columns=['words','count'])
        df.sort_values('count', ascending=False, inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def get_colordict(palette,number,start):
        pal = list(sns.color_palette(palette=palette, n_colors=number).as_hex())
        color_d = dict(enumerate(pal, start=start))
        return color_d

    df_words = get_df(text)
    df_words = df_words[df_words["words"]!="https"]

    index_list = [[i[0],i[-1]+1] for i in np.array_split(range(100), 5)]

    n = df_words['count'].max()
    color_dict = get_colordict('viridis', n, 1)

    fig, axs = plt.subplots(1, 5, figsize=(16,8), facecolor='white', squeeze=False)
    for col, idx in zip(range(0,5), index_list):
        df = df_words[idx[0]:idx[-1]]
        label = [w + ': ' + str(n) for w,n in zip(df['words'],df['count'])]
        color_l = [color_dict.get(i) for i in df['count']]
        x = list(df['count'])
        y = list(range(0,20))
    
        sns.barplot(x = x, y = y, data=df, alpha=0.9, orient = 'h',
                ax = axs[0][col], palette = color_l)
        axs[0][col].set_xlim(0,n+1)                     #set X axis range max
        axs[0][col].set_yticklabels(label, fontsize=12)
        axs[0][col].spines['bottom'].set_color('white')
        axs[0][col].spines['right'].set_color('white')
        axs[0][col].spines['top'].set_color('white')
        axs[0][col].spines['left'].set_color('white')
            
    plt.tight_layout()    
    plt.show()

    return df_words