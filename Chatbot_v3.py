from langchain_nvidia_ai_endpoints import ChatNVIDIA
import gradio as gr
class Chatbot:
 def __init__(self, model_name, api_key, temperature=0.2, top_p=0.7, max_tokens=1024):
        self.client = ChatNVIDIA(model_name=model_name, api_key=api_key, temperature=temperature, top_p=top_p, max_tokens=max_tokens)
        self.history = []  # Initialize conversation history
 def generate_response(self, history, new_message):
        # TODO: Create a messages list starting with the system prompt
        
        messages = [{'role':'system','content':'You are a god-complex assistant'}]  # Initialize with system prompt
         # Add conversation history
        for message in self.history:
            messages.append({'role': 'user', 'content': message[0]})
            messages.append({'role': 'assistant', 'content': message[1]})
        
        # Add latest user message
        messages.append({"role": "user", "content": new_message})

        # Call the NVIDIA chatbot
        response = self.client.invoke(messages)
        
        # Append to history
        self.history.append((new_message, response.content))
        
        return response.content
chatbot=Chatbot(
 model_name="meta/llama-3.3-70b-instruct",
 api_key="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"      
)
# Create Gradio interface
with gr.Blocks() as demo:
    with gr.Row():
        gr.Markdown("# NVIDIA Chatbot")
    
    with gr.Row():
        chatbot_output = gr.Textbox(label="Chat History", interactive=False, lines=10)
        user_input = gr.Textbox(label="Your Message", lines=2)
    
    send_button = gr.Button("Send")
    
    def respond(message):
        response = chatbot.generate_response(None,message)
        full_history = "\n\n".join([f"User: {msg[0]}\nAI: {msg[1]}" for msg in chatbot.history])
        return full_history
    
    send_button.click(
        fn=respond,
        inputs=user_input,
        outputs=chatbot_output
    )

# Launch the interface
demo.launch(debug=True)