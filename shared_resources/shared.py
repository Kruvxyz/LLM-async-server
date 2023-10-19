from typing import Dict, List, Tuple, Optional
import string
import random
from singleton_decorator import singleton
import threading
import time


@singleton
class Shared:
    def __init__(self, num_digits: int = 12) -> None:
        self.queue: List[Tuple[str, str]] = [] #fixme: cleanup with related question functions
        self.query_queue: List[Dict[str, str]] = []
        self.responses: Dict[str, Optional[str]] = {}
        self.num_digits = num_digits

    def get_id(self, schedule_sec: int = 60*60*24) -> str:
        while True:
            new_id = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=self.num_digits))
            if new_id not in self.responses:
                self.update_response((new_id, None), schedule_sec=schedule_sec)
                return new_id

    def get_question(self) -> Optional[Tuple[str, str]]:
        if len(self.queue) == 0:
            return None
        next_question = self.queue.pop(0)
        return next_question

    def get_query(self) -> Optional[Dict[str, str]]:
        if len(self.query_queue) == 0:
            return None
        next_query = self.query_queue.pop(0)
        if not type(next_query) is dict:
            raise TypeError("Must query with dict Dict[str, str]")
        return next_query

    def _add_query(self, new_query: Dict[str, str]) -> bool:
        self.query_queue.append(new_query)
        return True
        
    def _add_question(self, new_question: Tuple[str, str]) -> bool:
        self.queue.append(new_question)
        return True

    def add_query(self, user: str, system: str, history: List[Dict[str, str]] = None) -> Optional[str]:
        #fixme: history currently disable
        id = self.get_id()
        query = {'id': id, 'system': system, 'user': user}
        if self._add_query(query):
            return id
        else:
            return None
        
    def add_question(self, question: str) -> Optional[str]:
        id = self.get_id()
        if self._add_question((id, question)):
            return id
        else:
            return None

    def update_response(self, object: Tuple[str, Optional[str]], schedule_sec: int) -> bool:
        id, response = object
        self.responses[id] = response
        self.future_cleanup(id, schedule_sec)
        return True

    def remove_response(self, id: str, schedule_sec: Optional[int] = None) -> None:
        if schedule_sec:
            time.sleep(schedule_sec)
        try:  # fixme: quick and dirty solution, memory managment should be done better
            self.responses.pop(id)
        except:
            pass

    def get_response(self, id: str) -> Dict[str, str]:
        try:
            response = self.responses[id]
        except KeyError:
            return {"status": "Unknown"}

        response_json = {"status": "wait"}
        if response:
            response_json["status"] = "ok"
            response_json["answer"] = response
            self.remove_response(id)

        return response_json

    def future_cleanup(self, id: str, schedule_sec: int = 60*60*24*2) -> None:
        scheduled_remvoe_response = threading.Thread(
            target=self.remove_response, args=(id, schedule_sec))
        scheduled_remvoe_response.start()


shared = Shared()
