from datetime import datetime

class CTime():
    def current_time():
        return datetime.now()
    
    def format_time(dueDate:dict,dueTime:dict)-> datetime:
        day = str(dueDate.get("day",0))
        month = str(dueDate.get("month",0))
        year = str(dueDate.get("year",0))
        hours = str(dueTime.get("hours",0))
        minutes = str(dueTime.get("minutes",0))
        format = "%d%m%Y%H%M"
        date_string = datetime.strptime(f"{day}{month}{year}{hours}{minutes}",format)

        return date_string



        