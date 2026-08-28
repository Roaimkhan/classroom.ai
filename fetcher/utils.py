from datetime import datetime
from gc_agent.custom_errors import GCRConnectionError, GCRServerError, GCRRateLimitError

import fitz
import time

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

def retry_decorator(retry_range=3):
    def decorator(func):
        def wrapper(*args,**kwargs):            
                exponential_factor = 1
                for attempt in range(retry_range):
                    try:
                        return func(*args,**kwargs)
                    except (GCRConnectionError, GCRServerError) as e:
                        if attempt == (retry_range - 1):
                            raise e
                        time.sleep(5)
                        print(f"Retry attempt {attempt+1} failed")
                      
                    except (GCRRateLimitError) as e:
                        if attempt == (retry_range - 1):
                            raise e
                        time.sleep(5*exponential_factor)
                        exponential_factor += 1
                        print(f"Retry attempt {attempt+1} failed")

        return wrapper
    return decorator


