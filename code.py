import tkinter as tk
import nltk
from textblob import TextBlob
from newspaper import Article

nltk.download('punkt')


def summarize():
    # For url, I have to specify a start and end point.

    url = utext.get('1.0', 'end').strip()

    article = Article(url)

    article.download()

    article.parse()

    article.nlp()

    # config is required for the user to not be able to make changes
    # and we have to apply this process separately to get rid of each column expressed with the print below.
    title.config(state='normal')
    author.config(state='normal')
    publication.config(state='normal')
    summary.config(state='normal')
    sentiment.config(state='normal')

    # In case of changing the content, we will want to delete everything there first.
    # this way sensitivity is made available for analysis
    title.delete('1.0', "END")
    title.insert('1.0', article.title)

    author.delete('1.0', "END")
    author.insert('1.0', article.authors)

    publication.delete('1.0', "END")
    publication.insert('1.0', article.publish_date)

    summary.delete('1.0', "END")
    summary.insert('1.0', article.summary)

    analysis = TextBlob(article.text)
    sentiment.delete('1.0', "END")
    sentiment.insert('1.0',
                     f'Polarity: {analysis.polarity}, Sentiment: {"positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"}')

    # For "disabled" on content change
    title.config(state='disabled')
    author.config(state='disabled')
    publication.config(state='disabled')
    summary.config(state='disabled')
    sentiment.config(state='disabled')


# tkinter
root = tk.Tk()
root.title('News Summerizer')
root.geometry('1200x600')

# We will define the properties of the headers that we will tag between root.mainloop () and root.
tlabel = tk.Label(root, text="Title")
tlabel.pack()
title = tk.Text(root, height=1, width=140)

# We're going to do a configuration here. "Disable" for the user not to put anything other than the url in the box and "bg" for the background color.
title.config(state='disabled', bg='#dddddd')

# We pack it with pack() and complete it.
title.pack()

# Same procedures for authors tab
alabel = tk.Label(root, text="Author")
alabel.pack()

author = tk.Text(root, height=1, width=140)
author.config(state='disabled', bg='#dddddd')
author.pack()

# Same procedures for publication date tab
plabel = tk.Label(root, text="Publishing Date")
plabel.pack()

publication = tk.Text(root, height=1, width=140)
publication.config(state='disabled', bg='#dddddd')
publication.pack()

# Same procedures for summary tab
slabel = tk.Label(root, text="Summary")
slabel.pack()

summary = tk.Text(root, height=20, width=140)
summary.config(state='disabled', bg='#dddddd')
summary.pack()

# Same procedures for sentiment analysis
selabel = tk.Label(root, text="Sentiment Analysis")
selabel.pack()

sentiment = tk.Text(root, height=1, width=140)
sentiment.config(state='disabled', bg='#dddddd')
sentiment.pack()

# for the url to be entered by the user
ulabel = tk.Label(root, text="Enter URL")
ulabel.pack()
# In order not to write a url for the 2nd time, we named it differently 'utext' as it should not interfere with the other variable.
utext = tk.Text(root, height=1, width=140)
utext.pack()

# Now let's add a button for the summary
# We will connect command with def.
bt = tk.Button(root, text='Summarize', command=summarize)
bt.pack()

root.mainloop()


###NEWS SUMMARRY CODE
from newspaper import Article
from googletrans import Translator
import tkinter as tk
from tkinter import *
from textblob import TextBlob

import nltk
nltk.download('punkt')

# GUI Window
top = tk.Tk()
top.update()
top.geometry('680x500')
top.title('News Article Summary')

#Label for top
label = Label(top, background='#CDCDCD', font=('calibri', 20, 'bold'))
art_label = ('arial', 16, 'bold')
art_cont = ('verdana', 12)

#Variable used for both the function
article = ''
art_title = ''
article_sum = ''
art_content= ''

#Canvas and frame
my_canvas = Canvas(top, borderwidth=0, background='#ffffff')
frame = Frame(my_canvas, background='#ffffff')
frame.pack(fill=BOTH, expand=TRUE)
vsb = Scrollbar(top, orient='vertical', command=my_canvas.yview)
my_canvas.configure(yscrollcommand=vsb.set)
vsb.pack(side='right', fill='y')
my_canvas.pack(side='right', fill='both', expand=True)
my_canvas.create_window((0, 0), window=frame, anchor='nw')
my_canvas.pack(fill='both', expand=True)

