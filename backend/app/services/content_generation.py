from google import genai
from app.settings import settings
from app.prompts.outline import PROMPT_TEMPLATE, SYSTEM_INSTRUCTION 
import json
import logging
import base64
import httpx
from fastapi.responses import FileResponse 
import os
from schemas.content_generation import GeneratePresentationRequest

client = genai.Client(api_key=settings.GEMINI_API_KEY)

logger = logging.getLogger("app")

class OutlineClass:
    @staticmethod
    def generate_outline(user_prompt: str):

        final_prompt = PROMPT_TEMPLATE.format(user_prompt=user_prompt.strip())

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",  # or gemini-2.5-flash
                
                contents=[
                    {
                        "role": "user",
                        "parts": [{"text": final_prompt}],
                    },
                ],
                config={
                    "system_instruction": SYSTEM_INSTRUCTION,
                    "temperature": 0.0,
                    "max_output_tokens": 1024,
                    "response_mime_type": "application/json",
                },
            )

            # Access the text content and parse it as JSON
            try:
                outline_data = json.loads(response.text)
                logger.info("Outline generation successful")
                return outline_data
            except json.JSONDecodeError as json_err:
                logger.error(f"JSON decoding error: {json_err}")
                raise ValueError(f"Failed to parse JSON: {json_err}\nResponse Text: {response.text}")
        except Exception as e:
            logger.error(f"Error during API call: {e}")
            raise e

    @staticmethod
    def generate_image(prompt: str):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=[
                    {
                        "role": "user",
                        "parts": [{"text": prompt}]
                    }
                ],
                config={
                    "response_modalities": ["TEXT", "IMAGE"],
                    "response_mime_type": "application/json",
                    "temperature": 0.7, # Creativity level
                }
            )
            logger.info("Image generation successful")
            image_part = response.candidates[0].content.parts[0].inline_data
            return image_part
        except Exception as e:
            logger.error(f"Error during image generation: {e}")
            raise e

    @staticmethod
    async def generate_image_with_cloudfare_worker(prompt: str):
        try:
            endpoint = "https://text-to-image-template.manev7780.workers.dev"
            api_key = settings.CLOUDFLARE_API_TOKEN
            headers = {
                "Content-Type": "application/json",
                "x-api-key": api_key 
            }
            json = {
                "prompt": prompt
            }

            logger.info("Cloudflare Worker image generation started")

            async with httpx.AsyncClient(timeout=60.0) as client:
                try:
                    response = await client.post(
                        endpoint,
                        headers=headers,
                        json=json
                    )
                    response.raise_for_status()

                    # The Worker returns the raw binary image data (PNG)
                    if response.content:
                        logger.info("Cloudflare Worker image generation successful")
                        return response.content
                    else:
                        logger.error("Cloudflare Worker returned an empty response.")
                        raise ValueError("Cloudflare Worker returned an empty response.")
                    
                except httpx.HTTPStatusError as e:
                    # Log and raise a specific error for API issues
                    error_detail = response.text or "Unknown API Error"
                    logger.error(f"Worker API Error ({e.response.status_code}): {error_detail}")
                    raise ValueError(f"Image generation failed: {error_detail}")
                
                except Exception as e:
                    logger.error(f"Error during Cloudflare Worker call: {e}")
                    raise e


        except Exception as e:
            logger.error(f"Error saving image: {e}")
            raise e

    @staticmethod
    async def generate_image_and_save(prompt: str, file_path: str):
        try:
            image_bytes = await OutlineClass.generate_image_with_cloudfare_worker(prompt)
            
            if image_bytes:
                with open(file_path, "wb") as img_file:
                    img_file.write(image_bytes)
                logger.info(f"Image saved successfully at {file_path}")
                return file_path
            else:
                logger.error("No image data found in the response.")
                raise ValueError("No image data found in the response.")
        except Exception as e:
            logger.error(f"Error saving image: {e}")
            raise e

    @staticmethod
    def get_generated_image(image_name: str):
        try:
            if "/" in image_name or ".." in image_name:
                raise ValueError("Invalid image name")
            
            file_path = f"generated_images/{image_name}"

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"{file_path} does not exist")
        
            return FileResponse(file_path)
        
        except Exception as e:
            logger.error(f"Error getting generated image: {e}")
            raise e

    @staticmethod
    def generate_presentation(request: GeneratePresentationRequest):
        pass