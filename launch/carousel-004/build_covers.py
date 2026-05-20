"""
Генерация 5 обложек каруселей Instagram (1080x1350 JPG)
Каждая обложка — со своим визуальным языком, чтобы лента не «слипалась».
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W, H = 1080, 1350
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ───── COLORS ─────
RED        = (192, 57, 43)
RED_BRIGHT = (220, 70, 55)
DARK       = (14, 14, 14)
DARK2      = (24, 24, 24)
LIGHT      = (255, 255, 255)
GRAY       = (155, 155, 155)
GRAY_DIM   = (90, 90, 90)

YANDEX     = (252, 63, 29)
TG_CYAN    = (61, 181, 240)
WARN_GOLD  = (242, 189, 66)
GOLD       = (245, 197, 61)
GREEN_VK   = (0, 119, 255)
AVITO_GRN  = (0, 175, 80)
MAX_PURPLE = (139, 95, 230)
DZEN_GOLD  = (252, 196, 25)

# ───── FONTS ─────
PATHS = {
    'sans-bold':    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    'sans-reg':     '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    'sans-cond-b':  '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf',
    'serif-bold-it':'/usr/share/fonts/truetype/dejavu/DejaVuSerif-BoldItalic.ttf',
    'serif-bold':   '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
}

def f(name, size):
    return ImageFont.truetype(PATHS[name], size)

def text_w(d, txt, font):
    bbox = d.textbbox((0, 0), txt, font=font)
    return bbox[2] - bbox[0]

def text_h(d, txt, font):
    bbox = d.textbbox((0, 0), txt, font=font)
    return bbox[3] - bbox[1]

# ───── COMMON ELEMENTS ─────
def draw_top_bar_and_logo(img, page_str, logo_color=LIGHT):
    """Красная полоса сверху + логотип ИНсайты + пагинатор"""
    d = ImageDraw.Draw(img)
    # red top bar
    d.rectangle([(0, 0), (W, 14)], fill=RED)

    # логотип-глаз (упрощённый)
    ex, ey = 80, 70
    d.ellipse([(ex, ey), (ex+56, ey+36)], fill=LIGHT, outline=DARK, width=2)
    d.ellipse([(ex+17, ey+7), (ex+39, ey+29)], fill=RED)
    d.ellipse([(ex+23, ey+13), (ex+33, ey+23)], fill=DARK)

    # ИН|сайты
    fnt_b = f('serif-bold', 42)
    fnt_r = f('serif-bold', 42)  # both bold serif for harmony
    fnt_lt = f('sans-reg', 36)
    d.text((ex+72, ey-6), 'ИН', font=fnt_b, fill=logo_color)
    in_w = text_w(d, 'ИН', fnt_b)
    d.text((ex+72+in_w+4, ey-6), 'сайты', font=fnt_lt, fill=logo_color)

    # pager top-right
    fnt_p = f('sans-bold', 20)
    bb = d.textbbox((0,0), page_str, font=fnt_p)
    d.text((W - 80 - (bb[2]-bb[0]), ey + 4), page_str, font=fnt_p, fill=GRAY)

def draw_footer(img, brand_text='Инсайты · Выпуск 004 · 04.05.2026', swipe='Свайпай →'):
    d = ImageDraw.Draw(img)
    fy = H - 80
    d.line([(80, fy), (W-80, fy)], fill=(255,255,255,40), width=1)
    fnt = f('sans-bold', 18)
    d.text((80, fy + 25), brand_text.upper(), font=fnt, fill=GRAY)
    bb = d.textbbox((0,0), swipe.upper(), font=fnt)
    d.text((W - 80 - (bb[2]-bb[0]), fy + 25), swipe.upper(), font=fnt, fill=RED)

def draw_eyebrow(d, text, x, y, bg=RED, fg=LIGHT, pad_x=24, pad_y=14, font_size=22):
    fnt = f('sans-bold', font_size)
    bb = d.textbbox((0,0), text, font=fnt)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    d.rectangle([(x, y), (x + tw + pad_x*2, y + th + pad_y*2)], fill=bg)
    d.text((x + pad_x, y + pad_y - 4), text, font=fnt, fill=fg)
    return y + th + pad_y*2

def wrap_text(text, font, draw, max_w):
    """Простой word-wrap"""
    words = text.split(' ')
    lines = []
    current = ''
    for w in words:
        test = (current + ' ' + w).strip()
        if text_w(draw, test, font) <= max_w:
            current = test
        else:
            if current: lines.append(current)
            current = w
    if current: lines.append(current)
    return lines

def draw_multiline(d, lines, x, y, font, fill, line_h):
    for i, line in enumerate(lines):
        d.text((x, y + i*line_h), line, font=font, fill=fill)
    return y + len(lines) * line_h

def draw_headline_with_em(d, parts, x, y, font_normal, font_em, fill_normal, fill_em, max_w, line_h):
    """parts = [(text, is_em), ...]
       Рисует headline с курсивным выделением
    """
    # сначала разбиваем на слова с пометками
    words = []
    for text, is_em in parts:
        for w in text.split(' '):
            if w: words.append((w, is_em))

    # формируем строки
    lines = []
    current = []  # list of (word, is_em)
    current_w = 0
    space_w = text_w(d, ' ', font_normal)

    for word, is_em in words:
        fnt = font_em if is_em else font_normal
        ww = text_w(d, word, fnt)
        if current and current_w + space_w + ww > max_w:
            lines.append(current)
            current = [(word, is_em)]
            current_w = ww
        else:
            if current: current_w += space_w
            current.append((word, is_em))
            current_w += ww
    if current: lines.append(current)

    # рисуем
    for i, line in enumerate(lines):
        cx = x
        ly = y + i*line_h
        for j, (word, is_em) in enumerate(line):
            fnt = font_em if is_em else font_normal
            color = fill_em if is_em else fill_normal
            d.text((cx, ly), word, font=fnt, fill=color)
            cx += text_w(d, word, fnt)
            if j < len(line)-1:
                cx += space_w
    return y + len(lines)*line_h

# ───────────────────────────────────────────────────────────────────
# COVER 01 — ЯНДЕКС НЕЙРО (editorial с фото Ольги)
# ───────────────────────────────────────────────────────────────────
def cover_01():
    img = Image.new('RGB', (W, H), DARK)
    d = ImageDraw.Draw(img)

    # Загружаем фото Ольги, кропим под левую часть
    photo = Image.open(os.path.join(OUT_DIR, 'olga-zibert.jpg'))
    photo_w, photo_h = 480, 720
    pw, ph = photo.size
    # cover-fit
    ratio = max(photo_w / pw, photo_h / ph)
    nw, nh = int(pw * ratio), int(ph * ratio)
    photo = photo.resize((nw, nh), Image.LANCZOS)
    cx, cy = (nw - photo_w)//2, (nh - photo_h)//2
    photo = photo.crop((cx, cy, cx + photo_w, cy + photo_h))
    # fade-overlay снизу для перетекания в фон
    img.paste(photo, (80, 280))

    # красная вертикальная акцент-полоса слева от фото
    d.rectangle([(60, 280), (80, 1000)], fill=RED)

    draw_top_bar_and_logo(img, '01 / 05')

    # правая колонка — текст
    rx = 600
    ry = 280

    # eyebrow
    ny = draw_eyebrow(d, 'СЛОВО РЕДАКТОРА · НОВОСТЬ 01', rx, ry, font_size=18)
    ry = ny + 24

    # stat
    stat_fnt = f('serif-bold-it', 220)
    d.text((rx - 8, ry - 30), '−47%', font=stat_fnt, fill=LIGHT)
    ry += 200

    # headline
    h_n = f('sans-bold', 56)
    h_em = f('serif-bold-it', 56)
    ry = draw_headline_with_em(d,
        [('Алиса', False), (' съела ', True), ('трафик клиник', False)],
        rx, ry, h_n, h_em, LIGHT, RED_BRIGHT, max_w=400, line_h=68)
    ry += 30

    # sub
    sub_fnt = f('sans-reg', 22)
    sub_lines = wrap_text(
        'Яндекс Нейро отвечает прямо в выдаче. На сайт никто не идёт. В категории «здоровье» — уже 40% запросов с AI-ответом.',
        sub_fnt, d, 400)
    draw_multiline(d, sub_lines, rx, ry, sub_fnt, (200,200,200), 32)

    # подпись Ольги внизу под фото
    cap_fnt = f('sans-bold', 18)
    d.text((80, 1020), 'ОЛЬГА ЗИБЕРТ', font=cap_fnt, fill=RED)
    cap2 = f('sans-reg', 18)
    d.text((80, 1050), 'Основатель «Инсайты»', font=cap2, fill=GRAY)
    d.text((80, 1080), 'Стратегический маркетинг для клиник', font=cap2, fill=GRAY)

    draw_footer(img)
    img.save(os.path.join(OUT_DIR, 'cover-01-yandex-neuro.jpg'), 'JPEG', quality=92)
    print('✓ cover-01-yandex-neuro.jpg')

# ───────────────────────────────────────────────────────────────────
# COVER 02 — TELEGRAM +47% (logo-hero, центровая композиция)
# ───────────────────────────────────────────────────────────────────
def cover_02():
    img = Image.new('RGB', (W, H), (8, 18, 34))
    d = ImageDraw.Draw(img)

    # лёгкое свечение в центре
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([(150, 200), (930, 980)], fill=(61, 181, 240, 35))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img.paste(glow, (0,0), glow)

    draw_top_bar_and_logo(img, '01 / 05')

    # ОГРОМНЫЙ бумажный самолёт Telegram (cyan)
    cx, cy, r = W//2, 520, 240
    # circle bg
    d.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=TG_CYAN)
    # paper plane (упрощённая форма)
    plane = [
        (cx-130, cy-10),  # left
        (cx+170, cy-110), # top right
        (cx+115, cy+130), # bottom right
        (cx+30, cy+50),   # crease bottom
        (cx-15, cy+90),   # tail bottom
        (cx-15, cy+10),   # tail middle
        (cx-130, cy-10),  # back to left
    ]
    d.polygon(plane, fill=LIGHT)
    # crease line
    d.line([(cx-130, cy-10), (cx+30, cy+50)], fill=TG_CYAN, width=4)

    # eyebrow
    eye_y = 130
    draw_eyebrow(d, 'НОВОСТЬ 02 · TELEGRAM · РФ', 80, 850, bg=TG_CYAN, fg=DARK, font_size=20)

    # gigantic stat
    stat_fnt = f('serif-bold-it', 380)
    txt = '+47%'
    bb = d.textbbox((0,0), txt, font=stat_fnt)
    tw = bb[2]-bb[0]
    d.text(((W-tw)//2 - 24, 200), txt, font=stat_fnt, fill=LIGHT)

    # Headline below
    h_n = f('sans-bold', 60)
    h_em = f('serif-bold-it', 60)
    ry = 940
    draw_headline_with_em(d,
        [('Telegram', False), (' обогнал ', True), ('классический performance', False)],
        80, ry, h_n, h_em, LIGHT, TG_CYAN, max_w=W-160, line_h=72)

    # sub
    sub_fnt = f('sans-reg', 24)
    d.text((80, 1140), 'Рынок посевов в РФ +47% за квартал.', font=sub_fnt, fill=(220,220,220))
    d.text((80, 1175), 'ROI первой интеграции для клиники до ×16.', font=sub_fnt, fill=(220,220,220))

    draw_footer(img)
    img.save(os.path.join(OUT_DIR, 'cover-02-telegram.jpg'), 'JPEG', quality=92)
    print('✓ cover-02-telegram.jpg')

# ───────────────────────────────────────────────────────────────────
# COVER 03 — ЕРИР · 500 000 ₽ (warning / alarm)
# ───────────────────────────────────────────────────────────────────
def cover_03():
    img = Image.new('RGB', (W, H), (18, 8, 8))
    d = ImageDraw.Draw(img)

    # red diagonal stripe pattern сверху
    stripe = Image.new('RGBA', (W, H), (0,0,0,0))
    sd = ImageDraw.Draw(stripe)
    for i in range(-200, W+200, 80):
        sd.polygon([(i, 0), (i+40, 0), (i+40-200, 200), (i-200, 200)],
                   fill=(192, 57, 43, 60))
    img.paste(stripe, (0,0), stripe)

    draw_top_bar_and_logo(img, '01 / 05')

    # warning triangle огромный
    cx, cy = W//2, 480
    s = 280
    triangle = [(cx, cy-s), (cx+s*0.95, cy+s*0.6), (cx-s*0.95, cy+s*0.6)]
    d.polygon(triangle, fill=WARN_GOLD)
    # outline
    d.line([triangle[0], triangle[1], triangle[2], triangle[0]], fill=DARK, width=8)
    # exclamation
    excl_fnt = f('sans-bold', 240)
    bb = d.textbbox((0,0), '!', font=excl_fnt)
    tw = bb[2]-bb[0]
    d.text((cx - tw//2 - 5, cy - 110), '!', font=excl_fnt, fill=DARK)

    # eyebrow
    draw_eyebrow(d, 'НОВОСТЬ 03 · ФАС · ШТРАФЫ 2026', 80, 820, bg=RED, fg=LIGHT, font_size=20)

    # stamped diagonal "ШТРАФ"
    stamp_fnt = f('sans-bold', 120)
    txt = '500 000 ₽'
    bb = d.textbbox((0,0), txt, font=stamp_fnt)
    tw = bb[2]-bb[0]
    d.text(((W-tw)//2, 900), txt, font=stamp_fnt, fill=LIGHT)

    # Headline below
    h_n = f('sans-bold', 52)
    h_em = f('serif-bold-it', 52)
    draw_headline_with_em(d,
        [('Штраф за', False), (' каждый ', True), ('немаркированный пост', False)],
        80, 1080, h_n, h_em, LIGHT, WARN_GOLD, max_w=W-160, line_h=64)

    draw_footer(img)
    img.save(os.path.join(OUT_DIR, 'cover-03-erir.jpg'), 'JPEG', quality=92)
    print('✓ cover-03-erir.jpg')

# ───────────────────────────────────────────────────────────────────
# COVER 04 — Креатор-экономика (video frame с REC-индикатором)
# ───────────────────────────────────────────────────────────────────
def cover_04():
    img = Image.new('RGB', (W, H), (18, 14, 8))
    d = ImageDraw.Draw(img)

    # gold gradient hint
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([(200, 180), (880, 860)], fill=(245, 197, 61, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    img.paste(glow, (0,0), glow)

    draw_top_bar_and_logo(img, '01 / 05')

    # video frame (выглядит как кадр стрима / Reels)
    fx, fy, fw, fh = 180, 240, 720, 600
    d.rectangle([(fx-6, fy-6), (fx+fw+6, fy+fh+6)], outline=GOLD, width=4)
    d.rectangle([(fx, fy), (fx+fw, fy+fh)], fill=(28, 22, 15))

    # большой play button
    pcx, pcy, pr = W//2, fy + fh//2, 90
    d.ellipse([(pcx-pr, pcy-pr), (pcx+pr, pcy+pr)], fill=GOLD)
    triangle = [(pcx-30, pcy-45), (pcx+50, pcy), (pcx-30, pcy+45)]
    d.polygon(triangle, fill=DARK)

    # REC dot + text top-left of frame
    rec_x, rec_y = fx + 30, fy + 30
    d.ellipse([(rec_x, rec_y), (rec_x+22, rec_y+22)], fill=RED_BRIGHT)
    rec_fnt = f('sans-bold', 22)
    d.text((rec_x + 36, rec_y - 2), 'LIVE · ВРАЧ-БЛОГЕР', font=rec_fnt, fill=LIGHT)

    # timestamp bottom-right of frame
    ts_fnt = f('sans-bold', 22)
    d.text((fx + fw - 130, fy + fh - 38), '14:32:08', font=ts_fnt, fill=GOLD)

    # eyebrow ниже фрейма
    draw_eyebrow(d, 'НОВОСТЬ 04 · КРЕАТОР-ЭКОНОМИКА · 96 МЛРД ₽', 80, 880,
                 bg=GOLD, fg=DARK, font_size=18)

    # stat
    stat_fnt = f('serif-bold-it', 140)
    d.text((80, 950), '×2,3', font=stat_fnt, fill=LIGHT)

    # Headline beside stat? нет, под
    h_n = f('sans-bold', 48)
    h_em = f('serif-bold-it', 48)
    draw_headline_with_em(d,
        [('Лид от врача', False), (' дешевле ', True), ('Яндекс.Директа', False)],
        80, 1110, h_n, h_em, LIGHT, GOLD, max_w=W-160, line_h=58)

    draw_footer(img)
    img.save(os.path.join(OUT_DIR, 'cover-04-creator.jpg'), 'JPEG', quality=92)
    print('✓ cover-04-creator.jpg')

# ───────────────────────────────────────────────────────────────────
# COVER 05 — 3 канала (триптих Max + Avito + Яндекс)
# ───────────────────────────────────────────────────────────────────
def cover_05():
    img = Image.new('RGB', (W, H), DARK)
    d = ImageDraw.Draw(img)

    draw_top_bar_and_logo(img, '01 / 05')

    # eyebrow
    draw_eyebrow(d, 'НОВОСТЬ 05 · НОВЫЕ ПОВЕРХНОСТИ РФ · 2026', 80, 180,
                 bg=RED, fg=LIGHT, font_size=20)

    # триптих — 3 квадратные карточки в ряд
    card_w, card_h = 280, 280
    gap = 20
    total_w = card_w*3 + gap*2
    start_x = (W - total_w)//2
    y = 320

    cards = [
        ('M', MAX_PURPLE, 'MAX', 'мессенджер VK'),
        ('A', AVITO_GRN,  'AVITO',  'классифайд'),
        ('Я', YANDEX,     'URBAN ADS', 'геотаргет'),
    ]

    for i, (letter, color, title, sub) in enumerate(cards):
        x = start_x + i*(card_w + gap)
        # card bg
        d.rounded_rectangle([(x, y), (x+card_w, y+card_h)], radius=24, fill=color)
        # letter
        big_fnt = f('sans-bold', 220)
        bb = d.textbbox((0,0), letter, font=big_fnt)
        tw = bb[2]-bb[0]; th = bb[3]-bb[1]
        d.text((x + (card_w-tw)//2, y + (card_h-th)//2 - 30), letter, font=big_fnt, fill=LIGHT)
        # subtitle below card
        title_fnt = f('sans-bold', 24)
        sub_fnt = f('sans-reg', 18)
        bb = d.textbbox((0,0), title, font=title_fnt)
        tw = bb[2]-bb[0]
        d.text((x + (card_w-tw)//2, y + card_h + 24), title, font=title_fnt, fill=LIGHT)
        bb = d.textbbox((0,0), sub, font=sub_fnt)
        tw = bb[2]-bb[0]
        d.text((x + (card_w-tw)//2, y + card_h + 60), sub, font=sub_fnt, fill=GRAY)

    # огромное "3" по центру внизу
    big_fnt = f('serif-bold-it', 240)
    txt = '3 канала'
    bb = d.textbbox((0,0), txt, font=big_fnt)
    tw = bb[2]-bb[0]
    d.text(((W-tw)//2, 760), txt, font=big_fnt, fill=LIGHT)

    # Headline
    h_n = f('sans-bold', 52)
    h_em = f('serif-bold-it', 52)
    draw_headline_with_em(d,
        [('Новые рекламные', False), (' поверхности ', True), ('РФ', False)],
        80, 1060, h_n, h_em, LIGHT, RED_BRIGHT, max_w=W-160, line_h=64)

    # sub
    sub_fnt = f('sans-reg', 22)
    d.text((80, 1190), 'К концу 2026 — до 22% бюджетов клиник', font=sub_fnt, fill=(200,200,200))

    draw_footer(img)
    img.save(os.path.join(OUT_DIR, 'cover-05-triptych.jpg'), 'JPEG', quality=92)
    print('✓ cover-05-triptych.jpg')


if __name__ == '__main__':
    cover_01()
    cover_02()
    cover_03()
    cover_04()
    cover_05()
    print('\nГотово. 5 обложек сохранены в:', OUT_DIR)
