import openai
import pandas as pd

openai.api_key = "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"

prompt = """Classes: [`physics`, `chemistry`, `biology`, `mathematics`]
Classify the text into one of the above classes, and output only the class name.###\n"""

with open('ChannelData.csv') as file:
    titles = []
    responses = []
    for title in file:
      title = title.strip()
      if title == "video_title":
         continue
  
      res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.6,
        messages=[
          {"role": "user", "content": prompt+"Text: "+title},
        ],
        max_tokens=1
      )
      titles.append(title)
      predClass = res.choices[0].message.content.strip()
      responses.append(predClass)

      final_data = {'video_title': titles, 'class': responses} # Merge the data to form the final dataset
      table = pd.DataFrame(final_data)
      table.to_csv('Classification.csv', encoding='utf-8', index=False)

      print(title, predClass)
