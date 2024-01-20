from openai import OpenAI
import json
import time

openai_api_key = "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"

# Assume you have a text file named "transcript.txt" where the transcript is stored
with open("transcript.txt", "r") as text_file:
    text = text_file.read()

with open("data.json", "r") as json_file:
    data = json.load(json_file)

client = OpenAI(api_key=openai_api_key)

def assist():
    stri = ""
    assistant = client.beta.assistants.retrieve(assistant_id="asst_p48BVZEr6mMunzy2Axiebhqh")
    thread = client.beta.threads.create()

    # Add a Message to a Thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="facial expression data : " + json.dumps(data) + " speech to text : " + text 
        )

    # Run the Assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions=assistant.instructions
    )

    while True:
        # Wait for 5 seconds
        time.sleep(5)

        # Retrieve the run status
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        # If run is completed, get messages
        if run_status.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )

            # Loop through messages and print content based on role
            for msg in messages.data:
                role = msg.role
                content = msg.content[0].text.value

                if role == 'assistant':
                    # Only append assistant's response
                    stri += content
                    print(stri)
                return stri

if __name__ == "__main__":
    assist()
