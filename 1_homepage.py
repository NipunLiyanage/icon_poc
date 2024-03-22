import streamlit as st
import pathlib
import textwrap

import google.generativeai as genai
import PIL.Image

import textwrap
from fpdf import FPDF
import os

st.set_page_config(
    initial_sidebar_state="collapsed",
    layout="wide"
)

def text_to_pdf(text, filename):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Arial', size=fontsize_pt)
    splitted = text.split('\n')

    for line in splitted:
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)

    pdf.output(filename, 'F')

    with open(filename, "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    os.remove(filename)

    return PDFbyte

   

st.markdown("<h1 style='text-align: center; color: black;'>Blood Report Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: grey;'>Reports, Simplified! </h3>", unsafe_allow_html=True)



st.divider()

col1, col2, col3 = st.columns(3)

genai.configure(api_key=st.secrets["token"])

model = genai.GenerativeModel('gemini-pro-vision')

with col2:



    file = st.file_uploader(":green[**Select your Blood Report (JPG or PNG)**]", type=['png', 'jpg'], accept_multiple_files=False, key="Uploaded", help=None, on_change=None, args=None, kwargs=None,disabled=False, label_visibility="visible")

    disabledButton = False
    if file == None:
        disabledButton=True

    if disabledButton:
        st.markdown(':red[**Please Upload a report to continue.**]')

    button = st.button('Start',disabled=disabledButton,key='startBtn')

if button:

    if file is not None:
        img = PIL.Image.open(file)

        # response = model.generate_content(img)
        response = model.generate_content(["""
                        This is a image of a COMPLETE BLOOD COUNT (CBC) it's a one of the most important blood tests that your doctor will order is a complete blood count (CBC), an inventory of different types of blood cells. These can be grouped into three categories: red blood cells, white blood cells and platelets. Knowing how many of these cells are in a blood sample provides a lot of valuable information.
                        Go through each value and describe them like a docter describing it to a patient. Use the reference range from the image only. Imagine this is my blood report and you are a doctor but do not make the response like a letter but a report:
                        """, img], stream=True)
        response.resolve()

        st.write(response.text)

        pdf_file = text_to_pdf(response.text, 'summarized result.pdf')

        st.divider()
        st.markdown(':red[**The report will dissapear from the screen when you click download.**]')

        st.download_button(
            label="Download",
            data=pdf_file,
            file_name='result.pdf',
            mime='application/pdf',
        )





