# PPT Handout Converter
## What is it for?
Sometimes we are faced with such PPT handouts that has both slides and notes of the author, and the notes are not always on every page. As a result, if we want to read the handout (e.g. reviewing these slides for examination), we have to scroll over a lot of blank pages. Or if we want to print these handouts one slide in a page, a lot of paper will be wasted, if print four slides in a page, the font is too small to read.

![Drag Racing](./img/demo.png)

This script is to help convert these kind of PPT handouts  into a 4-in-1 document, with empty notes being ignored.  Thus the document can be more convenient for reading and eco-friendly for printing.
## How can I use it?
### Install the dependencies
To run the code, the following modules must be installed to your python environment.
```
pip install opencv-python pdf2image numpy Pillow
```
### Run the code
Create a folder named `pdf_in` in the same folder of the `Converter.py` script. Then simply run the script in its  directory. The output documents will be saved in the same folder.

### Tweak the parameters
For the current version, some parameters can only be modified in the script:
```
crop_up = 200
crop_down = 200
out_page_height = 3883
out_page_width = 5597
pdf_dir = "./pdf_in"
```
The `crop_up` and `crop_down` is the height in pixels to be cropped from the upper/lower side of the document, in case that the header/footer of the handout are marked as content to be merged into the output file. The `out_page_height` and `out_page_width` are the bitmap height and width of the output document. The `pdf_dir` is where the documents to be converted are stored.

## About the code
Currently this code is written in the exam period to save paper when printing the course slides for an open-book exam. There may exist many bugs and the coding style is bad. May improve in the future in my free time.