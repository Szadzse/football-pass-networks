import PyPDF2
import sys 

# PDF fájl megnyitása és betöltése
with open('data/2036582_lu.pdf', 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)

    with open('data/pypdf2/lu.txt', 'w', encoding='utf-8') as f:
        #sys.stdout = f # Change the standard output to the file we created.
        for page in range(len(pdf_reader.pages)):
            print(pdf_reader.pages[page].extract_text(), file=f)
        #sys.stdout = original_stdout # Reset the standard output to its original value