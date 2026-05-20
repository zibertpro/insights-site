"""
Генерация всех 25 слайдов 5 каруселей Instagram (1080x1350 JPG).
Каждая карусель: cover → news → mechanics → landing-clinic → landing-dental.
Каждая обложка визуально отличается от других.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W, H = 1080, 1350
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ───── COLORS ─────
RED        = (192, 57, 43)
RED_BRIGHT = (220, 70, 55)
DARK       = (14, 14, 14)
LIGHT      = (255, 255, 255)
GRAY       = (155, 155, 155)
GRAY_DIM   = (90, 90, 90)
GRAY_TEXT  = (74, 74, 74)
LGRAY      = (232, 232, 232)
BG_CARD    = (242, 242, 242)
BG_VEB     = (249, 249, 249)

YANDEX     = (252, 63, 29)
TG_CYAN    = (61, 181, 240)
WARN_GOLD  = (242, 189, 66)
GOLD       = (245, 197, 61)
GREEN_VK   = (0, 119, 255)
AVITO_GRN  = (0, 175, 80)
MAX_PURPLE = (139, 95, 230)

# ───── FONTS ─────
FP = {
    'sans-bold':    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    'sans-reg':     '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    'sans-cond-b':  '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf',
    'serif-bold-it':'/usr/share/fonts/truetype/dejavu/DejaVuSerif-BoldItalic.ttf',
    'serif-bold':   '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
    'serif-it':     '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf',
}

def f(name, size):
    return ImageFont.truetype(FP[name], size)

def tw(d, txt, font):
    bb = d.textbbox((0,0), txt, font=font)
    return bb[2] - bb[0]

def th(d, txt, font):
    bb = d.textbbox((0,0), txt, font=font)
    return bb[3] - bb[1]

def fit_font(d, txt, fp_key, max_w, start_size, min_size=20, step=4):
    size = start_size
    while size > min_size:
        fnt = f(fp_key, size)
        if tw(d, txt, fnt) <= max_w:
            return fnt, size
        size -= step
    return f(fp_key, min_size), min_size

def wrap(d, text, font, max_w):
    words = text.split(' ')
    lines, cur = [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if tw(d, test, font) <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def draw_lines(d, lines, x, y, font, fill, line_h):
    for i, line in enumerate(lines):
        d.text((x, y + i*line_h), line, font=font, fill=fill)
    return y + len(lines) * line_h

def draw_em(d, parts, x, y, font_n, font_em, fill_n, fill_em, max_w, line_h):
    """parts = [(text, is_em)] — рисует с курсивным выделением"""
    words = []
    for text, is_em in parts:
        for w in text.split(' '):
            if w: words.append((w, is_em))
    space_w = tw(d, ' ', font_n)
    lines, cur, cur_w = [], [], 0
    for word, is_em in words:
        fnt = font_em if is_em else font_n
        ww = tw(d, word, fnt)
        if cur and cur_w + space_w + ww > max_w:
            lines.append(cur); cur = [(word, is_em)]; cur_w = ww
        else:
            if cur: cur_w += space_w
            cur.append((word, is_em)); cur_w += ww
    if cur: lines.append(cur)
    for i, line in enumerate(lines):
        cx = x; ly = y + i*line_h
        for j, (word, is_em) in enumerate(line):
            fnt = font_em if is_em else font_n
            color = fill_em if is_em else fill_n
            d.text((cx, ly), word, font=fnt, fill=color)
            cx += tw(d, word, fnt)
            if j < len(line)-1: cx += space_w
    return y + len(lines)*line_h

# ───── COMMON HEADER/FOOTER ─────
def header_dark(img, page_str):
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (W, 14)], fill=RED)
    # logo glaz
    ex, ey = 80, 70
    d.ellipse([(ex, ey), (ex+56, ey+36)], fill=LIGHT, outline=DARK, width=2)
    d.ellipse([(ex+17, ey+7), (ex+39, ey+29)], fill=RED)
    d.ellipse([(ex+23, ey+13), (ex+33, ey+23)], fill=DARK)
    fnt_b = f('serif-bold', 42)
    fnt_lt = f('sans-reg', 36)
    d.text((ex+72, ey-6), 'ИН', font=fnt_b, fill=LIGHT)
    in_w = tw(d, 'ИН', fnt_b)
    d.text((ex+72+in_w+4, ey-6), 'сайты', font=fnt_lt, fill=LIGHT)
    fnt_p = f('sans-bold', 20)
    bb = d.textbbox((0,0), page_str, font=fnt_p)
    d.text((W - 80 - (bb[2]-bb[0]), ey + 4), page_str, font=fnt_p, fill=GRAY)

def header_light(img, page_str):
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (W, 14)], fill=RED)
    ex, ey = 80, 70
    d.ellipse([(ex, ey), (ex+56, ey+36)], fill=LIGHT, outline=DARK, width=2)
    d.ellipse([(ex+17, ey+7), (ex+39, ey+29)], fill=RED)
    d.ellipse([(ex+23, ey+13), (ex+33, ey+23)], fill=DARK)
    fnt_b = f('serif-bold', 42)
    fnt_lt = f('sans-reg', 36)
    d.text((ex+72, ey-6), 'ИН', font=fnt_b, fill=DARK)
    in_w = tw(d, 'ИН', fnt_b)
    d.text((ex+72+in_w+4, ey-6), 'сайты', font=fnt_lt, fill=DARK)
    fnt_p = f('sans-bold', 20)
    bb = d.textbbox((0,0), page_str, font=fnt_p)
    d.text((W - 80 - (bb[2]-bb[0]), ey + 4), page_str, font=fnt_p, fill=GRAY)

def footer_dark(img, brand='Инсайты · Выпуск 004 · 04.05.2026', swipe='Свайпай →'):
    d = ImageDraw.Draw(img)
    fy = H - 80
    d.line([(80, fy), (W-80, fy)], fill=(60,60,60), width=1)
    fnt = f('sans-bold', 18)
    d.text((80, fy + 25), brand.upper(), font=fnt, fill=GRAY)
    bb = d.textbbox((0,0), swipe.upper(), font=fnt)
    d.text((W - 80 - (bb[2]-bb[0]), fy + 25), swipe.upper(), font=fnt, fill=RED)

def footer_light(img, brand='Инсайты · Выпуск 004 · 04.05.2026', swipe='Свайпай →'):
    d = ImageDraw.Draw(img)
    fy = H - 80
    d.line([(80, fy), (W-80, fy)], fill=LGRAY, width=1)
    fnt = f('sans-bold', 18)
    d.text((80, fy + 25), brand.upper(), font=fnt, fill=GRAY_DIM)
    bb = d.textbbox((0,0), swipe.upper(), font=fnt)
    d.text((W - 80 - (bb[2]-bb[0]), fy + 25), swipe.upper(), font=fnt, fill=RED)

def eyebrow(d, text, x, y, bg=RED, fg=LIGHT, size=18, pad_x=20, pad_y=12):
    fnt = f('sans-bold', size)
    bb = d.textbbox((0,0), text, font=fnt)
    twd, thd = bb[2]-bb[0], bb[3]-bb[1]
    d.rectangle([(x, y), (x + twd + pad_x*2, y + thd + pad_y*2)], fill=bg)
    d.text((x + pad_x, y + pad_y - 4), text, font=fnt, fill=fg)
    return y + thd + pad_y*2

def save(img, name):
    p = os.path.join(OUT_DIR, name)
    img.save(p, 'JPEG', quality=92, optimize=True)
    print(f'✓ {name}')

# ════════════════════════════════════════════════════════════════════
# CAROUSEL 01 — ЯНДЕКС НЕЙРО
# ════════════════════════════════════════════════════════════════════

def c01_s1_cover():
    """Editorial с фото Ольги"""
    img = Image.new('RGB', (W, H), DARK)
    d = ImageDraw.Draw(img)
    header_dark(img, '01 / 05')

    # фото слева
    photo = Image.open(os.path.join(OUT_DIR, 'olga-zibert.jpg'))
    pw_target, ph_target = 460, 700
    pw, ph = photo.size
    ratio = max(pw_target / pw, ph_target / ph)
    nw, nh = int(pw * ratio), int(ph * ratio)
    photo = photo.resize((nw, nh), Image.LANCZOS)
    cx, cy = (nw - pw_target)//2, (nh - ph_target)//2
    photo = photo.crop((cx, cy, cx + pw_target, cy + ph_target))
    img.paste(photo, (90, 280))
    d.rectangle([(70, 280), (90, 980)], fill=RED)

    # подпись под фото
    cap_fnt = f('sans-bold', 19)
    d.text((90, 1000), 'ОЛЬГА ЗИБЕРТ', font=cap_fnt, fill=RED)
    cap2 = f('sans-reg', 17)
    d.text((90, 1028), 'Основатель «Инсайты»', font=cap2, fill=GRAY)
    d.text((90, 1054), 'Стратегический маркетинг для клиник', font=cap2, fill=GRAY)

    # правая колонка — текст
    rx, ry = 600, 280

    # eyebrow
    eyebrow(d, 'СЛОВО РЕДАКТОРА · НОВОСТЬ 01', rx, ry, size=15)
    ry += 70

    # stat — auto-fit
    stat_fnt, _ = fit_font(d, '−47%', 'serif-bold-it', 400, 200)
    d.text((rx, ry), '−47%', font=stat_fnt, fill=LIGHT)
    ry += th(d, '−47%', stat_fnt) + 30

    # headline
    h_n = f('sans-bold', 50)
    h_em = f('serif-bold-it', 50)
    ry = draw_em(d, [('Алиса', False), (' съела ', True), ('трафик клиник', False)],
                 rx, ry, h_n, h_em, LIGHT, RED_BRIGHT, max_w=410, line_h=60)
    ry += 25

    # sub
    sub_fnt = f('sans-reg', 20)
    sub_lines = wrap(d, 'Яндекс Нейро отвечает прямо в выдаче. На сайт никто не идёт. В категории «здоровье» — уже 40% запросов с AI-ответом.', sub_fnt, 410)
    draw_lines(d, sub_lines, rx, ry, sub_fnt, (210,210,210), 30)

    footer_dark(img)
    save(img, 'c01-s1-cover.jpg')

def c01_s2_news():
    img = Image.new('RGB', (W, H), LIGHT)
    d = ImageDraw.Draw(img)
    header_light(img, '02 / 05')

    x, y = 80, 220
    eyebrow(d, 'ЧТО ПРОИЗОШЛО', x, y, size=16)
    y += 62

    h_n = f('sans-bold', 52)
    h_em = f('serif-bold-it', 52)
    y = draw_em(d, [('Россия повторила сценарий', False), (' Google AI Overviews ', True), ('— но радикальнее', False)],
                x, y, h_n, h_em, DARK, RED, max_w=W-160, line_h=64)
    y += 40

    body_fnt = f('sans-reg', 24)
    body_b = f('sans-bold', 24)
    p1 = 'Если в Google ссылки ещё показываются рядом с ответом, то Яндекс Нейро и Алиса Про в значительной части сценариев дают развёрнутый текст-ответ — без перехода на сайт.'
    p2 = 'Симптомные запросы — «болит зуб мудрости», «к какому врачу при боли в спине» — конвертируются прямо в ответ ассистента. Клиника остаётся без просмотра страницы.'
    for p in [p1, p2]:
        lines = wrap(d, p, body_fnt, W-160)
        y = draw_lines(d, lines, x, y, body_fnt, GRAY_TEXT, 36)
        y += 24

    footer_light(img)
    save(img, 'c01-s2-news.jpg')

def c01_s3_mech():
    img = Image.new('RGB', (W, H), BG_VEB)
    d = ImageDraw.Draw(img)
    header_light(img, '03 / 05')
    x, y = 80, 220
    eyebrow(d, 'ХОРОШАЯ НОВОСТЬ', x, y, size=16)
    y += 62

    h_n = f('sans-bold', 50)
    h_em = f('serif-bold-it', 50)
    y = draw_em(d, [('Цитирование в Нейро даёт', False), (' +25–40% к кликам ', True), ('— больше, чем 2–3 место в выдаче', False)],
                x, y, h_n, h_em, DARK, RED, max_w=W-160, line_h=62)
    y += 36

    body_fnt = f('sans-reg', 24)
    p1 = '«Попасть в ответ» теперь ценнее, чем «занять топ». Падение органики неравномерное: сильнее всего пострадали те, кто жил на «информационке» без бренда.'
    p2 = 'Клиники с экспертными авторскими страницами, отзывами и заполненной картой теряют меньше — Нейро всё равно ссылается на проверенные источники.'
    for p in [p1, p2]:
        lines = wrap(d, p, body_fnt, W-160)
        y = draw_lines(d, lines, x, y, body_fnt, GRAY_TEXT, 36)
        y += 24

    # pull quote
    py = y + 10
    pull_h = 130
    d.rectangle([(x, py), (W-80, py+pull_h)], fill=BG_CARD)
    d.rectangle([(x, py), (x+5, py+pull_h)], fill=RED)
    pull_fnt = f('sans-bold', 24)
    pull_lines = wrap(d, 'SEO 2026 — это не «оптимизировать тайтлы», а упаковать экспертность так, чтобы её цитировал AI.', pull_fnt, W-160-40)
    draw_lines(d, pull_lines, x+25, py+22, pull_fnt, DARK, 32)

    footer_light(img)
    save(img, 'c01-s3-mech.jpg')

def landing_slide(filename, page, news_n, audience, headline_parts, bullets,
                  cta='Свайпни → следующая карусель', tag_color=RED, tag_text=None, footer_brand=None):
    img = Image.new('RGB', (W, H), LIGHT)
    d = ImageDraw.Draw(img)
    header_light(img, page)

    x, y = 80, 220
    eyebrow(d, f'ПРИЗЕМЛЕНИЕ · К НОВОСТИ {news_n}', x, y, size=15)
    y += 58

    if tag_text is None:
        tag_text = audience.upper()
    tag_fnt = f('sans-bold', 17)
    bb = d.textbbox((0,0), tag_text, font=tag_fnt)
    twd, thd = bb[2]-bb[0], bb[3]-bb[1]
    d.rectangle([(x, y), (x + twd + 36, y + thd + 24)], fill=tag_color)
    d.text((x + 18, y + 12 - 4), tag_text, font=tag_fnt, fill=LIGHT)
    y += thd + 50

    h_n = f('sans-bold', 46)
    h_em = f('serif-bold-it', 46)
    y = draw_em(d, headline_parts, x, y, h_n, h_em, DARK, RED, max_w=W-160, line_h=58)
    y += 34

    bullet_fnt = f('sans-reg', 22)
    bullet_b = f('sans-bold', 22)
    for bullet_parts in bullets:
        # bullet marker
        d.rectangle([(x, y+12), (x+22, y+16)], fill=tag_color)
        # text
        space_w = tw(d, ' ', bullet_fnt)
        words = []
        for text, is_b in bullet_parts:
            for w in text.split(' '):
                if w: words.append((w, is_b))
        cx = x + 38; cy = y
        line_h = 32
        cur_w = 0
        max_w = W - 160 - 38
        for j, (word, is_b) in enumerate(words):
            fnt = bullet_b if is_b else bullet_fnt
            ww = tw(d, word, fnt)
            if cx > x + 38 and cur_w + space_w + ww > max_w:
                cy += line_h
                cx = x + 38
                cur_w = 0
            if cur_w > 0:
                cx += space_w
                cur_w += space_w
            color = DARK if is_b else GRAY_TEXT
            d.text((cx, cy), word, font=fnt, fill=color)
            cx += ww
            cur_w += ww
        y = cy + line_h + 14

    # CTA
    cta_y = H - 150
    d.line([(80, cta_y), (W-80, cta_y)], fill=LGRAY, width=1)
    cta_fnt = f('serif-it', 22)
    d.text((80, cta_y + 18), cta, font=cta_fnt, fill=GRAY_TEXT)

    if footer_brand:
        footer_light(img, brand=footer_brand)
    else:
        footer_light(img, brand=f'Инсайты · {audience}')
    save(img, filename)

def c01_s4_clinic():
    landing_slide(
        filename='c01-s4-clinic.jpg', page='04 / 05', news_n='01',
        audience='Многопрофильная клиника',
        headline_parts=[('Перепаковать сайт под', False), (' цитирование Нейро', True)],
        bullets=[
            [('Взять ', False), ('10 симптомных запросов', True), (' из Яндекс.Вордстат и переписать страницы под формат AI-ответа: короткий ответ → FAQ → автор-врач', False)],
            [('Подключить ', False), ('schema.org', True), (' MedicalClinic / Physician / FAQPage', False)],
            [('Заполнить ', False), ('карточку в Яндекс.Бизнесе', True), (' — без неё цитирование в Нейро не работает', False)],
            [('Завести ', False), ('страницы врачей', True), (' с фото, опытом и публикациями', False)],
        ],
        cta='Свайпни → стоматологический угол',
        tag_color=RED,
    )

def c01_s5_dental():
    landing_slide(
        filename='c01-s5-dental.jpg', page='05 / 05', news_n='01',
        audience='Стоматология',
        headline_parts=[('Имя врача =', False), (' ответ ассистента', True)],
        bullets=[
            [('Через 6–9 месяцев пациент будет спрашивать у Алисы: ', False), ('«найди стоматолога-имплантолога в моём районе»', True)],
            [('Какое имя — зависит от ', False), ('цифрового следа врача', True), (': интервью, разборы кейсов, экспертные комментарии', False)],
            [('Профиль на ', False), ('Prodoctorov / НаПоправку', True), (' с отзывами на конкретные процедуры — обязателен', False)],
            [('Видео-разборы кейсов в ', False), ('VK Видео или YouTube', True), (' — капитал, который монетизируется в 2027', False)],
        ],
        cta='Конец карусели · Дальше — про Telegram +47%',
        tag_color=DARK,
    )

# ════════════════════════════════════════════════════════════════════
# CAROUSEL 02 — TELEGRAM +47%
# ════════════════════════════════════════════════════════════════════

def c02_s1_cover():
    """Logo-hero composition"""
    img = Image.new('RGB', (W, H), (8, 18, 34))
    d = ImageDraw.Draw(img)

    # лёгкое свечение
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([(150, 200), (930, 980)], fill=(61, 181, 240, 30))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img.paste(glow, (0,0), glow)

    header_dark(img, '01 / 05')

    # композиция: огромный paper plane слева, +47% справа
    # paper plane
    pcx, pcy, pr = 320, 530, 200
    d.ellipse([(pcx-pr, pcy-pr), (pcx+pr, pcy+pr)], fill=TG_CYAN)
    plane = [
        (pcx-105, pcy-5), (pcx+135, pcy-90),
        (pcx+90, pcy+105), (pcx+25, pcy+40),
        (pcx-12, pcy+72), (pcx-12, pcy+8), (pcx-105, pcy-5),
    ]
    d.polygon(plane, fill=LIGHT)
    d.line([(pcx-105, pcy-5), (pcx+25, pcy+40)], fill=TG_CYAN, width=4)

    # +47% справа от plane (auto-fit)
    stat_txt = '+47%'
    stat_fnt, _ = fit_font(d, stat_txt, 'serif-bold-it', 460, 280)
    sx = 580
    sy = pcy - th(d, stat_txt, stat_fnt)//2 - 30
    d.text((sx, sy), stat_txt, font=stat_fnt, fill=LIGHT)

    # eyebrow
    eyebrow(d, 'НОВОСТЬ 02 · TELEGRAM · РФ', 80, 850, bg=TG_CYAN, fg=DARK, size=18)

    # Headline
    h_n = f('sans-bold', 56)
    h_em = f('serif-bold-it', 56)
    draw_em(d, [('Telegram', False), (' обогнал ', True), ('классический performance', False)],
            80, 940, h_n, h_em, LIGHT, TG_CYAN, max_w=W-160, line_h=68)

    # sub
    sub_fnt = f('sans-reg', 22)
    d.text((80, 1170), 'Рынок посевов в РФ +47% за квартал.', font=sub_fnt, fill=(220,220,220))
    d.text((80, 1202), 'ROI первой интеграции для клиники до ×16.', font=sub_fnt, fill=(220,220,220))

    footer_dark(img)
    save(img, 'c02-s1-cover.jpg')

def c02_s2_news():
    img = Image.new('RGB', (W, H), LIGHT)
    d = ImageDraw.Draw(img)
    header_light(img, '02 / 05')
    x, y = 80, 220
    eyebrow(d, 'ЧТО ПРОИЗОШЛО', x, y, size=16); y += 62
    h_n = f('sans-bold', 56)
    h_em = f('serif-bold-it', 56)
    y = draw_em(d, [(' 71% ', True), ('россиян доверяют Telegram-каналам как источнику новостей', False)],
                x, y, h_n, h_em, DARK, RED, max_w=W-160, line_h=68)
    y += 40
    body_fnt = f('sans-reg', 24)
    p1 = '76% доверяют конкретным авторам — врачам, экспертам, блогерам. Это в 9 раз больше, чем телевидению.'
    p2 = 'Telegram перестал быть «дополнительным каналом». В I квартале 2026 он впервые превысил суммарные бюджеты Яндекс.Директа в недвижимости, медицине, образовании и бьюти.'
    for p in [p1, p2]:
        lines = wrap(d, p, body_fnt, W-160)
        y = draw_lines(d, lines, x, y, body_fnt, GRAY_TEXT, 36); y += 24
    footer_light(img)
    save(img, 'c02-s2-news.jpg')

def c02_s3_mech():
    img = Image.new('RGB', (W, H), BG_VEB)
    d = ImageDraw.Draw(img)
    header_light(img, '03 / 05')
    x, y = 80, 220
    eyebrow(d, 'ЧТО МЕНЯЕТСЯ', x, y, size=16); y += 62
    h_n = f('sans-bold', 56)
    h_em = f('serif-bold-it', 56)
    y = draw_em(d, [('Креатив больше не работает.', False), (' Работает воронка', True)],
                x, y, h_n, h_em, DARK, RED, max_w=W-160, line_h=68)
    y += 40
    body_fnt = f('sans-reg', 24)
    p1 = 'Простые рекламные посты с «акция / запись / телефон» проседают.'
    p2 = 'Конвертирующая связка 2026: нативный пост-новость в чужом канале → 3 поста-приземления в своём канале → бот с подарком → CRM/КЦ со скриптами под каждый тип лида.'
    for p in [p1, p2]:
        lines = wrap(d, p, body_fnt, W-160)
        y = draw_lines(d, lines, x, y, body_fnt, GRAY_TEXT, 36); y += 24

    py = y + 10; pull_h = 130
    d.rectangle([(x, py), (W-80, py+pull_h)], fill=BG_CARD)
    d.rectangle([(x, py), (x+5, py+pull_h)], fill=RED)
    pull_fnt = f('sans-bold', 24)
    pull_lines = wrap(d, 'Без воронки бюджет «улетает»: пользователь читает интересный пост — и никуда не идёт.', pull_fnt, W-160-40)
    draw_lines(d, pull_lines, x+25, py+22, pull_fnt, DARK, 32)

    footer_light(img)
    save(img, 'c02-s3-mech.jpg')

def c02_s4_clinic():
    landing_slide(
        filename='c02-s4-clinic.jpg', page='04 / 05', news_n='02',
        audience='Многопрофильная клиника',
        headline_parts=[('Воронка', False), (' вместо ', True), ('креатива', False)],
        bullets=[
            [('Запустить ', False), ('1 посев', True), (' в проверенном канале — с полной связкой: пост + 3 приземления + бот + скрипты', False)],
            [('Сравнить ', False), ('cost-per-lead', True), (' с текущим контекстом — обычно в 2–3 раза дешевле', False)],
            [('Перед посевом — ', False), ('обязательно', True), (' завести свой Telegram-канал с регулярным контентом и 500–1 000 подписчиков', False)],
            [('Без своего канала ', False), ('посев бесполезен', True), (' — приземлять некуда', False)],
        ],
        cta='Свайпни → стоматологический угол',
        tag_color=RED,
    )

def c02_s5_dental():
    landing_slide(
        filename='c02-s5-dental.jpg', page='05 / 05', news_n='02',
        audience='Стоматология',
        headline_parts=[('Канал врача', False), (' важнее ', True), ('канала клиники', False)],
        bullets=[
            [('Личный канал ', False), ('имплантолога / ортодонта', True), (' работает на доверие сильнее брендового', False)],
            [('Контент: ', False), ('кейсы пациентов, процессы, разборы', True), (' — даёт горячий лид', False)],
            [('Тест: запустить параллельно ', False), ('2 интеграции', True), (' — на канал клиники и на канал врача', False)],
            [('Часто канал врача ', False), ('выигрывает 2:1', True), (' по доходимости до договора', False)],
        ],
        cta='Конец карусели · Дальше — про штрафы 500 000 ₽',
        tag_color=DARK,
    )

# ════════════════════════════════════════════════════════════════════
# CAROUSEL 03 — ЕРИР · 500 000 ₽
# ════════════════════════════════════════════════════════════════════

def c03_s1_cover():
    img = Image.new('RGB', (W, H), (18, 8, 8))
    d = ImageDraw.Draw(img)

    # diagonal stripe pattern
    stripe = Image.new('RGBA', (W, H), (0,0,0,0))
    sd = ImageDraw.Draw(stripe)
    for i in range(-200, W+200, 80):
        sd.polygon([(i, 0), (i+40, 0), (i+40-200, 200), (i-200, 200)],
                   fill=(192, 57, 43, 70))
    img.paste(stripe, (0,0), stripe)

    header_dark(img, '01 / 05')

    # warning triangle
    cx, cy = W//2, 480; s = 240
    triangle = [(cx, cy-s), (cx+int(s*0.95), cy+int(s*0.6)), (cx-int(s*0.95), cy+int(s*0.6))]
    d.polygon(triangle, fill=WARN_GOLD)
    d.line([triangle[0], triangle[1], triangle[2], triangle[0]], fill=DARK, width=8)
    excl_fnt = f('sans-bold', 220)
    bb = d.textbbox((0,0), '!', font=excl_fnt)
    d.text((cx - (bb[2]-bb[0])//2 - 5, cy - 110), '!', font=excl_fnt, fill=DARK)

    eyebrow(d, 'НОВОСТЬ 03 · ФАС · ШТРАФЫ 2026', 80, 800, bg=RED, fg=LIGHT, size=18)

    # stat
    stat_txt = '500 000 ₽'
    stat_fnt, _ = fit_font(d, stat_txt, 'serif-bold-it', W-160, 180)
    sw = tw(d, stat_txt, stat_fnt)
    d.text(((W-sw)//2, 880), stat_txt, font=stat_fnt, fill=LIGHT)

    # headline
    h_n = f('sans-bold', 50)
    h_em = f('serif-bold-it', 50)
    draw_em(d, [('Штраф за', False), (' каждый ', True), ('немаркированный пост', False)],
            80, 1080, h_n, h_em, LIGHT, WARN_GOLD, max_w=W-160, line_h=62)

    footer_dark(img)
    save(img, 'c03-s1-cover.jpg')

def c03_s2_news():
    img = Image.new('RGB', (W, H), LIGHT)
    d = ImageDraw.Draw(img)
    header_light(img, '02 / 05')
    x, y = 80, 220
    eyebrow(d, 'ЧТО ПОПАДАЕТ ПОД ЗАКОН', x, y, size=16); y += 62
    h_n = f('sans-bold', 56)
    h_em = f('serif-bold-it', 56)
    y = draw_em(d, [('Шире,', False), (' чем многие думают', True)],
                x, y, h_n, h_em, DARK, RED, max_w=W-160, line_h=68)
    y += 40
    body_fnt = f('sans-reg', 24)
    p1 = 'Под обязательную маркировку с токеном ОРД попадают: посты блогеров с упоминанием бренда, интеграции в Telegram-каналах, видео в VK Видео и YouTube с продакт-плейсментом, сторис, рилсы, кружочки.'
    p2 = 'Под удар попали клиники, которые работают с врачами-блогерами «по доверию» — без юридического оформления.'
    for p in [p1, p2]:
        lines = wrap(d, p, body_fnt, W-160)
        y = draw_lines(d, lines, x, y, body_fnt, GRAY_TEXT, 36); y += 24
    footer_light(img)
    save(img, 'c03-s2-news.jpg')

def c03_s3_mech():
    img = Image.new('RGB', (W, H), BG_VEB)
    d = ImageDraw.Draw(img)
    header_light(img, '03 / 05')
    x, y = 80, 220
    eyebrow(d, 'ГЛАВНЫЙ РИСК', x, y, size=16); y += 62
    h_n = f('sans-bold', 56)
    h_em = f('serif-bold-it', 56)
    y = draw_em(d, [('Не только штраф.', False), (' Приостановка ', True), ('рекламной деятельности', False)],
                x, y, h_n, h_em, DARK, RED, max_w=W-160, line_h=68)
    y += 36
    body_fnt = f('sans-reg', 24)
    p1 = 'После повторного нарушения клиника может остаться без основных рекламных каналов на месяцы.'
    p2 = 'В медицине добавляются свои ограничения: запрещены гарантии результата, формулировки «лучший», «единственный», «100%-ный».'
    for p in [p1, p2]:
        lines = wrap(d, p, body_fnt, W-160)
        y = draw_lines(d, lines, x, y, body_fnt, GRAY_TEXT, 36); y += 24

    py = y + 10; pull_h = 150
    d.rectangle([(x, py), (W-80, py+pull_h)], fill=BG_CARD)
    d.rectangle([(x, py), (x+5, py+pull_h)], fill=RED)
    pull_fnt = f('sans-bold', 23)
    pull_lines = wrap(d, 'Что нужно за 30 дней: подключить ОРД, перевести договоры с блогерами в письменную форму, маркировать каждый пост.', pull_fnt, W-160-40)
    draw_lines(d, pull_lines, x+25, py+22, pull_fnt, DARK, 32)
    footer_light(img)
    save(img, 'c03-s3-mech.jpg')

def c03_s4_clinic():
    landing_slide(
        filename='c03-s4-clinic.jpg', page='04 / 05', news_n='03',
        audience='Многопрофильная клиника',
        headline_parts=[('Регламент', False), (' «Маркировка-30»', True)],
        bullets=[
            [('Подключить ', False), ('ОРД', True), (' к юрлицу клиники (Яндекс ОРД — самый простой)', False)],
            [('Назначить ', False), ('ответственного', True), (' — обычно СММ-менеджер или агентство', False)],
            [('Завести единый чек-лист: ', False), ('договор → токен → пометка → отчёт в ЕРИР', True)],
            [('Аудит за 1 день: ', False), ('выгрузить рекламные посты', True), (' за 3 месяца. Если без токенов — есть риск штрафа', False)],
        ],
        cta='Свайпни → стоматологический угол',
        tag_color=RED,
    )

def c03_s5_dental():
    landing_slide(
        filename='c03-s5-dental.jpg', page='05 / 05', news_n='03',
        audience='Стоматология',
        headline_parts=[('Договоры со всеми', False), (' врачами-блогерами', True)],
        bullets=[
            [('Часто врач сам ведёт канал и пишет о клинике. Для ФАС ', False), ('это может быть рекламой без денег', True), (' — если есть аффилированность', False)],
            [('Разделить контент врача на ', False), ('3 категории', True), (': личное (без маркировки), упоминание клиники с ценами (с маркировкой), оплачиваемая интеграция (с маркировкой и договором)', False)],
            [('Обучить врачей ', False), ('30-минутным скриптом', True), (' — что писать можно, что нельзя', False)],
            [('Один договор + регламент = ', False), ('защита юрлица', True), (' от штрафов', False)],
        ],
        cta='Конец карусели · Дальше — креатор-экономика 96 млрд ₽',
        tag_color=DARK,
    )

# ════════════════════════════════════════════════════════════════════
# CAROUSEL 04 — КРЕАТОР-ЭКОНОМИКА
# ════════════════════════════════════════════════════════════════════

def c04_s1_cover():
    img = Image.new('RGB', (W, H), (18, 14, 8))
    d = ImageDraw.Draw(img)
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([(200, 180), (880, 860)], fill=(245, 197, 61, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    img.paste(glow, (0,0), glow)

    header_dark(img, '01 / 05')

    # video frame
    fx, fy, fw, fh = 180, 240, 720, 600
    d.rectangle([(fx-6, fy-6), (fx+fw+6, fy+fh+6)], outline=GOLD, width=4)
    d.rectangle([(fx, fy), (fx+fw, fy+fh)], fill=(28, 22, 15))

    # play button
    pcx, pcy, pr = W//2, fy + fh//2, 90
    d.ellipse([(pcx-pr, pcy-pr), (pcx+pr, pcy+pr)], fill=GOLD)
    triangle = [(pcx-30, pcy-45), (pcx+50, pcy), (pcx-30, pcy+45)]
    d.polygon(triangle, fill=DARK)

    # REC dot + text
    rec_x, rec_y = fx + 30, fy + 30
    d.ellipse([(rec_x, rec_y), (rec_x+22, rec_y+22)], fill=RED_BRIGHT)
    rec_fnt = f('sans-bold', 22)
    d.text((rec_x + 36, rec_y - 2), 'LIVE · ВРАЧ-БЛОГЕР', font=rec_fnt, fill=LIGHT)

    # timestamp
    ts_fnt = f('sans-bold', 22)
    d.text((fx + fw - 130, fy + fh - 38), '14:32:08', font=ts_fnt, fill=GOLD)

    eyebrow(d, 'НОВОСТЬ 04 · КРЕАТОР-ЭКОНОМИКА · 96 МЛРД ₽', 80, 880, bg=GOLD, fg=DARK, size=15)

    # stat (auto-fit)
    stat_txt = '×2,3'
    stat_fnt, _ = fit_font(d, stat_txt, 'serif-bold-it', W-160, 140)
    d.text((80, 945), stat_txt, font=stat_fnt, fill=LIGHT)

    # headline
    h_n = f('sans-bold', 46)
    h_em = f('serif-bold-it', 46)
    draw_em(d, [('Лид от врача', False), (' дешевле ', True), ('Яндекс.Директа', False)],
            80, 1110, h_n, h_em, LIGHT, GOLD, max_w=W-160, line_h=58)

    footer_dark(img)
    save(img, 'c04-s1-cover.jpg')

def c04_s2_news():
    img = Image.new('RGB', (W, H), LIGHT)
    d = ImageDraw.Draw(img)
    header_light(img, '02 / 05')
    x, y = 80, 220
    eyebrow(d, 'ЧТО ПРОИЗОШЛО', x, y, size=16); y += 62
    h_n = f('sans-bold', 50)
    h_em = f('serif-bold-it', 50)
    y = draw_em(d, [('Не блогер на 1 млн.', False), (' Микро-эксперт ', True), ('на 3–10 тыс.', False)],
                x, y, h_n, h_em, DARK, RED, max_w=W-160, line_h=62)
    y += 40
    body_fnt = f('sans-reg', 24)
    p1 = 'В России работают длинные отношения с микро- и nano-экспертами: врач с каналом 3–10 тыс. подписчиков, медицинский журналист, специалист по нутрициологии.'
    p2 = 'Аудитория узкая, но горячая: 60–80% подписчиков — целевые. Стоимость интеграции — 30–80 тыс. ₽, окупаемость с первых пациентов.'
    for p in [p1, p2]:
        lines = wrap(d, p, body_fnt, W-160)
        y = draw_lines(d, lines, x, y, body_fnt, GRAY_TEXT, 36); y += 24
    footer_light(img)
    save(img, 'c04-s2-news.jpg')

def c04_s3_mech():
    img = Image.new('RGB', (W, H), BG_VEB)
    d = ImageDraw.Draw(img)
    header_light(img, '03 / 05')
    x, y = 80, 220
    eyebrow(d, 'ГЛАВНЫЙ СДВИГ 2026', x, y, size=16); y += 62
    h_n = f('sans-bold', 56)
    h_em = f('serif-bold-it', 56)
    y = draw_em(d, [('От «закупки» —', False), (' к «выращиванию»', True)],
                x, y, h_n, h_em, DARK, RED, max_w=W-160, line_h=68)
    y += 40
    body_fnt = f('sans-reg', 24)
    p1 = '64% маркетологов в РФ увеличивают долю бюджета на работу с собственными врачами клиники, а не на покупку рекламы у внешних.'
    p2 = 'Логика простая: внешний инфлюенсер уйдёт в другую клинику, собственный врач — это капитал, привязанный к юрлицу.'
    for p in [p1, p2]:
        lines = wrap(d, p, body_fnt, W-160)
        y = draw_lines(d, lines, x, y, body_fnt, GRAY_TEXT, 36); y += 24

    py = y + 10; pull_h = 150
    d.rectangle([(x, py), (W-80, py+pull_h)], fill=BG_CARD)
    d.rectangle([(x, py), (x+5, py+pull_h)], fill=RED)
    pull_fnt = f('sans-bold', 23)
    pull_lines = wrap(d, 'Прогноз ARDA: к концу 2026 доля бюджета клиник на работу с врачами-экспертами вырастет с 14% до 25–30%.', pull_fnt, W-160-40)
    draw_lines(d, pull_lines, x+25, py+22, pull_fnt, DARK, 32)
    footer_light(img)
    save(img, 'c04-s3-mech.jpg')

def c04_s4_clinic():
    landing_slide(
        filename='c04-s4-clinic.jpg', page='04 / 05', news_n='04',
        audience='Многопрофильная клиника',
        headline_parts=[('Программа', False), (' «Медиа-врач» ', True), ('на 12 месяцев', False)],
        bullets=[
            [('Выбрать ', False), ('2 врачей', True), (' с потенциалом — общительные, любят преподавать, есть тема', False)],
            [('Контент: ', False), ('1 ролик в неделю в VK Видео', True), (' + 2 поста в Telegram + 1 разбор кейса в Дзен в месяц', False)],
            [('Бюджет — ', False), ('80–120 тыс. ₽ в месяц', True), (' на врача (продакшн + СММ)', False)],
            [('Измерять рост подписчиков и количество ', False), ('прямых обращений', True), (' «я к врачу из канала»', False)],
        ],
        cta='Свайпни → стоматологический угол',
        tag_color=RED,
    )

def c04_s5_dental():
    landing_slide(
        filename='c04-s5-dental.jpg', page='05 / 05', news_n='04',
        audience='Стоматология',
        headline_parts=[('Имплантолог + ортодонт =', False), (' 2 медиа-актива', True)],
        bullets=[
            [('В клинике обычно ', False), ('1–2 «технологичных»', True), (' направления: имплантация, элайнеры', False)],
            [('Идеальный материал для медиа: ', False), ('«до/после», большой средний чек, длинный цикл сделки', True)],
            [('Канал имплантолога ', False), ('окупает себя за 3–4 месяца', True), (' через 1–2 продажи плана', False)],
            [('Снимать: разборы кейсов, ответы на страхи, процессы. ', False), ('Не рекламу — экспертный контент для AI', True)],
        ],
        cta='Конец карусели · Дальше — Max, Avito, Urban Ads',
        tag_color=DARK,
    )

# ════════════════════════════════════════════════════════════════════
# CAROUSEL 05 — 3 канала
# ════════════════════════════════════════════════════════════════════

def c05_s1_cover():
    img = Image.new('RGB', (W, H), DARK)
    d = ImageDraw.Draw(img)
    header_dark(img, '01 / 05')

    eyebrow(d, 'НОВОСТЬ 05 · НОВЫЕ ПОВЕРХНОСТИ РФ · 2026', 80, 180, bg=RED, fg=LIGHT, size=17)

    # триптих
    card_w, card_h = 280, 280; gap = 20
    total_w = card_w*3 + gap*2
    sx = (W - total_w)//2; y0 = 320

    cards = [
        ('M', MAX_PURPLE, 'MAX', 'мессенджер VK'),
        ('A', AVITO_GRN,  'AVITO',  'классифайд'),
        ('Я', YANDEX,     'URBAN ADS', 'геотаргет'),
    ]

    for i, (letter, color, title, sub) in enumerate(cards):
        x = sx + i*(card_w + gap)
        d.rounded_rectangle([(x, y0), (x+card_w, y0+card_h)], radius=24, fill=color)
        big_fnt = f('sans-bold', 220)
        bb = d.textbbox((0,0), letter, font=big_fnt)
        twd = bb[2]-bb[0]; thd = bb[3]-bb[1]
        d.text((x + (card_w-twd)//2, y0 + (card_h-thd)//2 - 30), letter, font=big_fnt, fill=LIGHT)
        title_fnt = f('sans-bold', 24)
        sub_fnt = f('sans-reg', 18)
        bb = d.textbbox((0,0), title, font=title_fnt); twd = bb[2]-bb[0]
        d.text((x + (card_w-twd)//2, y0 + card_h + 22), title, font=title_fnt, fill=LIGHT)
        bb = d.textbbox((0,0), sub, font=sub_fnt); twd = bb[2]-bb[0]
        d.text((x + (card_w-twd)//2, y0 + card_h + 56), sub, font=sub_fnt, fill=GRAY)

    # Stat — only "3", with word "канала" smaller below
    big_fnt = f('serif-bold-it', 220)
    txt = '3'
    bb = d.textbbox((0,0), txt, font=big_fnt); twd = bb[2]-bb[0]
    sx_stat = 100
    d.text((sx_stat, 720), txt, font=big_fnt, fill=LIGHT)
    word_fnt = f('serif-bold-it', 80)
    d.text((sx_stat + twd + 20, 850), 'канала', font=word_fnt, fill=RED_BRIGHT)

    # Headline
    h_n = f('sans-bold', 48)
    h_em = f('serif-bold-it', 48)
    draw_em(d, [('Новые рекламные', False), (' поверхности ', True), ('РФ', False)],
            80, 1020, h_n, h_em, LIGHT, RED_BRIGHT, max_w=W-160, line_h=58)

    # sub
    sub_fnt = f('sans-reg', 22)
    d.text((80, 1170), 'К концу 2026 — до 22% бюджетов клиник', font=sub_fnt, fill=(200,200,200))

    footer_dark(img)
    save(img, 'c05-s1-cover.jpg')

def c05_s2_news():
    img = Image.new('RGB', (W, H), LIGHT)
    d = ImageDraw.Draw(img)
    header_light(img, '02 / 05')
    x, y = 80, 220
    eyebrow(d, 'КТО ЗА ЧТО ОТВЕЧАЕТ', x, y, size=16); y += 62
    h_n = f('sans-bold', 50)
    h_em = f('serif-bold-it', 50)
    y = draw_em(d, [('Три', False), (' разные ', True), ('логики, не «всё одинаковое»', False)],
                x, y, h_n, h_em, DARK, RED, max_w=W-160, line_h=62)
    y += 40
    body_fnt = f('sans-reg', 23)
    body_b = f('sans-bold', 23)
    # MAX
    d.text((x, y), 'Max от VK', font=body_b, fill=DARK); y += 32
    p1 = 'Мессенджер с 50+ млн пользователей, реклама в каналах и сервисах. Стоимость показа в 1,8× ниже VK Видео. Аудитория — родители и регионы.'
    lines = wrap(d, p1, body_fnt, W-160); y = draw_lines(d, lines, x, y, body_fnt, GRAY_TEXT, 33); y += 22
    # AVITO
    d.text((x, y), 'Avito Ads', font=body_b, fill=DARK); y += 32
    p2 = 'Рекламная выручка +41% YoY. Пользователь приходит с готовым намерением: «ищу стоматолога рядом».'
    lines = wrap(d, p2, body_fnt, W-160); y = draw_lines(d, lines, x, y, body_fnt, GRAY_TEXT, 33); y += 22
    footer_light(img)
    save(img, 'c05-s2-news.jpg')

def c05_s3_mech():
    img = Image.new('RGB', (W, H), BG_VEB)
    d = ImageDraw.Draw(img)
    header_light(img, '03 / 05')
    x, y = 80, 220
    eyebrow(d, 'ГЛАВНЫЙ НЕДООЦЕНЁННЫЙ КАНАЛ', x, y, size=15); y += 62
    h_n = f('sans-bold', 50)
    h_em = f('serif-bold-it', 50)
    y = draw_em(d, [('Яндекс', False), (' Urban Ads ', True), ('— реклама в Драйве, Такси, Самокатах, Лавке', False)],
                x, y, h_n, h_em, DARK, RED, max_w=W-160, line_h=62)
    y += 36
    body_fnt = f('sans-reg', 24)
    p1 = 'Главная ценность — точечный геотаргет: показать рекламу клиники только тем, кто проезжает в радиусе 1 км или зашёл в Лавку в районе.'
    p2 = 'Сценарий «реклама человеку, который сейчас находится рядом и может зайти». Конверсия в визит — в разы выше performance-каналов.'
    for p in [p1, p2]:
        lines = wrap(d, p, body_fnt, W-160)
        y = draw_lines(d, lines, x, y, body_fnt, GRAY_TEXT, 36); y += 22

    py = y + 10; pull_h = 130
    d.rectangle([(x, py), (W-80, py+pull_h)], fill=BG_CARD)
    d.rectangle([(x, py), (x+5, py+pull_h)], fill=RED)
    pull_fnt = f('sans-bold', 23)
    pull_lines = wrap(d, 'Стоматология срочной помощи, аллерголог, ЛОР — категории, где Urban Ads даёт лучшую конверсию.', pull_fnt, W-160-40)
    draw_lines(d, pull_lines, x+25, py+22, pull_fnt, DARK, 32)
    footer_light(img)
    save(img, 'c05-s3-mech.jpg')

def c05_s4_clinic():
    landing_slide(
        filename='c05-s4-clinic.jpg', page='04 / 05', news_n='05',
        audience='Многопрофильная клиника',
        headline_parts=[('Геотаргет', False), (' вместо ', True), ('общего охвата', False)],
        bullets=[
            [('Тест в ', False), ('Яндекс Urban Ads', True), (' с геотаргетом на радиус 2 км вокруг клиники', False)],
            [('Креатив — узкий: ', False), ('один врач, одна услуга, один оффер', True), (' («Терапевт за 2 часа от 2 500 ₽»)', False)],
            [('Сравнить ', False), ('cost-per-visit', True), (' с Яндекс.Директом за тот же бюджет', False)],
            [('В ', False), ('Avito Ads', True), (' — разместить услуги клиники с фото врача и реальной ценой', False)],
        ],
        cta='Свайпни → стоматологический угол',
        tag_color=RED,
    )

def c05_s5_dental():
    landing_slide(
        filename='c05-s5-dental.jpg', page='05 / 05', news_n='05',
        audience='Стоматология',
        headline_parts=[('Острая боль —', False), (' Urban Ads. ', True), ('Имплантация — Max', False)],
        bullets=[
            [('«Острые» обращения ', False), ('(острая боль, скол коронки)', True), (' — идеальный кандидат для Urban Ads', False)],
            [('Геотаргет 3 км + ', False), ('«Принимаем сегодня в течение 2 часов»', True), (' = высокая конверсия в визит', False)],
            [('Для ', False), ('имплантологии', True), (' — Max-каналы клиники с длинным контентом и прогревом', False)],
            [('30-дневный пилот на ', False), ('Avito с услугой «Чистка + осмотр от 2 990 ₽»', True), (' — типичная «дверь в клинику»', False)],
        ],
        cta='Конец дайджеста · @insightsmedia · 04.05.2026',
        tag_color=DARK,
    )


# ────────────────────────────────────────────────────────────────────
def main():
    funcs = [
        c01_s1_cover, c01_s2_news, c01_s3_mech, c01_s4_clinic, c01_s5_dental,
        c02_s1_cover, c02_s2_news, c02_s3_mech, c02_s4_clinic, c02_s5_dental,
        c03_s1_cover, c03_s2_news, c03_s3_mech, c03_s4_clinic, c03_s5_dental,
        c04_s1_cover, c04_s2_news, c04_s3_mech, c04_s4_clinic, c04_s5_dental,
        c05_s1_cover, c05_s2_news, c05_s3_mech, c05_s4_clinic, c05_s5_dental,
    ]
    for fn in funcs:
        fn()
    print(f'\nГотово. {len(funcs)} слайдов сохранены в: {OUT_DIR}')

if __name__ == '__main__':
    main()
