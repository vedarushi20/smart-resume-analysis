from fpdf import FPDF

def generate_report(name, email, matched, missing, score, all_skills):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Smart Resume Analysis Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
    pdf.cell(200, 10, txt=f"Match Score: {score}%", ln=True)
    pdf.ln(5)

    pdf.multi_cell(0, 10, txt=f"Extracted Skills: {', '.join(all_skills)}")
    pdf.multi_cell(0, 10, txt=f"Matched Keywords: {', '.join(matched)}")
    pdf.multi_cell(0, 10, txt=f"Missing Keywords: {', '.join(missing)}")

    file_path = f"{name}_report.pdf"
    pdf.output(file_path)
    return file_path
