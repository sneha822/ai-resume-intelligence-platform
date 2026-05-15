#extracting email
import re
import PyPDF2
path = r'C:\Users\lenovo\Documents\GitHub\ai-resume-intelligence-platform\data\raw\Aryan_Mehta_AI_Resume.pdf'

with open(path, 'rb') as pdf_file:
    reader = PyPDF2.PdfReader(pdf_file)
    

    email_pattern = r'[a-zA-Z0-9+-_.%]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern=r'\+?\d{10,12}'


    for page in reader.pages:
        text = page.extract_text()
        if text:
            emails = re.findall(email_pattern, text)
            if emails: 
                print("email:", emails)
        
        #phone number
        if text:
            phone_number = re.findall(phone_pattern,text)
        if phone_number:
            print("phone:",phone_number)






