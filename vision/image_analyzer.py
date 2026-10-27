import base64

from core.llm import get_llm


def analyze_image(
    image_bytes: bytes,
    question: str = "Describe this image.",
) -> str:

    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": question,
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}"
                },
            },
        ],
    }

    response = get_llm().invoke([message])

    return response.text