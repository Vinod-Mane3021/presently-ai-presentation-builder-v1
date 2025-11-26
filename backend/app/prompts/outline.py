SYSTEM_INSTRUCTION = "You are a helpful AI that generates outlines for presentations."

PROMPT_TEMPLATE = """
Create a coherent and relevant outline for the following prompt:

"{user_prompt}"

The outline should consist of at least 6 points, with each point written as a single sentence.
Ensure the outline is well-structured and directly related to the topic.

Return the output in the following JSON format:

{{
  "outlines": [
    "Point 1",
    "Point 2",
    "Point 3",
    "Point 4",
    "Point 5",
    "Point 6"
  ]
}}

Ensure that the JSON is valid and properly formatted. Do not include any other text or explanations outside the JSON.
""".strip()

