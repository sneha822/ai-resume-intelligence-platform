import string 


def to_lower_case(text):
    if not isinstance(text,str):
        raise TypeError("text must be string")
    return text.lower()




def remove_punctuations(text):
    if not isinstance(text,str):
        raise TypeError("text must be string")
    return text.translate(str.maketrans('','',string.punctuation))





def clean_whitespace(text):
    if not isinstance(text,str):
        raise TypeError("text must be string")
    return " ".join(text.split())

s="HHHHHHHHHHHH,,,,    krish"
print(to_lower_case(s))
    