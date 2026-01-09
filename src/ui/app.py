"""Streamlit UI for Personal Finance Manager."""

import os

import httpx
import pandas as pd
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")


def process_document(uploaded_file) -> dict:
    """Send document to the API for processing."""
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    response = httpx.post(f"{API_URL}/process", files=files, timeout=120.0)
    response.raise_for_status()
    return response.json()


def send_chat_query(query: str) -> str:
    """Send a chat query to the API."""
    response = httpx.post(
        f"{API_URL}/chat",
        json={"query": query},
        timeout=60.0,
    )
    response.raise_for_status()
    data = response.json()
    return data["response"]


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Personal Finance Manager",
        page_icon="💰",
        layout="wide",
    )

    st.title("Personal Finance Manager")
    st.markdown("Upload bank statements (PDF/CSV) to extract and analyze transactions.")

    with st.sidebar:
        st.header("Upload Statement")
        uploaded_file = st.file_uploader(
            "Choose a bank statement",
            type=["pdf", "csv"],
            help="Upload a PDF or CSV bank statement",
        )

        process_button = st.button("Process", type="primary", disabled=not uploaded_file)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Statement Processing")
        if process_button and uploaded_file:
            with st.spinner("Processing statement..."):
                try:
                    result = process_document(uploaded_file)

                    if result["success"]:
                        st.success(
                            f"Successfully processed {uploaded_file.name}! "
                            f"Extracted {result['transaction_count']} transactions."
                        )

                        if result["transactions"]:
                            df = pd.DataFrame(result["transactions"])
                            df.columns = ["Date", "Merchant", "Description", "Amount", "Category"]
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.info("No transactions were extracted from the file.")
                    else:
                        st.error(f"Processing failed: {result.get('message', 'Unknown error')}")

                except httpx.HTTPStatusError as e:
                    st.error(f"API error: {e.response.text}")
                except httpx.ConnectError:
                    st.error(
                        f"Could not connect to API at {API_URL}. Make sure the backend is running."
                    )
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.info("Upload a bank statement using the sidebar to get started.")

    with col2:
        st.subheader("Chat with Your Data")

        chat_container = st.container(height=400)
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        if prompt := st.chat_input("Ask about your transactions..."):
            st.session_state.messages.append({"role": "user", "content": prompt})

            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)

            with st.spinner("Analyzing..."):
                try:
                    response = send_chat_query(prompt)

                    st.session_state.messages.append({"role": "assistant", "content": response})

                    with chat_container:
                        with st.chat_message("assistant"):
                            st.markdown(response)

                except httpx.HTTPStatusError as e:
                    error_msg = f"API error: {e.response.text}"
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    with chat_container:
                        with st.chat_message("assistant"):
                            st.error(error_msg)

                except httpx.ConnectError:
                    error_msg = (
                        f"Could not connect to API at {API_URL}. Make sure the backend is running."
                    )
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    with chat_container:
                        with st.chat_message("assistant"):
                            st.error(error_msg)

            st.rerun()


if __name__ == "__main__":
    main()
