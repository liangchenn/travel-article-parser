import re
import json
from collections import defaultdict

import pandas as pd
import streamlit as st

from utils.article import parse_url
from utils.nlp import nlp
from utils.gpt import PROMPT
from utils.gpt import process_text_with_gpt 
        
        
    

st.header("Minimal Article Parser")

url = st.text_input("Please enter the article URL", 'https://www.cntraveler.com/gallery/best-things-to-do-in-tokyo')

if not len(url):
    st.markdown("**PLEASE ENTER VALID URL**")

data = parse_url(url)

raw, gpt_parsed, parsed = st.tabs(['Raw Results', '[Beta] GPT Parsed Results', '[Beta] NLP Parsed Results'])


with raw:
    st.markdown("### Description")
    st.markdown("**The raw results show the header in the article in different levels.**")
    
    st.markdown("### Header Results")    
    for k, v in data.items():
        st.markdown(f'#### {k.capitalize()}')
        st.json(v)

with gpt_parsed:

    st.markdown("### Description")
    st.markdown("After we got the title, use GPT-3.5 to parse the attractions.")
    st.markdown("`It may take a while to process the results.`")

    st.markdown("### Results")
    
    all_lst = []
    for h, lst in data.items():
        all_lst.extend(lst)
    # st.write(str(all_lst))

    gpt_raw_result = process_text_with_gpt(PROMPT + str(all_lst))

    output_result = [ele.strip() for ele in gpt_raw_result.replace("[", "").replace("]", "").replace("'", "").split(",")]


    st.write(output_result)

    
    
with parsed:
    
    
    st.markdown("### Description")
    st.markdown("**The parsed results show the Special Nouns extracted from titles.**")
    
    
    st.markdown("### Results")
    all_res = []
    for k, v in data.items():
        doc = nlp(', '.join(v))
        
        res = pd.DataFrame(
            {
                "noun": [e.text for e in doc.ents],
                "noun_type": [e.label_ for e in doc.ents]
                
            }
        )
        all_res.append(res)
    df = pd.concat(all_res).drop_duplicates(subset=['noun']).sort_values("noun")
    
    st.markdown("### Noun Type Filter")
    noun_types = st.multiselect(
        label="Select Target Noun Types",
        options=df.noun_type.unique(),
        # default=('GPE', 'LOC', 'PERSON')
        )
    final_df = df[df.noun_type.isin(noun_types)].copy()
    
    st.markdown(f"Total num of results: {final_df.shape[0]}")
    st.dataframe(final_df.reset_index(drop=True))
    
    st.download_button(label="Download filtered results", data=final_df.to_csv(index=False), file_name='article_parsed_result.csv')