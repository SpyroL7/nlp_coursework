import re
import html
from collections import Counter


def clean_data(text: str) -> str:
  if not isinstance(text, str):
    return text
    
  # turns """text""" and ""text"" into "text"
  text = re.sub(r'"{2,}', '"', text)
  
  # standardises whitespace
  text = re.sub(r'\s+', ' ', text).strip()
  
  # fixes HTML artifacts (&amp; -> &)
  text = html.unescape(text)
  
  return text

def main():
  # dataset = "dontpatronizeme_pcl.tsv"
  # dataset = "synthetic_pcl_data.tsv"
  dataset = "synthetic_pcl_data2.tsv"

  keep_punctuation = False

  # if keep_punctuation:
  #   # splits off punctuation into distinct tokens
  #   re_punctuation_string = r'(\s+|[,;:"()/.\'])'
  # else:
  #   # splits at punctuation, removing it
  #   re_punctuation_string = '[\s,;:"()/.\']'

  # instead of splitting on set symbols, use negative set of numbers and letters
  re_find_string = r'\d+|[a-z]+|[^\w\s]'

  stop_words = {'and', 'the', 'a', 'an', 'is', 'in', 'that', 'this', 'there'}

  vocab = set()
  avg_len = 0
  count = 0
  max_len = 0
  min_len = float('inf')

  stop_word_count = 0
  bigrams = Counter()

  label_counter = [0, 0, 0, 0, 0]
  labels = set()


  with open(dataset, 'r', encoding='utf-8') as file:
    # skip the first 4 lines
    for _ in range(4):
      next(file)

    for line in file:
      line = line.strip()
      text = line.split('\t')[4]

      label = int(line.split('\t')[5])
      label_counter[label] += 1
      labels.add(label)

      text = clean_data(text)
      tokenised_text = re.findall(re_find_string, text.lower())  # splits on any non-alphanumeric symbol and keeps it
      # raw_tokens = re.split(re_punctuation_string, text)
      # tokenised_text = [t.lower() for t in raw_tokens if t and not t.isspace()]

      # print(tokenised_text)
      # print("---------")
      stop_word_count += len([t for t in tokenised_text if t in stop_words])
      tt_no_punctuation_or_stop_words = [t for t in tokenised_text if (t.isalnum() or t == "'") and t not in stop_words]
      # tt_no_punctuation = [t for t in tokenised_text if (t.isalnum() or t == "'")]
      # paragraph_bigrams = zip(tt_no_punctuation_or_stop_words, tt_no_punctuation_or_stop_words[1:])
      paragraph_bigrams = zip(tt_no_punctuation_or_stop_words, tt_no_punctuation_or_stop_words[1:], tt_no_punctuation_or_stop_words[2:])

      bigrams.update(paragraph_bigrams)

      length = len(tokenised_text)
      # if length == 0 or length == 1:
      #   continue  # para 8640 is empty, para 1656 = 'refugees'
      max_len = max(max_len, length)
      min_len = min(min_len, length)
      avg_len = (avg_len * count + length) / (count + 1)

      count += 1
      vocab.update(tokenised_text)

  print(f"vocab size: {len(vocab)}")
  print(f"avg paragraph length: {avg_len:.1f}")
  print(f"max length: {max_len}")
  print(f"min length: {min_len}")
  print(f"total paragraphs: {count}")

  print(f"labels: {labels}")
  print(f"number of paragraphs per label: {label_counter}")
  print(f"negative paragraphs (label=0,1): {label_counter[0] + label_counter[1]}, positive paragraphs (label=2,3,4): {label_counter[2] + label_counter[3] + label_counter[4]}")


  print("-------------------------------")

  print(f"stop words: {stop_word_count} / {int(avg_len*count)} = {stop_word_count*100/(avg_len*count):.2f}%")
  # print("Top 10 Most Common Bigrams:")
  # for (w1, w2, w3), count in bigrams.most_common(20):
  #     print(f"{w1} {w2} {w3}: {count}")


if __name__ == "__main__":
  main()