from py4j.java_gateway import JavaGateway

gateway = JavaGateway()
pdf_box_utils = gateway.jvm.PdfBoxUtils()


text = pdf_box_utils.extractText('data/2036582_lu.pdf')
print(text)

