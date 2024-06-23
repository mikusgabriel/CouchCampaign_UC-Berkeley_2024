from PIL import Image
import io
import base64


def image_to_string(image_path):
    try:
        # Open the image file
        with Image.open(image_path) as img:
            # Convert image to RGB mode if it's not already in RGB
            img = img.convert("RGB")

            # Convert image to byte array
            img_bytes = io.BytesIO()
            img.save(
                img_bytes, format="PNG"
            )  # Change format as needed (PNG, JPEG, etc.)
            img_bytes.seek(0)

            # Encode byte array to base64 string
            img_str = base64.b64encode(img_bytes.read()).decode("utf-8")

            return img_str
    except IOError as e:
        print(f"Error converting image to string: {e}")
        return None


