from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.analysis import StemmingAnalyzer
from textblob import TextBlob
import os.path
import json, os

wd = os.getcwd() +"\\scrappedata\\"


# Specify schema
schema = Schema(
            title=              TEXT(stored=True, analyzer=StemmingAnalyzer()),
            author=             TEXT,
            movie=              KEYWORD(stored=True, lowercase=True),
            url=                ID(stored=True),
            passage=            TEXT(analyzer=StemmingAnalyzer()),
            passage_summary=    STORED,
            meta_data=          STORED,
            ending_type=        KEYWORD(stored=True, lowercase=True)
        )

# Creates the index
if not os.path.exists("index"):
    os.mkdir("index")
    ix = create_in("index", schema)
else:
    ix = open_dir("index")

writer = ix.writer()
# writer.add_document(
#     title=u'Testing is this correction',
#     author=u'Bill Gates',
#     movie=u'Batman',
#     url=u'https://testingonetwo.com',
#     passage=u'Some super duper long ass passage that no one wants to read. I am having difficulties trying to think of what else to write.',
#     passage_summary=u'Some super duper long ass passage that no one wants to read.'
# )
print(wd)
count = 0
#keys Movie, Title, Author, Hyperlink, Passage, Summary
while(True):
    txtfile = (wd+"textfile%i.txt" % (count))
    if os.path.exists(txtfile):
        print(count)
        with open(txtfile, 'r', encoding ="utf-8") as txt_file:
            datastore = json.load(txt_file)
            for i in range(len(datastore)):
                t = datastore[i]["Title"]
                a = datastore[i]["Author"]
                m = datastore[i]["Movie"]
                h = datastore[i]["Hyperlink"]
                p = datastore[i]["Passage"]
                s = datastore[i]["Summary"]
                md = datastore[i]["MetaData"]

                lp = datastore[i]["LastChapter"]
                blob = TextBlob(lp)
                score = 0.0
                for sentence in blob.sentences:
                    score = score + sentence.sentiment.polarity*sentence.sentiment.subjectivity
                print(score)
                if score > 0.1:
                    et = "Positive"
                elif score < -0.1:
                    et = "Negative"
                else:
                    et = "Neutral"
                print(et)
                writer.add_document (
                title = t,
                author = a,
                movie = m,
                url = h,
                passage = p,
                passage_summary = s,
                meta_data = md,
                ending_type= et
                )
                
        count = count + 1
    else:
        break
            
writer.commit()



