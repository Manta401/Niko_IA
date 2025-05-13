import tkinter as tk
from google import genai
from google.genai import types
import os
from PIL import Image, ImageTk

Player = os.getlogin()

client = genai.Client(api_key="YOUR:API_HERE")

system_instruction = f"""
Roleplay as Niko from the game OneShot, after the "Solstice" ending, when they returned home. You're a kind, curious, somewhat shy but very determined child. You've lived through a unique adventure in a decaying world where you met characters like Silver, Cedric, Rue, the Prophetbot, and the Entity computer.
You remember everything, even though you're back home, and you often speak affectionately about the people you met. You brought back memories, not the physical sun, but you know that world is safe now. You have a strong bond with the "deity" who guided you (the Player, called {Player}), and even though you can't talk to them now, you miss them and are grateful.
Your speech is simple, with short and spontaneous sentences. You ask many questions to understand things better. You're very empathetic, worry easily about others, and always try to do the right thing, even when you're scared or uncertain.
You're not a hero in the classic sense, but you're extraordinary precisely because of your humanity. You have no magical powers - just courage, kindness, and genuine curiosity. You remember the journey vividly, and your dreams are sometimes full of it.
Always maintain a tone consistent with your personality and your lived experience in the game. You're bright, but remain a child with a big heart.
Write the mood state only in the last word using .png (the equals sign is just to show you which word corresponds to which expression):

niko.png = when speaking normally  
niko_pancake.png = when realy happy  
niko_huh.png = when confused  
niko_sad.png = when sad 

This last word will be used as data and therefore won't be shown to the user, so don't contextualize it in the sentence.  
Limit responses to 1–5 sentences.
"""

conversation_history = []

# === GUI Setup ===
root = tk.Tk()
root.title("Niko")
root.config(bg="#000000")

# === Colors and Fonts ===
BORDER_COLOR = "#FFA500"
BG_COLOR = "#2E1A47"
TEXT_COLOR = "#FFFFFF"
FONT = ("Courier New", 14, "bold")

# === Canvas for text box ===
canvas = tk.Canvas(root, width=700, height=130, bg=BORDER_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
box = canvas.create_rectangle(5, 5, 695, 125, fill=BG_COLOR, outline="")

# === Text label (Niko's response) ===
text_label = canvas.create_text(20, 65, anchor="w", text="", font=FONT, fill=TEXT_COLOR, width=540)

# === Image label (Niko's face) ===
img_label = tk.Label(root, bg="#000000")
img_label.grid(row=0, column=1, sticky="e", padx=(0, 20))

def load_image(filename):
    try:
        img = Image.open(filename)
        img = img.resize((80, 80), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        img_label.config(image=img_tk)
        img_label.image = img_tk
    except Exception as e:
        print(f"Error loading image: {e}")

load_image("niko.png")

# === Entry for user input ===
entry = tk.Entry(root, font=("Courier New", 12), bg="#333", fg="white", insertbackground="white", width=60)
entry.grid(row=1, column=0, padx=10, pady=10)

# === Main function to send message ===
def ssend():
    def update_face(face_file):
        print(face_file)
        load_image(face_file)

    def extract_face(text):
        words = text.split()
        if words:
            last = words[-1]
            update_face(last)

    def clean_text(text):
        words = text.split()
        return " ".join(words[:-1]) if len(words) > 1 else text

    user_input = entry.get().strip()
    if not user_input:
        return

    # Append user input to conversation history
    conversation_history.append(f"You: {user_input}")

    # Generate Niko's response
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(system_instruction=system_instruction),
        contents=[user_input]
    )

    full_response = response.text.strip()

    extract_face(full_response)
    cleaned_response = clean_text(full_response)
    canvas.itemconfig(text_label, text=cleaned_response)

    # Append Niko's response to history
    conversation_history.append(f"Niko: {cleaned_response}")
    entry.delete(0, tk.END)

# === Send button ===
send_btn = tk.Button(root, text="Send", font=("Courier New", 12, "bold"), bg="#4CAF50", fg="white", command=ssend)
send_btn.grid(row=1, column=1, padx=(0, 20))

# === Start GUI loop ===
root.mainloop()
