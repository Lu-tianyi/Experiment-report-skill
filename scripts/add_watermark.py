import fitz
import sys
import os
from PIL import Image
import io


def add_watermark(input_pdf: str, watermark_image: str, output_pdf: str, opacity: float = 0.25, scale: float = 0.4):
    if not os.path.exists(input_pdf):
        print(f"Error: Input PDF not found: {input_pdf}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(watermark_image):
        print(f"Error: Watermark image not found: {watermark_image}", file=sys.stderr)
        sys.exit(1)

    pil_img = Image.open(watermark_image).convert("RGBA")
    r, g, b, a = pil_img.split()
    a = a.point(lambda x: int(x * opacity))
    pil_img = Image.merge("RGBA", (r, g, b, a))

    img_bytes = io.BytesIO()
    pil_img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    doc = fitz.open(input_pdf)

    for page_num in range(len(doc)):
        page = doc[page_num]
        rect = page.rect

        wm_width = rect.width * scale
        wm_height = wm_width * pil_img.height / pil_img.width

        wm_rect = fitz.Rect(
            (rect.width - wm_width) / 2,
            (rect.height - wm_height) / 2,
            (rect.width + wm_width) / 2,
            (rect.height + wm_height) / 2,
        )

        page.insert_image(wm_rect, stream=img_bytes.getvalue(), overlay=True, keep_proportion=True)

    doc.save(output_pdf, garbage=4, deflate=True, clean=True)
    doc.close()
    print(f"Watermarked PDF saved to: {output_pdf}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python add_watermark.py <input_pdf> <watermark_image> [output_pdf] [opacity]", file=sys.stderr)
        sys.exit(1)

    input_pdf = sys.argv[1]
    watermark_image = sys.argv[2]
    output_pdf = sys.argv[3] if len(sys.argv) > 3 else input_pdf.replace(".pdf", "_watermarked.pdf")
    opacity = float(sys.argv[4]) if len(sys.argv) > 4 else 0.25

    add_watermark(input_pdf, watermark_image, output_pdf, opacity)
