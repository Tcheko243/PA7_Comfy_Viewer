import webbrowser
import os
import cv2
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo

class PA7_Comfy_Viewer:
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "view_image"
    CATEGORY = "PA7"

    # Créez le dossier temporaire dans le même répertoire que ce fichier Python
    script_dir = os.path.dirname(__file__)
    temp_dir = os.path.join(script_dir, "temp")

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    image_path = os.path.join(temp_dir, "output_image.png")
    info_path = os.path.join(temp_dir, "image_info.txt")
    viewer_url = None  # Stocker l'URL du visualiseur

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",)
            }
        }

    def extract_metadata(self, image_path):
        # Ouvrir l'image pour extraire les métadonnées
        with Image.open(image_path) as img:
            metadata = img.info

        # Extraire les informations pertinentes des métadonnées
        prompt = metadata.get("prompt", "N/A")
        width = metadata.get("width", "N/A")
        height = metadata.get("height", "N/A")
        sampler = metadata.get("sampler", "N/A")

        # Enregistrer les informations des métadonnées dans un fichier texte
        with open(self.info_path, "w") as info_file:
            info_file.write(f"Prompt: {prompt}\n")
            info_file.write(f"Width: {width}px\n")
            info_file.write(f"Height: {height}px\n")
            info_file.write(f"Sampler: {sampler}\n")

    def view_image(self, image):
        # Convertir l'image en tableau numpy et vérifier les dimensions
        image_array = np.array(image)

        # Vérifier les dimensions de l'image
        print(f"Image original shape: {image_array.shape}")

        # Si l'image a 4 dimensions, supprimer la première dimension
        if len(image_array.shape) == 4 and image_array.shape[0] == 1:
            image_array = np.squeeze(image_array, axis=0)
            print(f"Squeezed image shape: {image_array.shape}")

        # Vérifier les dimensions de l'image
        if len(image_array.shape) == 3:
            height, width, channels = image_array.shape
            print(f"Image dimensions: {width}x{height}, Channels: {channels}")
        elif len(image_array.shape) == 2:
            height, width = image_array.shape
            print(f"Image dimensions: {width}x{height}, Grayscale")
        else:
            print("Unsupported image shape:", image_array.shape)
            return (image,)

        if width > 10000 or height > 10000:
            print(f"Image dimensions exceed limit: {width}x{height}")
            return (image,)

        # Convertir l'image en format BGR pour cv2 si elle est en RGB
        if channels == 3:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        # Convertir les valeurs des pixels en entiers appropriés
        image_array = np.clip(image_array * 255, 0, 255).astype(np.uint8)

        # Afficher quelques valeurs de pixels pour déboguer
        print("Pixel values at (0, 0):", image_array[0, 0])

        success = cv2.imwrite(self.image_path, image_array)
        if not success:
            print(f"Failed to write image to {self.image_path}")
            return (image,)

        print(f"Image successfully written to {self.image_path}")

        # Extraire les métadonnées et les enregistrer dans un fichier
        self.extract_metadata(self.image_path)

        # Ouvrir le visualiseur HTML (une seule fois)
        viewer_path = os.path.join(os.path.dirname(__file__), "viewer.html")
        viewer_url = f"file://{viewer_path}"

        if PA7_Comfy_Viewer.viewer_url != viewer_url:
            webbrowser.open(viewer_url)
            PA7_Comfy_Viewer.viewer_url = viewer_url

        # Retourner l'image au prochain nœud du pipeline
        return (image,)

NODE_CLASS_MAPPINGS = {
    "PA7_Comfy_Viewer": PA7_Comfy_Viewer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PA7_Comfy_Viewer": "PA7 Comfy Viewer"
}
