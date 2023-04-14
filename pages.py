import pandas as pd
import streamlit as st
from stqdm import stqdm

from utils.article import parse_url
from utils.gpt import process_url
from utils.nlp import nlp


def preview_page():
    url = st.text_input(
        "Please enter the article URL to preview parsed results",
        "https://www.cntraveler.com/gallery/best-things-to-do-in-tokyo",
    )

    if not len(url):
        st.markdown("**PLEASE ENTER VALID URL**")

    data = parse_url(url)

    raw, gpt_parsed, parsed = st.tabs(["Raw Results", "[Beta] GPT Parsed Results", "[Beta] NLP Parsed Results"])

    with raw:
        st.markdown("### Description")
        st.markdown("**The raw results show the header in the article in different levels.**")

        st.markdown("### Header Results")
        for k, v in data.items():
            st.markdown(f"#### {k.capitalize()}")
            st.json(v)

    with gpt_parsed:

        st.markdown("### Description")
        st.markdown("After we got the title, use GPT-3.5 to parse the attractions.")
        st.markdown("`It may take a while to process the results.`")

        st.markdown("### Results")

        gpt_raw_result = process_url(url)
        output_result = [
            ele.strip() for ele in gpt_raw_result.replace("[", "").replace("]", "").replace("'", "").split(",")
        ]

        st.write(output_result)

    with parsed:

        st.markdown("### Description")
        st.markdown("**The parsed results show the Special Nouns extracted from titles.**")

        st.markdown("### Results")
        all_res = []
        for k, v in data.items():
            doc = nlp(", ".join(v))

            res = pd.DataFrame({"noun": [e.text for e in doc.ents], "noun_type": [e.label_ for e in doc.ents]})
            all_res.append(res)
        df = pd.concat(all_res).drop_duplicates(subset=["noun"]).sort_values("noun")

        st.markdown("### Noun Type Filter")
        noun_types = st.multiselect(
            label="Select Target Noun Types",
            options=df.noun_type.unique(),
            # default=('GPE', 'LOC', 'PERSON')
        )
        final_df = df[df.noun_type.isin(noun_types)].copy()

        st.markdown(f"Total num of results: {final_df.shape[0]}")
        st.dataframe(final_df.reset_index(drop=True))

        st.download_button(
            label="Download filtered results",
            data=final_df.to_csv(index=False),
            file_name="article_parsed_result.csv",
        )


def batch_update_page():

    st.markdown("### Batch Update Page")
    st.markdown(
        """
    1. Upload CSV file containing article links
    2. Choose the url column
    3. Press `EXECUTE` button to start the process
    4. Press `DOWNLOAD` button to download results
    """
    )

    st.markdown("#### 1. Upload File")
    uploaded_file = st.file_uploader(label="Choose the CSV file here")

    if not uploaded_file:
        raise ValueError("Please Choose a Valid Filepath")

    raw_df = pd.read_csv(uploaded_file)

    st.markdown("##### Data Preview")
    st.dataframe(raw_df.head(10))

    st.markdown("#### 2. Choose URL Column")
    col = st.selectbox(label="Choose the column of URL", options=raw_df.columns)

    st.markdown("#### 3. Processing")
    df = raw_df.copy()

    execute_button = st.button(label="EXECUTE")
    if execute_button:
        result_list = []
        for url in stqdm(df[col].values):
            _res = process_url(url)
            result_list.append({col: url, "POI": _res})

        st.markdown("#### 4. Results")
        if result_list:
            result_df = pd.DataFrame(result_list)
            st.dataframe(result_df)
            filepath = st.text_input(label="Filename", value="parsed_results")
            st.download_button(
                label="DOWNLOAD RESULTS",
                data=result_df.to_csv(index=False),
                file_name=f"{filepath}.csv",
            )
