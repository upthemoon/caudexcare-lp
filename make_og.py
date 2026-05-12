"""OG画像（1200x630）を作成。Twitter/Facebookシェア時に表示される。"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
GREEN_DEEP = (46, 93, 58)
GREEN_DARK = (30, 65, 40)
GREEN_BRIGHT = (111, 184, 124)
WHITE = (255, 255, 255)
SUB = (200, 220, 200)

img = Image.new("RGB", (W, H), GREEN_DEEP)
draw = ImageDraw.Draw(img)

for y in range(H):
    t = y / H
    r = int(GREEN_DEEP[0] * (1 - t) + GREEN_DARK[0] * t)
    g = int(GREEN_DEEP[1] * (1 - t) + GREEN_DARK[1] * t)
    b = int(GREEN_DEEP[2] * (1 - t) + GREEN_DARK[2] * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

def find_font(size):
    candidates = [
        "/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
        "/Library/Fonts/tokoshieIPAGothic.ttf",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
    ]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except Exception:
            continue
    return ImageFont.load_default()

f_brand = find_font(36)
f_title = find_font(72)
f_sub = find_font(32)
f_meta = find_font(26)

LEFT_X = 60
try:
    icon = Image.open("/Users/sherlockholmes/caudexcare-lp/icon-256.png").convert("RGBA")
    icon = icon.resize((90, 90), Image.LANCZOS)
    mask = Image.new("L", (90, 90), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (90, 90)], radius=20, fill=255)
    img.paste(icon, (LEFT_X, 65), mask)
except Exception as e:
    print("icon paste failed:", e)
draw.text((LEFT_X + 110, 80), "CaudexCare", fill=WHITE, font=f_brand)

draw.text((LEFT_X, 200), "水やりタイミング、", fill=WHITE, font=f_title)
draw.text((LEFT_X, 290), "もう忘れない。", fill=GREEN_BRIGHT, font=f_title)

draw.text((LEFT_X, 410), "多肉植物・コーデックスの管理アプリ", fill=SUB, font=f_sub)
draw.text((LEFT_X, 460), "基本機能ぜんぶ無料 / 105種以上の植物DB", fill=WHITE, font=f_sub)

draw.text((LEFT_X, 540), "App Storeで入手  •  iPhone・iPad対応", fill=SUB, font=f_meta)

try:
    shot = Image.open("/Users/sherlockholmes/caudexcare-lp/screenshots/01_home.png")
    target_h = 540
    aspect = shot.width / shot.height
    target_w = int(target_h * aspect)
    shot_resized = shot.resize((target_w, target_h), Image.LANCZOS)
    mask = Image.new("L", (target_w, target_h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (target_w, target_h)], radius=40, fill=255)
    img.paste(shot_resized, (W - target_w - 60, 45), mask)
except Exception as e:
    print("Screenshot composite failed:", e)

img.save("/Users/sherlockholmes/caudexcare-lp/og.jpg", "JPEG", quality=88, optimize=True)
print(f"OG image saved: {W}x{H}")
