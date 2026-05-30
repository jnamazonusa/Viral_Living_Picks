#!/usr/bin/env python3
"""
generate_page.py
products.json을 읽어서 index.html을 자동 생성합니다.
사용법: python generate_page.py
"""

import json
from datetime import datetime

def load_products(path="products.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def render_stars(rating):
    full = int(rating)
    has_half = (rating - full) >= 0.5
    stars = "★" * full
    if has_half:
        stars += "½"
    return stars

def render_product_card(p):
    tag_html = f'<span class="tag">{p["tag"]}</span>' if p.get("tag") else ""
    stars = render_stars(p["rating"])
    return f"""
    <a class="card" href="{p['affiliate_url']}" target="_blank" rel="noopener" data-category="{p['category']}">
      <div class="card-img-wrap">
        <img src="{p['image_url']}" alt="{p['title']}" loading="lazy" onerror="this.style.display='none'">
        {tag_html}
      </div>
      <div class="card-body">
        <span class="category-badge">{p['category']}</span>
        <h3 class="card-title">{p['title']}</h3>
        <p class="card-desc">{p['description']}</p>
        <div class="card-meta">
          <span class="stars">{stars}</span>
          <span class="rating-num">{p['rating']}</span>
          <span class="review-count">({p['review_count']:,})</span>
        </div>
        <div class="card-footer">
          <span class="cta">Check on Amazon →</span>
        </div>
      </div>
    </a>"""

def get_categories(products):
    cats = ["전체"]
    seen = set()
    for p in products:
        c = p["category"]
        if c not in seen:
            cats.append(c)
            seen.add(c)
    return cats

def generate_html(data):
    site = data["site"]
    products = data["products"]
    categories = get_categories(products)
    
    cards_html = "\n".join(render_product_card(p) for p in products)
    
    cat_buttons = "\n".join(
        f'<button class="filter-btn{"active" if c == "전체" else ""}" data-filter="{c}">{c}</button>'
        for c in categories
    )

    updated = datetime.now().strftime("%Y.%m.%d 업데이트")

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{site['title']} — {site['handle']}</title>
  <meta property="og:title" content="{site['title']}">
  <meta property="og:description" content="{site['bio']}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #f7f7f5;
      --bg2: #ffffff;
      --bg3: #efefed;
      --border: rgba(0,0,0,0.08);
      --border2: rgba(0,0,0,0.15);
      --text: #111111;
      --text2: #777777;
      --accent: #FF6B35;
      --accent-dim: #FF6B3512;
      --radius: 12px;
      --font-mono: 'Space Mono', monospace;
      --font-sans: 'DM Sans', sans-serif;
    }}
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-sans);
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }}

    /* ── 헤더 ── */
    .header {{
      text-align: center;
      padding: 60px 24px 40px;
      position: relative;
    }}
    .header::after {{
      content: '';
      display: block;
      width: 60px;
      height: 2px;
      background: var(--accent);
      margin: 0 auto;
      margin-top: 32px;
    }}
    .handle {{
      font-family: var(--font-mono);
      font-size: 13px;
      color: var(--accent);
      letter-spacing: 0.12em;
      text-transform: uppercase;
      margin-bottom: 12px;
    }}
    .site-title {{
      font-family: var(--font-mono);
      font-size: clamp(32px, 8vw, 56px);
      font-weight: 700;
      letter-spacing: -0.02em;
      line-height: 1;
    }}
    .site-bio {{
      margin-top: 14px;
      font-size: 14px;
      color: var(--text2);
      font-weight: 300;
    }}
    .updated {{
      margin-top: 8px;
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--text2);
      opacity: 0.5;
    }}

    /* ── 필터 ── */
    .filter-wrap {{
      display: flex;
      gap: 8px;
      justify-content: center;
      flex-wrap: wrap;
      padding: 0 24px 32px;
    }}
    .filter-btn {{
      font-family: var(--font-mono);
      font-size: 12px;
      padding: 7px 16px;
      border: 1px solid var(--border2);
      border-radius: 100px;
      background: transparent;
      color: var(--text2);
      cursor: pointer;
      transition: all 0.2s;
      letter-spacing: 0.05em;
    }}
    .filter-btn:hover {{ border-color: var(--accent); color: var(--accent); }}
    .filter-btn.active {{
      background: var(--accent);
      border-color: var(--accent);
      color: #fff;
      font-weight: 700;
    }}

    /* ── 그리드 ── */
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
      padding: 0 24px 80px;
      max-width: 1100px;
      margin: 0 auto;
    }}

    /* ── 카드 ── */
    .card {{
      display: flex;
      flex-direction: column;
      background: var(--bg2);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow: hidden;
      text-decoration: none;
      color: inherit;
      transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }}
    .card:hover {{
      transform: translateY(-4px);
      border-color: var(--accent);
      box-shadow: 0 8px 32px rgba(0,0,0,0.10);
    }}
    .card.hidden {{ display: none; }}

    .card-img-wrap {{
      position: relative;
      background: #fff;
      aspect-ratio: 1;
      overflow: hidden;
    }}
    .card-img-wrap img {{
      width: 100%;
      height: 100%;
      object-fit: contain;
      padding: 12px;
      transition: transform 0.3s ease;
    }}
    .card:hover .card-img-wrap img {{ transform: scale(1.04); }}

    .tag {{
      position: absolute;
      top: 10px;
      left: 10px;
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 700;
      background: var(--accent);
      color: #fff;
      padding: 4px 8px;
      border-radius: 4px;
      letter-spacing: 0.05em;
    }}

    .card-body {{
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      flex: 1;
    }}
    .category-badge {{
      font-family: var(--font-mono);
      font-size: 10px;
      color: var(--accent);
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }}
    .card-title {{
      font-size: 14px;
      font-weight: 500;
      line-height: 1.5;
      color: var(--text);
    }}
    .card-desc {{
      font-size: 12px;
      color: var(--text2);
      line-height: 1.6;
    }}
    .card-meta {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
    }}
    .stars {{ color: var(--accent); font-size: 13px; }}
    .rating-num {{ color: var(--text); font-weight: 500; }}
    .review-count {{ color: var(--text2); }}

    .card-footer {{
      margin-top: auto;
      padding-top: 12px;
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .price {{
      font-family: var(--font-mono);
      font-size: 15px;
      font-weight: 700;
      color: var(--text);
    }}
    .cta {{
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--accent);
      letter-spacing: 0.05em;
    }}

    /* ── 푸터 ── */
    footer {{
      text-align: center;
      padding: 32px 24px;
      border-top: 1px solid var(--border);
      font-size: 11px;
      color: var(--text2);
      font-family: var(--font-mono);
      line-height: 1.8;
    }}
    footer a {{ color: var(--accent); text-decoration: none; font-weight: 500; }}

    @media (max-width: 600px) {{
      .grid {{ grid-template-columns: 1fr 1fr; gap: 10px; padding: 0 12px 60px; }}
      .card-body {{ padding: 12px; }}
    }}
  </style>
</head>
<body>
  <header class="header">
    <p class="handle">{site['handle']}</p>
    <h1 class="site-title">{site['title']}</h1>
    <p class="site-bio">{site['bio']}</p>
    <p class="updated">{updated}</p>
  </header>

  <nav class="filter-wrap">
    {cat_buttons}
  </nav>

  <main class="grid" id="grid">
    {cards_html}
  </main>

  <footer>
    <p>이 페이지의 링크는 아마존 어필리에이트 링크입니다.</p>
    <p>구매 시 추가 비용 없이 소정의 수수료가 지급됩니다.</p>
    <p style="margin-top:8px"><a href="https://www.instagram.com/{site['handle'].replace('@','')}">{site['handle']}</a></p>
  </footer>

  <script>
    const buttons = document.querySelectorAll('.filter-btn');
    const cards   = document.querySelectorAll('.card');

    buttons.forEach(btn => {{
      btn.addEventListener('click', () => {{
        buttons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const f = btn.dataset.filter;
        cards.forEach(c => {{
          c.classList.toggle('hidden', f !== '전체' && c.dataset.category !== f);
        }});
      }});
    }});
  </script>
</body>
</html>"""

if __name__ == "__main__":
    data = load_products("products.json")
    html = generate_html(data)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ index.html 생성 완료! ({len(data['products'])}개 제품)")
    print("📁 GitHub Pages에 index.html + products.json 올리면 됩니다.")
