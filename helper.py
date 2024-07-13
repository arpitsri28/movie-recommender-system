import ast
import nltk
from nltk.stem.porter import PorterStemmer

def convert(obj):
  l=[]
  for i in ast.literal_eval(obj):
    l.append(i['name'])
  return l

def convert_cast(obj):
  l=[]
  counter = 0
  for i in ast.literal_eval(obj):
    if counter != 3:
      l.append(i['name'])
      counter = counter + 1
    else:
      break
  return l

def fetch_director(obj):
  l=[]
  for i in ast.literal_eval(obj):
    if i['job'] == 'Director':
      l.append(i['name'])
      break
  return l

ps = PorterStemmer()
def stem(text):
  y = []
  for i in text.split():
    y.append(ps.stem(i))
  
  string = " ".join(y)
  return string