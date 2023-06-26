import random
import string
import PyPDF2
from datetime import datetime
from os import system, path, stat

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

def get_file_size(sid):
    if path.exists(f"files/{sid}/{sid}.pdf"):
        file_size = stat(f"files/{sid}/{sid}.pdf")
        return file_size.st_size / (1024 * 1024)
    
class Check:
    def sid(sid, sql, action):
        # The folder exist but no data in database
        if action == "add":
            pages_num = get_pages_num(sid)
            sql.execute("SELECT * FROM books WHERE sid = %s", [sid])
            row = sql.fetchall()
            if pages_num == 0 or len(row) != 0:
                return False
            return True
        
        # There is data in database
        elif action == "edit":
            sql.execute("SELECT * FROM books WHERE sid = %s", [sid])
            if sql.fetchone():
                return True
            return  False

    def title(title):
        if title:
            return True
        return False

    def author(author):
        if author:
            return True
        return False

    def version(version):
        if version:
            return True
        return False

    def date(date):
        try:
            datetime.strptime(date, "%Y-%m-%d").timestamp()
        except:
            return False
        if datetime.strptime(date, "%Y-%m-%d").timestamp() > datetime.now().timestamp():
            return  False
        return True

    def lang(lang):
        if lang:
            return True
        return False

    def desc(desc):
        if desc:
            return True
        return False