#Scrollbar
def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox('all'))
frame.bind("<Configure>", lambda event, canvas=my_canvas: onFrameConfigure(my_canvas))

#Translating and Summary Function
def translate_news():
    global article
    global art_title
    global article_sum
    global art_content

    # Article
    article = Article(news_url.get())
    article.download()
    article.parse()
    article.nlp()

    # Sentiment analysis
    texts = article.title + article.summary + article.text
    summary_sentiment = TextBlob(texts)
    sentiment_polarity = summary_sentiment.sentiment.polarity
    sentiment_subjectivity = summary_sentiment.sentiment.subjectivity
    print(sentiment_polarity,sentiment_subjectivity)

    #Translating Article
    translator = Translator()
    art_title = translator.translate(article.title, dest=btn2.get())
    article_sum = translator.translate(article.summary, dest=btn2.get())
    art_content = translator.translate(article.text, dest=btn2.get())

    #Printing title
    title_label = Label(frame, text="Article Title:", font=art_label)
    title_label.pack(pady=3)

    article_title = Text(frame,height=2,width=65,wrap='word', font=art_cont,borderwidth=2)
    article_title.insert('end',art_title.text)
    article_title.config(state="disabled")
    article_title.pack(pady=1)

    #Printing Summary
    summary_label = Label(frame, text="Article Summary:", font=art_label)
    summary_label.pack(pady=3)

    text_box = Text(frame, height=8, width=50, wrap='word')
    text_box.insert('end', article_sum.text)
    text_box.pack(fill=BOTH,expand=True)

    # Printing Publisher date
    publish_label = Label(frame, text="Article Publish Date:", font=art_label)
    publish_label.pack(pady=3)

    article_publish = Text(frame, height=1, width=50, font=art_cont, borderwidth=2)
    if  article.publish_date == None:
        article.publish_date = "Not mentioned"
    article_publish.insert('end', article.publish_date)

    article_publish.config(state="disabled")
    article_publish.pack(pady=1)

    # Printing Image top link
    link_label = Label(frame, text="Article Image link:", font=art_label)
    link_label.pack(pady=3)

    label_image = Text(frame, height=2, width=65, font=art_cont,borderwidth=2)
    label_image.insert('end', article.top_image)
    label_image.config(state="disabled")
    label_image.pack(pady=5)

    # Printing sentiment analysis results
    sentiment_label = Label(frame, text="Sentiment Analysis:", font=art_label)
    sentiment_label.pack(pady=3)
    sentiment_result = Text(frame, height=2, width=65, wrap='word', font=art_cont, borderwidth=2)
    sentiment_result.insert('end', f"Polarity: {sentiment_polarity:.2f}, Subjectivity: {sentiment_subjectivity:.2f}")
    sentiment_result.config(state="disabled")
    sentiment_result.pack(pady=1)

#Download Article function
def download_article():
    file1 = open("News_summary_file.txt", "w+", encoding="utf-8")
    file1.write("Title:\n")
    file1.write(art_title.text)
    file1.write("\n\nArticle Text:\n")
    file1.write(art_content.text)
    file1.write("\n\nArticle Summary:\n")
    file1.write(article_sum.text)
    file1.write("\n\nArticle Publish Date:\n")
    file1.write(str(article.publish_date))
    file1.write("\n\nArticle Image link:\n")
    file1.write(str(article.top_image))
    file1.close()

#Url Entry field
Label(frame, text="URL", font=('arial', 18, 'bold')).pack()
news_url = Entry(frame, width=65, borderwidth=2, font=('verdana', 11))
news_url.configure(highlightbackground='red', highlightcolor="red")
news_url.pack(pady=5)

#Language Selection
my_label = Label(frame, text="Select Language in which you want to translate", font=art_label)
my_label.pack(pady=5)

#Radio Font
font_radio = ('calibri', 13)
btn2 = StringVar(value="en")
Radiobutton(frame, text="English", value="en", variable=btn2, font=font_radio).pack(pady=5)
Radiobutton(frame, text="Hindi", value="hi", variable=btn2, font=font_radio).pack(pady=5)
Radiobutton(frame, text="Marathi", value="mr", variable=btn2, font=font_radio).pack(pady=5)

#Translating and Summarization button
translate_button = Button(frame, text="Translate and Summarize", font=('verdana', 11, 'bold'), command=translate_news).pack(pady=6)

#Download Article button
download_button = Button(frame, text="Download Article", font=('verdana', 11, 'bold'), command=download_article)
download_button.pack(pady=6)

top.mainloop()


