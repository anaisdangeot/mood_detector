import matplotlib.pyplot as plt
from wordcloud import WordCloud
import sys,os
os.chdir(sys.path[0])

text = open('lyrics_parts_test.txt',mode="r",encoding='utf-8').read()
wc = WordCloud(mode = "RGBA", background_color=None,  height=1600, width=1400)
wc.generate(text)
wc.to_file('gghj.png')
...
