import streamlit as st
import searchconsole
import pandas as pd
from pathlib import Path
import json
import pandas as pd
#from io import StringIO

###########################################

from contextlib import contextmanager
from io import StringIO
from streamlit.report_thread import REPORT_CONTEXT_ATTR_NAME
from threading import current_thread
from time import sleep
import streamlit as st
import sys


@contextmanager
def st_redirect(src, dst):
    old_write = src.write

    with StringIO() as buffer:
        def new_write(b):
            if getattr(current_thread(), REPORT_CONTEXT_ATTR_NAME, None):
                buffer.write(b)
                dst(buffer.getvalue())
            else:
                old_write(b)

        try:
            src.write = new_write
            yield
        finally:
            src.write = old_write


@contextmanager
def st_stdout(dst):
    with st_redirect(sys.stdout, dst):
        yield


@contextmanager
def st_stderr(dst):
    with st_redirect(sys.stderr, dst):
        yield


def main():
    out1 = st.empty()
    with st_stdout(out1.code):
        print("Hello")
        sleep(1)
        print("World")

    out2 = st.empty()
    with st_stdout(out2.info):
        print("Goodbye")
        sleep(1)
        print("World")


if __name__ == "__main__":
    main()


###########################################

st.set_option('deprecation.showfileUploaderEncoding', False)

st.title("Connect to GSC via Josh Carty code")
st.header("Try JC's former code - it may work")
st.write("https://github.com/jcchouinard/GoogleSearchConsole-Tutorial")

uploaded_file = st.file_uploader("Choose a file")

if not uploaded_file:
    st.warning('Upload your credentials first. ☝️')
    st.stop()

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.read()
    #st.write(type(bytes_data))
    #st.write(bytes_data)
    import json
    JsonFromString = json.loads(bytes_data)
    st.header("First JSON file!")
    st.write(JsonFromString)

site = 'https://www.tatielou.co.uk/'    # Property to extract

num_days = 5                    # Number of Days, Months to Extract
#creds = 'GSCTatieLouCredentialsNonLegacy.json'
output = 'gsc_data.csv'

st.header("Proceed to Oauth")

my_file = Path("credentials.json")
#if st.button('Proceed to Oauth'):


if my_file.is_file():
    #account = searchconsole.authenticate(client_config=JsonFromString,credentials='credentials.json')
    account = searchconsole.authenticate(client_config=JsonFromString,credentials='credentials.json')
    webproperty = account['https://www.tatielou.co.uk/']
    report = webproperty.query.range('today', days=-7).dimension('query').get()
    df = pd.DataFrame(report.rows)
    st.write(df)
else:
    #account = searchconsole.authenticate(client_config=JsonFromString,serialize='credentials.json')
    #Synode's code ###############
    outputStdout = st.empty()
    with st_stdout(outputStdout.info):
        account = searchconsole.authenticate(client_config=JsonFromString,serialize='credentials.json', flow="console")
        #searchconsole.authenticate(client_config="GSCTatieLouCredentials.json", serialize='credentials.json', flow="console")
    #st.write('No, credentials.json doesnt exist')


try:
    with open("credentials.json", "r") as f:
        my_dict = json.load(f)
    st.header("2nd JSON file: credentials.json")
    st.write(my_dict)
except FileNotFoundError:
    st.warning('credentials.json NOT THERE')

st.checkbox("checkboxTest")
st.stop()

