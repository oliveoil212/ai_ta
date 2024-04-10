# from openai import OpenAI
import os
# from dotenv import load_dotenv
# from dotenv import find_dotenv, load_dotenv
import time
import logging

class GPT():
    def __init__(self,client,assistant):
        self.client = client
        self.assistant = assistant
        self.thread = None
        self.latest_run = None
    def new_thread(self):
        self.thread = self.client.beta.threads.create()
    def prompt_and_run(self, message):
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id, role="user", content=message
        )

        # === Run our Assistant ===
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            # instructions="Please address the user as James Bond",
        )
        self.latest_run = run

    def get_last_response(self,verbose=False):
        thread_id = self.thread.id
        run_id = self.latest_run.id
        while True:
            try:
                run = self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
                if run.completed_at:
                    if verbose:
                        elapsed_time = run.completed_at - run.created_at
                        formatted_elapsed_time = time.strftime(
                        "%H:%M:%S", time.gmtime(elapsed_time)
                        )
                        print(f"Run completed in {formatted_elapsed_time}")
                        logging.info(f"Run completed in {formatted_elapsed_time}")
                        # Get messages here once Run is completed!          
                    messages = self.client.beta.threads.messages.list(thread_id=thread_id)
                    last_message = messages.data[0]
                    response = last_message.content[0].text.value
                    return response
                    print(f"Assistant Response: {response}")
                    break
            except Exception as e:
                logging.error(f"An error occurred while retrieving the run: {e}")
                break
            logging.info("Waiting for run to complete...")
            time.sleep(3)


    
