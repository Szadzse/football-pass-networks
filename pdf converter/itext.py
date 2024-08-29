# Importáljuk az iText Java osztályokat
from com.itextpdf.text.pdf import PdfWriter, Document, Paragraph
 
# Létrehozunk egy új PDF dokumentumot
document = Document()
 
# Megnyitjuk a dokumentumot a kiírásra
output = FileOutputStream("hello.pdf")
document.open()
 
# Hozzáadunk egy bekezdést a dokumentumhoz
document.add(Paragraph("Hello, World!"))
 
# Bezárjuk a dokumentumot
document.close()
output.close()
