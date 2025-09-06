from langchain_experimental.agents import create_csv_agent
from dotenv import load_dotenv
import os
import streamlit as st
from langchain_openai import OpenAI


def main():
    # Load environment variables
    load_dotenv()

    # Optionally set API key directly (not recommended for production)
    os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY", "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")

    if not os.environ['OPENAI_API_KEY']:
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(page_title="Abbey asks CSV")
    st.header("Ask your CSV")

    csv_file = st.file_uploader("Upload a CSV file", type="csv")

    if csv_file is not None:
        # Save the uploaded CSV to a temporary file
        temp_path = "temp.csv"
        with open(temp_path, "wb") as f:
            f.write(csv_file.getvalue())

        # Create the agent (order of arguments fixed)
        agent = create_csv_agent(
            OpenAI(temperature=0),
            temp_path,
            verbose=True,
            allow_dangerous_code=True
        )

        user_question = st.text_input("Ask a question about your CSV:")

        if user_question:
            with st.spinner(text="In progress..."):
                st.write(agent.run(user_question))

        # Remove the temporary file
        os.remove(temp_path)


if __name__ == "__main__":
    main()
