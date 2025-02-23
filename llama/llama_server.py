import requests


class ChatOllama:
    def __init__(self, server_url, model="llama3.2", temperature=0):
        self.server_url = server_url
        self.model = model
        self.temperature = temperature

    def query(self, input_text):
        # Construct the payload for the POST request
        payload = {
            "model": self.model,
            "prompt": input_text,
            "temperature": self.temperature,
            "stream": False,
            # Add any other necessary parameters here
        }

        # Send the request to the server
        try:
            response = requests.post(self.server_url, json=payload)
            response.raise_for_status()  # This will raise an error for bad responses
            return response.json().get(
                "response", ""
            )  # Assuming 'response' is the key for the output text
        except requests.exceptions.RequestException as e:
            raise Exception(f"An error occurred when contacting the server: {e}")


# Set up the ChatOllama instance with the server URL
llama_model = ChatOllama(
    server_url="https://alert-fly-enabled.ngrok-free.app/api/generate"
)  # Replace '/endpoint' with the correct path

# Example usage
try:
    response_text = llama_model.query("Hello, how are you?")
    print(response_text)
except Exception as e:
    print(f"An error occurred: {e}")
