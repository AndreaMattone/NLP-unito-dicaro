import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud, STOPWORDS

f = open("dataset.txt", "r")
text = f.read()
wordcloud = WordCloud(width=1920, height=1080, random_state=1, background_color='blue',
                      collocations=False, stopwords=STOPWORDS).generate(text)
plt.figure(figsize=(8, 7))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

a = np.random.random((20, 20))
plt.imshow(a, cmap='hot', interpolation='nearest')
plt.show()
