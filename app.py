import streamlit as st

from pathlib import Path

from ingest import ingest_pdf
from rag_pipeline import generate_answer


# -----------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(

    page_title="DocuMind",

    page_icon="📚",

    layout="wide"
)


# -----------------------------------
# 2. SESSION STATE
# -----------------------------------

if "processed_source" not in st.session_state:
    st.session_state.processed_source = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------------
# 3. APPLICATION HEADER
# -----------------------------------

st.title("📚 DocuMind")

st.subheader("AI-Powered Document Intelligence System")

st.write(
    "Upload your PDF documents and ask questions "
    "using Retrieval-Augmented Generation (RAG)."
)

st.divider()


# -----------------------------------
# 4. SIDEBAR
# -----------------------------------

with st.sidebar:

    st.header("📂 Document Upload")

    uploaded_file = st.file_uploader(

        "Upload your PDF",

        type=["pdf"]
    )

    if uploaded_file is not None:

        st.success(f"Selected: {uploaded_file.name}")

        if st.button("⚙️ Process PDF", use_container_width=True):

            try:

                upload_folder = Path("uploaded_docs")

                upload_folder.mkdir(exist_ok=True)

                safe_filename = Path(uploaded_file.name).name

                pdf_path = upload_folder / safe_filename

                pdf_path.write_bytes(
                    uploaded_file.getvalue()
                )

                with st.spinner("Processing your PDF..."):

                    total_chunks = ingest_pdf(
                        str(pdf_path),
                        safe_filename
                    )

                st.session_state.processed_source = safe_filename

                st.session_state.messages = []

                st.success(
                    f"Successfully processed! "
                    f"{total_chunks} chunks created."
                )

            except Exception as error:

                st.error(f"Processing failed: {error}")

    st.divider()

    st.header("📄 Current Document")

    if st.session_state.processed_source:

        st.success(st.session_state.processed_source)

    else:

        st.info("No document processed yet.")

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()


# -----------------------------------
# 5. MAIN CHAT SECTION
# -----------------------------------

st.header("💬 Chat with your PDF")


# Display previous conversation

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("sources"):

            with st.expander("📖 View Sources"):

                for source in message["sources"]:

                    st.write(
                        f"Page: {source['page_number']}"
                    )


# -----------------------------------
# 6. QUESTION INPUT
# -----------------------------------

question = st.chat_input(
    "Ask something about your PDF..."
)


# -----------------------------------
# 7. GENERATE ANSWER
# -----------------------------------

if question:

    if not st.session_state.processed_source:

        st.warning("Please upload and process a PDF first.")

    elif (
        uploaded_file is not None
        and uploaded_file.name != st.session_state.processed_source
    ):

        st.warning("Please process the newly selected PDF first.")

    else:

        st.session_state.messages.append({

            "role": "user",

            "content": question

        })

        with st.chat_message("user"):

            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("DocuMind is thinking..."):

                try:

                    answer, sources = generate_answer(

                        question,

                        st.session_state.processed_source

                    )

                    st.markdown(answer)

                    if sources:

                        with st.expander("📖 View Sources"):

                            for source in sources:

                                st.write(
                                    f"Page: {source['page_number']}"
                                )

                    st.session_state.messages.append({

                        "role": "assistant",

                        "content": answer,

                        "sources": sources

                    })

                except Exception as error:

                    st.error(f"Answer generation failed: {error}")