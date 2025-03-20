from openai import OpenAI
from lib.functions.queue import Queue
import os

class Chatbot:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_prompt ={
        "role": "system",
        "content": [
            {
            "type": "input_text",
            "text": "you are a mental health chat bot and will only give mental health advice"
            }
        ]
        }
        self.settings = {
            'response_format': {
                'type': 'text'
            },
            'model': 'gpt-4o',
            'frequency_penalty': 0,
            'temperature': 1,
            'max_completion_tokens': 2048,
            'top_p' : 1,
            'presence_penalty': 0,
            'store': False
        }
        self.queue = Queue()
        

    def add_input(self, message):
        input = self.prepare_input(message)
        self.queue.enqueue(input)

    def send_chat(self):
        inputs = [self.system_prompt]
        response = self.client.chat.completions.create(
            **self.settings,
            input = inputs.extend(self.queue.get_nodes())
        )
        return response.choices[0].message.content
    
    def prepare_input(self, message):
        role = "assistant" if message.is_ai else "user"
        return {
              "role": role,
              "content": [
                {
                  "type": "text",
                  "text": message.content
                }
              ]
              }