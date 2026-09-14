from datetime import datetime
from gc_agent.custom_errors import GCRConnectionError, GCRServerError, GCRRateLimitError

import time

class CTime():
    @staticmethod
    def current_time():
        return datetime.now()

    @staticmethod
    def format_time(due_date_dict=None, due_time_dict=None):
        """
        Safely parses  Google Classroom due date and time dictionaries into a datetime object.
        Returns None if fields are missing or if the date values are invalid.
        """
        if not due_date_dict or not isinstance(due_date_dict, dict):
            return None
            
        year = due_date_dict.get("year")
        month = due_date_dict.get("month")
        day = due_date_dict.get("day")
        
        # If any core date part is missing, there's no valid deadline
        if not year or not month or not day:
            return None

        # Default to midnight if dueTime is missing or empty
        hours = 0
        minutes = 0
        if due_time_dict and isinstance(due_time_dict, dict):
            hours = due_time_dict.get("hours", 0) or 0
            minutes = due_time_dict.get("minutes", 0) or 0

        try:
            # Construct datetime safely using integers to avoid string-gluing bugs
            return datetime(
                year=int(year), 
                month=int(month), 
                day=int(day), 
                hour=int(hours), 
                minute=int(minutes)
            )
        except ValueError as e:
            # Gracefully handle any unexpected calendar discrepancies
            return None




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


