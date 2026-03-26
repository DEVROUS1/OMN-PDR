from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
import os

def create_schedule_image(template_bytes, data_dict):
    """
    template_bytes: bytes of the uploaded image
    data_dict: {"Tarih": "...", "Pazartesi": "...", "Salı": "..."}
    Returns: BytesIO containing the output PNG.
    """
    img = Image.open(io.BytesIO(template_bytes)).convert("RGB")
    draw = ImageDraw.Draw(img)
    w, h = img.size
    
    # Try finding a TTF
    try:
        if os.name == 'nt':
            font_path = "C:\\Windows\\Fonts\\arial.ttf"
            font_bold_path = "C:\\Windows\\Fonts\\arialbd.ttf"
        else:
            font_path = "arial.ttf"
            font_bold_path = "arialbd.ttf"
            
        font = ImageFont.truetype(font_path, int(w * 0.015))  # roughly 15px if width=1000
        font_header = ImageFont.truetype(font_bold_path, int(w * 0.022))
    except Exception:
        font = ImageFont.load_default()
        font_header = ImageFont.load_default()

    # Image Sections (Relative coordinates)
    # Row 1 (Top) offsets
    top_y_start = h * 0.16
    bottom_y_start = h * 0.55
    
    # x_left, y_top, x_right, y_bottom
    boxes = {
        "Pazartesi": (w * 0.025, top_y_start, w * 0.24, h * 0.52),
        "Salı": (w * 0.275, top_y_start, w * 0.49, h * 0.52),
        "Çarşamba": (w * 0.525, top_y_start, w * 0.73, h * 0.52),
        "Perşembe": (w * 0.765, top_y_start, w * 0.97, h * 0.52),
        
        "Cuma": (w * 0.025, bottom_y_start, w * 0.24, h * 0.98),
        "Cumartesi": (w * 0.275, bottom_y_start, w * 0.49, h * 0.98),
        "Pazar": (w * 0.525, bottom_y_start, w * 0.73, h * 0.98),
    }

    # Fill content
    padding_x = 5  # Left padding inside the box
    for gun, bbox in boxes.items():
        text = data_dict.get(gun, "").strip()
        if text:
            maxWidth = (bbox[2] - bbox[0]) - (padding_x * 2)
            
            # Simple text wrap logic
            y_offset = bbox[1]
            for para in text.split("\n"):
                if not para.strip():
                    y_offset += 10
                    continue
                
                words = para.split(' ')
                current_line = ""
                for word in words:
                    test_line = (current_line + " " + word).strip()
                    # bbox: (left, top, right, bottom)
                    text_bbox = draw.textbbox((0, 0), test_line, font=font)
                    if (text_bbox[2] - text_bbox[0]) <= maxWidth:
                        current_line = test_line
                    else:
                        draw.text((bbox[0] + padding_x, y_offset), current_line, fill=(30, 30, 30), font=font)
                        y_offset += (text_bbox[3] - text_bbox[1]) + 4
                        current_line = word
                
                if current_line:
                    draw.text((bbox[0] + padding_x, y_offset), current_line, fill=(30, 30, 30), font=font)
                    text_bbox = draw.textbbox((0, 0), current_line, font=font)
                    y_offset += (text_bbox[3] - text_bbox[1]) + 8

    # Tarih Field
    tarih_val = data_dict.get("Tarih", "")
    if tarih_val:
        draw.text((w * 0.82, h * 0.04), tarih_val, fill=(0, 0, 0), font=font_header)

    out_bytes = io.BytesIO()
    img.save(out_bytes, format="PNG")
    out_bytes.seek(0)
    return out_bytes
