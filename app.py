import streamlit as st
from crew import ask
from fpdf import FPDF


# Custom FPDF class for proper formatting
class PDF(FPDF):
    def header(self):
        self.set_font("Times", "B", 14)
        self.cell(0, 10, "AI-Powered Insight Wizard Report", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Times", "I", 8)
        self.cell(0, 10, "Generated by AI Insight Wizard | Powered by CrewAI", 0, 0, "C")


def format_and_clean(text):
    # Remove markdown styling
    text = text.replace("**", "").replace("##", "").replace("###", "").replace("* ", "- ")
    return text


# Save content to a structured PDF
def save_to_pdf(content, filename="Company_Research_Report.pdf"):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Times", "", 12)

    sections = [
        ("Industry Research Report", content[0]),
        ("AI Use Cases", content[1]),
        ("Resource Collection", content[2]),
    ]

    for section_title, section_text in sections:
        # Section Title
        pdf.set_font("Times", "B", 13)
        pdf.cell(0, 10, section_title, ln=True)
        pdf.ln(2)
        pdf.set_font("Times", "", 12)

        # Clean and format content
        formatted_lines = format_and_clean(section_text).split("\n")
        for line in formatted_lines:
            line = line.strip()
            if not line:
                continue

            # Subsections (Headings with colon)
            if line.endswith(":") and not line.lower().startswith("http"):
                pdf.set_font("Times", "B", 12)
                pdf.multi_cell(0, 8, line)
                pdf.set_font("Times", "", 12)
                pdf.ln(1)
            # Numbered Points
            elif line[:2].isdigit() or (len(line) > 2 and line[1] == "." and line[0].isdigit()):
                pdf.set_font("Times", "B", 12)
                pdf.multi_cell(0, 8, line)
                pdf.set_font("Times", "", 12)
                pdf.ln(1)
            # Bullets
            elif line.startswith("- "):
                pdf.multi_cell(0, 8, f"  - {line[2:]}")
            # Regular paragraphs
            else:
                pdf.multi_cell(0, 8, line)
        pdf.ln(5)

    pdf.output(filename)


# Streamlit App
def main():
    st.set_page_config(page_title="AI Insight Wizard", layout="centered")
    st.title("🌐 AI-Powered Insight Wizard 🌐")
    st.subheader("Your Ultimate Assistant for Industry Research & Innovation")

    st.markdown("""
        Welcome to the AI Insight Wizard!  
        Generate in-depth industry insights, discover transformative AI use cases,  
        and compile tailored resources for seamless innovation.
    """)

    st.markdown("### Enter a Company or Industry to Begin:")
    query = st.text_input("e.g., Fintech, Renewable Energy, SpaceX")

    if 'response' not in st.session_state:
        st.session_state.response = []

    if st.button("Generate Insights"):
        response = ask(query)
        st.session_state.response = [
            response.tasks_output[0].raw,
            response.tasks_output[1].raw,
            response.tasks_output[2].raw,
        ]

        section_labels = ["Industry Research Report", "AI Use Cases", "Resource Collection"]
        for i, label in enumerate(section_labels):
            st.markdown(f"### {label}")
            st.write(st.session_state.response[i])

    st.markdown("---")
    st.markdown("### Save Your Report as PDF")
    if st.button("🔗 Save as PDF") and st.session_state.get("response"):
        save_to_pdf(st.session_state.response)
        st.session_state.pdf_saved = True
        st.success("📄 PDF saved successfully!")

    if st.session_state.get("pdf_saved", False):
        with open("Company_Research_Report.pdf", "rb") as f:
            st.download_button(
                label="📥 Download Report",
                data=f,
                file_name="Company_Research_Report.pdf",
                mime="application/pdf"
            )


if __name__ == "__main__":
    main()
