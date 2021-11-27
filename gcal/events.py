import datetime
from typing import List

class Event:
    def __init__(self, start:datetime.datetime, end:datetime.datetime, title:str, description:str):
        self.start = start
        self.end = end
        self.title = title
        self.description = description

class Events:
    def __init__(self, start:datetime, end:datetime):
        self.events = []
        self.dates = []
        self.add_dates(start, end)
    
    def add_dates(self, start:datetime, end:datetime):
        start_date = datetime.date(start.year, start.month, start.day)
        end_date = datetime.date(end.year, end.month, end.day)
        date_delta = end_date - start_date
        for i in range(date_delta.days + 1):
            day = start_date + datetime.timedelta(days = i)
            friendly_date = self.get_day_from_dt(day)
            self.dates.append(friendly_date)

    def add_event(self, start:datetime, end:datetime, title:str, description:str):
        event = Event(start=start, end=end, title=title, description=description)
        self.events.append(event)

    def get_day_from_dt(self, dt:datetime) -> str:
        return dt.strftime("%-d %b %Y")

    def find_events_by_day(self, friendly_date:str) -> List[Event]:
        return_events = []
        for event in self.events:
            if self.get_day_from_dt(event.start) == friendly_date:
                return_events.append(event)

        return return_events
