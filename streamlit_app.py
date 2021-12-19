import streamlit as st
import os
from PIL import Image
from convert_image_to_text import pdf2texts
from convert_image_to_text import image2text
import main
from load_css import local_css


def load_image(image_file):
	img = Image.open(image_file)
	return img


icon = load_image('Bchecker.ico')
st.set_page_config(
	page_title='Bchecker',
	page_icon=icon
)
local_css("style.css")
st.title('Plagiarism Checker')
menu = st.sidebar.selectbox('Menu', ('Image', 'Text'))
text = ''
if menu == 'Image':
	st.subheader('Upload Files')
	file = st.file_uploader('')
	if file is not None:
		file_details = {'File_Name': file.name, 'File_Type': file.type}
		# Saving file
		with open(file.name, 'wb') as f:
			f.write(file.getbuffer())
		if file.type[:5] == 'image':
			# Convert image to text
			text = image2text(file.name)
		elif file.type[-3:] == 'pdf':
			# Convert image to text
			text = pdf2texts(file.name)
			st.write(text)

		else:
			st.write('This is not an image file')

		if os.path.exists(file.name):
			os.remove(file.name)
		else:
			pass
elif menu == 'Text':
	text = st.text_area('Copy and Paste your document here')
if text != '':
	score, sim_words, clean_text, urls = main.text_similarity_score(text)
	st.write(clean_text)
	st.write(score)
	st.write(urls)
	data_words = clean_text.split()
	colored_text = '<h>'
	for i in range(len(data_words)):
		if data_words[i] in sim_words:
			data_words[i] = "<span class='bold highlight' >" + data_words[i] + "</span>"
		colored_text += data_words[i] + ' '
	colored_text += '</h>'
	st.markdown(colored_text, unsafe_allow_html=True)
