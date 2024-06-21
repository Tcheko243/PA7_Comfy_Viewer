# PA7 Comfy Viewer

## Description

The `PA7_Comfy_Viewer` node is used to display an image generated in an HTML visualization window and show associated metadata, like the prompt, image size, and the sampler used.

## Installation

1. Put the `PA7_Comfy_Viewer.py` file in the `custom_nodes` folder of ComfyUI.
2. Put the `viewer.html` file in the same directory as `PA7_Comfy_Viewer.py`.

## Usage

1. Add the `PA7_Comfy_Viewer` node to your ComfyUI pipeline.
2. Connect a generated image as input to this node.
3. When the node is executed, an HTML visualization window will automatically open to display the image and associated metadata. If a `ComfyViewer` window is already open, it will be reused.
4. The visualization window automatically refreshes every second to display the latest image and updated metadata.

## Notes

- The node creates a temporary `temp` folder in the same directory as `PA7_Comfy_Viewer.py` to store the image and metadata.
- Make sure that file permissions allow creation and writing in this folder.
- Image dimensions are limited to 10000x10000 pixels to prevent processing errors.
