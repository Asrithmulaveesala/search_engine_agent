
import streamlit as st
import tempfile
import os

from agent import create_search_agent

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="AI Search Engine Agent",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 AI Search Engine Agent")
st.caption(
    "Ask questions about general knowledge, research papers, or an uploaded PDF."
)

# ---------------- Session State ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_executor" not in st.session_state:
    st.session_state.agent_executor = None

if "pdf_temp_path" not in st.session_state:
    st.session_state.pdf_temp_path = None

if "connected" not in st.session_state:
    st.session_state.connected = False

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("⚙️ Configure Agent")

    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="Enter your Groq API key"
    )

    uploaded_pdf = st.file_uploader(
        "Upload PDF (Optional)",
        type=["pdf"],
        help="A PDF is only needed for questions about your document."
    )

    initialize = st.button(
        "Initialize Agent",
        use_container_width=True
    )

    if initialize:
        if not groq_api_key.strip():
            st.error("Please enter your Groq API key.")

        else:
            new_pdf_path = None

            try:
                with st.spinner("Initializing agent..."):

                    # Save the PDF only if one was uploaded
                    if uploaded_pdf is not None:
                        with tempfile.NamedTemporaryFile(
                            delete=False,
                            suffix=".pdf"
                        ) as temp_file:
                            temp_file.write(uploaded_pdf.getvalue())
                            new_pdf_path = temp_file.name

                    # Initialize with or without a PDF
                    new_executor = create_search_agent(
                        groq_api_key=groq_api_key,
                        pdf_path=new_pdf_path
                    )

                    old_pdf_path = st.session_state.pdf_temp_path

                    st.session_state.agent_executor = new_executor
                    st.session_state.pdf_temp_path = new_pdf_path
                    st.session_state.connected = True
                    st.session_state.messages = []

                    # Remove the previous temporary PDF after success
                    if old_pdf_path and os.path.exists(old_pdf_path):
                        try:
                            os.remove(old_pdf_path)
                        except OSError:
                            pass

                st.success("Agent initialized successfully!")

            except Exception as e:
                st.session_state.agent_executor = None
                st.session_state.connected = False

                if new_pdf_path and os.path.exists(new_pdf_path):
                    try:
                        os.remove(new_pdf_path)
                    except OSError:
                        pass

                st.error(f"Initialization failed: {e}")

    st.divider()

    if st.session_state.connected:
        st.success("Agent is ready.")
    else:
        st.info("Enter your API key and initialize the agent.")

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.button("Disconnect Agent", use_container_width=True):
        st.session_state.agent_executor = None
        st.session_state.connected = False
        st.session_state.messages = []

        old_pdf_path = st.session_state.pdf_temp_path
        if old_pdf_path and os.path.exists(old_pdf_path):
            try:
                os.remove(old_pdf_path)
            except OSError:
                pass

        st.session_state.pdf_temp_path = None
        st.rerun()

# ---------------- Display Chat History ----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- Chat Interface ----------------
question = st.chat_input(
    "Ask a question about anything, research, or your PDF..."
)

if question:
    if st.session_state.agent_executor is None:
        st.warning(
            "Please enter your Groq API key and click "
            "'Initialize Agent'. PDF upload is optional."
        )

    else:
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            try:
                with st.spinner("Agent is searching..."):
                    response = st.session_state.agent_executor.invoke({
                        "input": question
                    })

                    answer = response["output"]

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Failed to generate answer: {e}")


