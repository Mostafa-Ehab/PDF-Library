import random
import string
import PyPDF2
from os import system, path

# Define a function
def generate_sid(length=16):
    # Define all possible characters
    characters = string.ascii_letters + string.digits
    # Create random string
    random_string = ''.join(random.choice(characters) for _ in range(length))
    # Set the return value to the generated string
    return random_string

def is_admin(session):
    if session.get("user_id"):
        if session["is_admin"]:
            return True
    
    return False

def pdf_convert(sid):
    num = get_pages_num(sid)
    for i in range(num):
        print("Converting")
        system(
            f'inkscape "files/{sid}/{sid}.pdf" --pdf-page={i+1} --export-type="svg" -o "files/{sid}/{i+1}.svg"')
        
def get_pages_num(sid):
    if path.exists(f"files/{sid}/{sid}.pdf"):
        file = open(f"files/{sid}/{sid}.pdf", 'rb')
        try:
            reader = PyPDF2.PdfReader(file)
            num = len(reader.pages)
            return num
        except:
            return 0
    return 0
