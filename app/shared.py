from typing import Dict, List, Tuple, Optional
import string
import random
from singleton_decorator import singleton


@singleton
class Shared:
    def __init__(self, num_digits: int = 12) -> None:
        self.queue: List[Tuple[str, str]] = []
        self.responses: Dict[str, Optional[str]] = {}
        self.num_digits = num_digits

    def get_id(self) -> str:
        while True:
            new_id = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=self.num_digits))
            if new_id not in self.responses:
                self.responses[new_id] = None
                return new_id

    def get_question(self) -> Optional[Tuple[str, str]]:
        if len(self.queue) == 0:
            return None
        next_question = self.queue[0]
        self.queue = self.queue[1:]
        return next_question

    def _add_question(self, new_question: Tuple[str, str]) -> bool:
        self.queue.append(new_question)
        return True

    def add_question(self, question: str) -> Optional[str]:
        id = self.get_id()
        if self._add_question((id, question)):
            return id
        else:
            return None

    def update_response(self, object: Tuple[str, Optional[str]]) -> bool:
        id, response = object
        self.responses[id] = response
        return True

    def get_response(self, id: str) -> Dict[str, str]:
        try:
            response = self.responses[id]
        except KeyError:
            return {"status": "Unknown"}

        response_json = {"status": "wait"}
        if response:
            response_json["status"] = "ok"
            response_json["answer"] = response
            self.responses.pop(id)

        return response_json


shared = Shared()
