import os
import base64
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def extract_info_from_card(image_path):
    base64_image = encode_image(image_path)

    prompt = """
    You are an information extraction system.

    Extract ONLY the following fields from the visiting card:
    - company
    - contact_person
    - email
    - phone

    Rules:
    - Return STRICT JSON only
    - If a field is missing, return null
    - No extra text, no explanation

    Example output:
    {
        "company": "ABC Pvt Ltd",
        "contact_person": "John Doe",
        "email": "john@abc.com",
        "phone": "+91-9876543210"
    }
    """

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        temperature=0,
        max_tokens=300,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    image_path = "D:\SOHAM\DandV\lead management system\WhatsApp Image 2026-04-18 at 4.02.18 PM.jpeg"  # replace with your image

    result = extract_info_from_card(image_path)
    print("Extracted Data:\n", result)