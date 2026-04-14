from datetime import datetime
import fitz

class CTime():
    @staticmethod
    def current_time():
        return datetime.now()
        
    @staticmethod
    def format_time(dueDate:dict,dueTime:dict)-> datetime:
        day = str(dueDate.get("day",0))
        month = str(dueDate.get("month",0))
        year = str(dueDate.get("year",0))
        hours = str(dueTime.get("hours",0))
        minutes = str(dueTime.get("minutes",0))
        format = "%d%m%Y%H%M"

        if len(month)<2:
            tmp_month = month
            month="0"
            month+=tmp_month
        
        date_string = datetime.strptime(f"{day}{month}{year}{hours}{minutes}",format)

        return date_string


def pdf_bytes_to_text(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""
    for page in doc:
        text += page.get_text()
    
    return text