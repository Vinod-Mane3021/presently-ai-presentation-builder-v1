from app.services.content_generation import OutlineClass
from fastapi import APIRouter, status, Request
from fastapi.responses import FileResponse, JSONResponse
import logging

router = APIRouter(
    prefix="/generate",
    tags=["content-generation"],
)

logger = logging.getLogger("app")

@router.post("/outlines", response_model=dict, status_code=status.HTTP_200_OK)
def generate_outline(user_prompt: str):
    try:
        outline_response = OutlineClass.generate_outline(user_prompt)
        return {"outline": outline_response}
    except Exception as e:
        return {"error": str(e)}
    

# @router.get("/image", response_model=dict, status_code=status.HTTP_200_OK)
# async def generate_image(user_prompt: str):
#     return await OutlineClass.generate_image_and_save(user_prompt, "generated_images/image.jpg")
#     return {"message": "Image generation endpoint - to be implemented"}

@router.post("/image", response_model=dict)
async def generate_image(user_prompt: str, request: Request):
    file_path = await OutlineClass.generate_image_and_save(user_prompt, "generated_images/image.jpg")
    file_url = str(request.base_url) + file_path
    return {
        "file_path": file_path,
        "file_url": file_url
    }

@router.get("/get-generated-image")
async def get_generated_image(image_name: str):
    try:
        return OutlineClass.get_generated_image(image_name)
    except FileNotFoundError:
        return JSONResponse(
            status_code=404,
            content={"error": f"Image '{image_name}' not found"}
        )

    except Exception as e:
        logger.error(f"Error fetching image: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "An unexpected error occurred while fetching the image"}
        )
    