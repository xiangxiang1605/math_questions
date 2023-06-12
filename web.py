from flask import Flask, render_template, request, send_file
from io import BytesIO
from app import generate_questions, generate_pdf

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    num_questions = int(request.form['num_questions'])
    max_number = int(request.form['max_number'])
    page_number = int(request.form.get('page_number') if request.form.get('page_number') else '10')
    pages = []
    for _ in range(0, page_number):
        questions = generate_questions(num_questions, max_number)
        pages.append(questions)
    # Generate PDF
    pdf_bytes = BytesIO()
    generate_pdf(pages,pdf_bytes)
    # Return the generated PDF as a file for download
    pdf_bytes.seek(0)
    return send_file(pdf_bytes, download_name='questions.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run()
