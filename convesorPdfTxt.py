# from ctypes import string_at
import fitz

fname = "Provas/portugues.pdf"  # get document filename
doc = fitz.open(fname)  # open document
out = open(fname[:-4] + ".txt", "wb")  # open text output
for page in doc:  # iterate the document pages
    text = page.get_text().encode("utf8")  # get plain text (is in UTF-8)
    out.write(text)  # write text of page
    out.write(bytes((12,)))  # write page delimiter (form feed 0x0C)
doc.close()
out.close()
