import streamlit as st
from agents.writeragent import get_writer_agent
from agents.researcheragent import get_researcher_agent
from agents.editoragent import get_editor_agent
import pdfkit
import markdown2
from io import BytesIO


def main():
    st.title("AI Content Creation Agents - Article Generator")
    
    with st.sidebar:
        st.header("Settings")
        tone = st.selectbox("Tone", ["Professional", "Casual", "Technical"])
        sections = st.slider("Sections", 3, 6, 4)
        use_serpapi = st.checkbox("Enable Web Research", True)

    
    topic = st.text_input("Enter your topic:")
    
    if st.button("Generate Content"):
        with st.spinner("Creating content..."):
            # Initialize agents\
            st.write("Initializing  Researcher, Writer, and Editor agents...")
            researcher = get_researcher_agent()
    
            writer = get_writer_agent()
            editor = get_editor_agent()
            
            # Execute pipeline
            research = researcher.research_pipeline(topic)
            draft = writer.write_draft(research, tone)
            edited = editor.edit_content(draft)
            
            # Display results
            with st.expander("Research Results"):
                st.markdown(research)
            
            with st.expander("First Draft"):
                st.markdown(draft)
            
            with st.expander("Final Content"): 
                st.subheader("Final Version")
                st.markdown(edited)



                # Convert Markdown to HTML
                html_content = markdown2.markdown(edited)

                # Generate PDF
                # pdf = pdfkit.from_string(html_content, False)

                # Create text file content
                text_content = edited.encode()

                # PDF download button
                # st.download_button(
                #     label="Download PDF",
                #     data=pdf,
                #     file_name="final_content.pdf",
                #     mime="application/pdf"
                # )

                # Text file download button
                st.download_button(
                    label="Download Text",
                    data=text_content,
                    file_name="final_content.txt",
                    mime="text/plain"
                )
               

if __name__ == "__main__":
    main()