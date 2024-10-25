import streamlit as st
from openai import OpenAI

# UCase_006(v002): Submit request PB was added
st.set_page_config(page_title="Industry_#002", page_icon="📊")

# Load the API key from secrets
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["openai"]["api_key"]
else:
    openai_api_key = st.session_state.api_key
    client = OpenAI(api_key=openai_api_key)

# Page 1: Fanuc Robot Assistant
def fanuc_robot_assistant():
    st.markdown("# 📄 Fanuc Robot Assistant")
    st.markdown(
        """
        The Fanuc Robot Assistant supports automated operations, error troubleshooting, and 
        configuration management of industrial robots. It helps in diagnosing and resolving 
        common errors in Fanuc robotic systems for smooth manufacturing workflows.
        """
    )
    st.write("More details about Fanuc Robot Assistant functionalities will be added here.")

    # Ask for the alarm code directly instead of uploading a document.
    st.write(" I'm Lucas_7, your Fanuc Robot Assistant powered by OpenAI API!")
    st.write(" I will provide you the explanation and road map for troubleshooting a robot alarm code.")
    St.write ("Note: This GPT still on trainning, sothe answers are not accurate yet"
    alarm_code = st.text_area(
        "Describe the Robot Alarm Code:",
        placeholder="Enter the alarm code (e.g., SRVO-023 or a description of the issue)...",
    )

    # Add a Submit button to trigger the request
    if st.button("Submit"):
        if alarm_code:
            # Construct the specific prompt for the AI assistant.
            question = f"Can you give me the explanation and road map to troubleshoot specific Fanuc Robot alarm code: {alarm_code}"

            # Generate a response using the OpenAI API.
            messages = [
                {
                    "role": "user",
                    "content": question,
                }
            ]

            stream = client.chat.completions.create(
                model="gpt-4",
                temperature=1.3,
                max_tokens=256,
                messages=messages,
                stream=True,
            )

            # Display the response in the app using `st.write_stream`.
            st.write_stream(stream)
        else:
            st.error("Please enter a robot alarm code before submitting.")

# Page 2: Configurations of Electronic Components Assistant
def electronic_components_assistant():
    st.markdown("# 📄 Configurations of Electronic Components Assistant")
    st.markdown(
        """
        This assistant helps with the setup and configuration of electronic components 
        used in manufacturing systems. It ensures optimal configurations for the best 
        performance and compatibility across different systems.
        """
    )
    st.write("More details about Configurations of Electronic Components will be added here.")

# Page 3: Factory Asset Effectiveness
def factory_asset_effectiveness():
    st.markdown("# 📄 Factory Asset Effectiveness")
    st.markdown(
        """
        Tracking factory asset effectiveness is key to optimizing manufacturing operations. 
        This assistant helps in monitoring and improving Overall Equipment Effectiveness (OEE) 
        by analyzing machine performance, downtime, and output quality.
        """
    )
    st.write("More details about Factory Asset Effectiveness will be added here.")

# Page 4: Documentation
def documentation():
    st.markdown("# 📄 Documentation ")
    st.markdown(
        """
        At this section you will find the documentation about the cases explained for the Bussines units.
        """
    )
    st.write("Documentation will be added here.")

# Main Page Selection
page_names_to_funcs = {
    "—": lambda: st.write("Select a page from the sidebar."),
    "📄 Fanuc Robot Assistant": fanuc_robot_assistant,
    "📄 Configurations of Electronic Components Assistant": electronic_components_assistant,
    "📄 Factory Asset Effectiveness": factory_asset_effectiveness,
    "📄 Documentation": documentation,
}

# Sidebar for Navigation
st.sidebar.header("AI AT MANUFACTURING 4.0")
demo_name = st.sidebar.selectbox("Choose a use case", page_names_to_funcs.keys())
st.markdown("# AI AT MANUFACTURING 4.0")

# Render Main Introductory Content Only on Main Page
if demo_name == "—":
    st.markdown(
        """
        Manufacturing 4.0 integrates AI to optimize manufacturing processes. Explore use cases that show how 
        AI assistants can enhance productivity, troubleshooting and equipment monitoring.
        
        **Explore Use Cases:**
        - 📄 Fanuc Robot Assistant.
        - 📄 Configurations of electronic components Assistant.
        - 📄 Factory Asset Effectiveness.
        - 📄 Documentation.
        """
    )
    st.write("👈 Select a demo from the dropdown on the left to explore examples of what AI assistance can achieve!")

# Render Selected Page
page_names_to_funcs[demo_name]()
