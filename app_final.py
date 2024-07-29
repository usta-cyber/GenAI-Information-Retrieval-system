import streamlit as st
from src.helper import get_pdf_text, get_text_chunks, get_vector_store, get_conversational_chain

# Define a function to handle user input and display chat history
def user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chatHistory = response['chat_history']
    for i, message in enumerate(st.session_state.chatHistory):
        if i % 2 == 0:
            st.markdown(f"**User:** {message.content}")
        else:
            st.markdown(f"**Reply:** {message.content}")

# Main function to set up the Streamlit app
def main():
    st.set_page_config(page_title="Document Information Retrieval System", layout="wide")
    
    st.markdown("""
        <style>
            .main {
                background-color: #f0f2f6;
                padding: 20px;
            }
            .sidebar .sidebar-content {
                background-color: #dfe6e9;
            }
            .stTextInput input {
                border-radius: 10px;
            }
            .stButton button {
                border-radius: 10px;
                background-color: #0984e3;
                color: white;
            }
            .stButton button:hover {
                background-color: #74b9ff;
            }
            .stMarkdown {
                padding: 10px;
                border-radius: 5px;
                background-color: #dfe6e9;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("📄 Document Information Retrieval System")
    
    # Input field for user's question
    user_question = st.text_input("🔍 Ask a Question from the PDF Files", "")

    # Initialize session state variables
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = []

    # Handle user input
    if user_question:
        user_input(user_question)

    # Sidebar for file upload and processing
    with st.sidebar:
        st.header("Menu")
        pdf_docs = st.file_uploader("📁 Upload your PDF Files", accept_multiple_files=True)
        if st.button("Submit & Process"):
            if pdf_docs:
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    vector_store = get_vector_store(text_chunks)
                    st.session_state.conversation = get_conversational_chain(vector_store)
                    st.success("Done! You can now ask questions from the PDFs.")
            else:
                st.warning("Please upload at least one PDF file.")

if __name__ == "__main__":
    main()
