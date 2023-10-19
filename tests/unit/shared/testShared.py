import unittest
import time
from shared_resources.shared import Shared


class TestSahred(unittest.TestCase):
    def test_question(self): 
        question = "test"
        shared = Shared()
        id = shared.add_question(question)
        verify_id, verify_question = shared.queue[0]
        self.assertEqual(question, verify_question)
        self.assertEqual(id, verify_id)

        verify_id, verify_question = shared.get_question()
        self.assertEqual(question, verify_question)
        self.assertEqual(id, verify_id)

        obj = shared.get_question()
        self.assertEqual(None, obj)

    def test_query(self):
        # test variables
        user_prompt = "test"
        system_prompt = "system"
        
        # test
        shared = Shared()
        id = shared.add_query(user=user_prompt, system=system_prompt)
        stored_dict = shared.query_queue[0]
        self.assertEqual(user_prompt, stored_dict['user'])
        self.assertEqual(system_prompt, stored_dict['system'])
        self.assertEqual(id, stored_dict['id'])

        stored_dict = shared.get_query()
        self.assertEqual(user_prompt, stored_dict['user'])
        self.assertEqual(system_prompt, stored_dict['system'])
        self.assertEqual(id, stored_dict['id'])

        obj = shared.get_query()
        self.assertEqual(None, obj)

    def test_response(self):
        shared = Shared()
        id = shared.get_id(1)
        self.assertEqual(None, shared.responses[id])
        self.assertEqual({"status": "wait"}, shared.get_response(id))
        time.sleep(3)
        self.assertEqual({"status": "Unknown"}, shared.get_response(id))

        expected_response = "test"
        shared.update_response((id, expected_response), 1)
        self.assertEqual(
            {"status": "ok", "answer": expected_response}, shared.get_response(id))
        self.assertEqual({"status": "Unknown"}, shared.get_response(id))


if __name__ == '__main__':
    unittest.main()
