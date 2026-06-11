#!/usr/bin/env python3
"""
update_programmation.py

Télécharge le Google Doc de programmation (export HTML), en extrait le tableau,
et régénère programmation.html avec les deux vues (desktop + mobile).

Usage :
    py -3 scripts/update_programmation.py
    # ou
    python3 scripts/update_programmation.py

Nécessite : Python 3.6+ (stdlib uniquement)
"""

import urllib.request
import re
import html as html_module
import os
import sys

# ── Configuration ────────────────────────────────────────────────────────────

GOOGLE_DOC_ID = "1iXZjXpH8-j4PTD1x4FjOXIbGm1VlK3Dp1ajanU1_FRc"
EXPORT_URL = f"https://docs.google.com/document/d/{GOOGLE_DOC_ID}/export?format=html"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "programmation.html")

WEEKDAYS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
WEEKDAY_SHORT = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# Couleurs de header mobile par semaine
WEEK_HEADER_COLORS = [
    ("#B55A40", "#fff"),   # semaine 1
    ("#1A6B8C", "#fff"),   # semaine 2
    ("#2E7D32", "#fff"),   # semaine 3
    ("#B8860B", "#fff"),   # semaine 4
    ("#6B4C7A", "#fff"),   # semaine 5
    ("#8B4513", "#fff"),   # semaine 6 (secours)
]

# Classification des événements
CLASS_RULES = [
    (
        ["académie", "résidence", "béryl", "apprentissage mutuel"],
        "ev-residence",
    ),
    (
        ["jeux de plateau", "jeux de rôles", "jeu de rôle", "loup-garou"],
        "ev-jeu",
    ),
    (
        ["ouverture", "ouvert"],
        "ev-ouverture",
    ),
    (
        [
            "chorale",
            "théâtre",
            "dessin",
            "jam",
            "afrovibe",
            "circle song",
            "chant",
            "modèle vivant",
            "forum",
        ],
        "ev-artistique",
    ),
]

SPECIAL_KEYWORDS = [
    "soirée critique",
    "arpentage",
    "docu blast",
    "prépa pancartes",
    "pride",
]

KNOWN_NAMES = {
    "cécile",
    "morgane",
    "blaise",
    "kérim",
    "béryl",
    "laurie",
    "vera",
    "salvina",
    "sarah",
}

TIME_RE = re.compile(r"^\d{1,2}\s*[hH]\s*\d{0,2}")
TIME_SEARCH_RE = re.compile(r"\d{1,2}\s*[hH]\s*\d{0,2}")


def classify_event(text: str) -> str:
    t = text.lower()
    for keywords, cls in CLASS_RULES:
        if any(k in t for k in keywords):
            return cls
    if any(k in t for k in SPECIAL_KEYWORDS):
        return "ev-special"
    return "ev-special"


def split_cell_events(lines):
    """
    Reçoit une liste de lignes de texte (une par <p>/<li> de la cellule)
    et renvoie une liste d’événements (strings).
    """
    if not lines:
        return []

    # Retirer le numéro de jour s’il est seul en première ligne
    if lines[0].isdigit():
        lines = lines[1:]
    if not lines:
        return []

    events = []
    current = [lines[0]]
    current_has_time = bool(TIME_SEARCH_RE.search(lines[0]))
    current_count = 1

    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        starts_with_time = bool(TIME_RE.match(line))
        line_words = line.split()
        line_len = len(line_words)
        line_starts_upper = line[0].isupper() if line else False

        prev = current[-1]
        prev_words = prev.split()
        prev_last = prev_words[-1].lower().rstrip(".,;:!?") if prev_words else ""
        prev_short = len(prev) < 20 and len(prev_words) <= 2
        prev_ends_name = prev_last in KNOWN_NAMES
        prev_has_time = bool(TIME_SEARCH_RE.search(prev))

        is_new = False
        # 1) heure en début de ligne + événement actuel déjà “rempli”
        if starts_with_time and (current_has_time or current_count > 1):
            is_new = True
        # 2) ligne précédente courte + ligne actuelle substantielle + majuscule
        elif prev_short and line_len >= 2 and line_starts_upper:
            # Exception : si l’événement actuel n’a qu’une ligne et que c’est une heure,
            # c’est un début, pas une fin → ne pas couper
            if not (current_count == 1 and TIME_RE.match(current[0])):
                is_new = True
        # 3) ligne précédente se termine par un prénom connu + ligne actuelle substantielle + majuscule
        elif prev_ends_name and line_len >= 2 and line_starts_upper:
            is_new = True

        if is_new:
            events.append(" ".join(current))
            current = [line]
            current_has_time = bool(TIME_SEARCH_RE.search(line))
            current_count = 1
        else:
            current.append(line)
            current_has_time = current_has_time or bool(TIME_SEARCH_RE.search(line))
            current_count += 1

    events.append(" ".join(current))
    return events


def parse_google_doc():
    """
    Télécharge le Google Doc en HTML, extrait le titre et le tableau,
    renvoie (month_year, weeks).
    weeks = liste de semaines, chaque semaine = liste de jours,
    chaque jour = dict {day, weekday, events}.
    """
    req = urllib.request.Request(EXPORT_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode("utf-8")

    # Nettoyer styles/scripts
    raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", raw, flags=re.DOTALL)

    # Extraire le mois/année depuis le titre
    month_year = "Programmation"
    m = re.search(
        r"-\s*([A-Za-zûéèêàçô\s]+\d{4})", html_module.unescape(raw)
    )
    if m:
        month_year = m.group(1).strip()
        # Normaliser la casse : première lettre majuscule
        parts = month_year.split()
        if parts:
            parts[0] = parts[0].capitalize()
            month_year = " ".join(parts)

    # Extraire le tableau
    table_m = re.search(r"<table[^>]*>(.*?)</table>", raw, re.DOTALL)
    if not table_m:
        raise ValueError("Tableau non trouvé dans le document Google.")

    table_html = table_m.group(1)

    rows = []
    for tr_m in re.finditer(r"<tr[^>]*>(.*?)</tr>", table_html, re.DOTALL):
        tr = tr_m.group(1)
        cells = []
        for td_m in re.finditer(r"<td[^>]*>(.*?)</td>", tr, re.DOTALL):
            td = td_m.group(1)
            # Extraire le texte de chaque <p>, <span>, <li>
            lines = []
            for p_m in re.finditer(r"<p[^>]*>(.*?)</p>", td, re.DOTALL):
                p = p_m.group(1)
                # Enlever toutes les balises internes
                txt = re.sub(r"<[^>]+>", " ", p)
                txt = html_module.unescape(txt)
                txt = " ".join(txt.split())
                if txt:
                    lines.append(txt)
            # Gérer aussi les <li> éventuels
            for li_m in re.finditer(r"<li[^>]*>(.*?)</li>", td, re.DOTALL):
                li = li_m.group(1)
                txt = re.sub(r"<[^>]+>", " ", li)
                txt = html_module.unescape(txt)
                txt = " ".join(txt.split())
                if txt:
                    lines.append(txt)
            cells.append(lines)
        rows.append(cells)

    if not rows:
        raise ValueError("Aucune ligne dans le tableau.")

    # Première ligne = header
    data_rows = rows[1:]

    weeks = []
    for row in data_rows:
        week = []
        for col_idx, lines in enumerate(row):
            if not lines:
                continue
            # La première ligne doit être un jour (1-31)
            first = lines[0].strip()
            if first.isdigit() and 1 <= int(first) <= 31:
                day_num = int(first)
                events = split_cell_events(lines)
                if events or day_num:
                    week.append(
                        {
                            "day": day_num,
                            "weekday": WEEKDAYS[col_idx],
                            "events": events,
                        }
                    )
        if week:
            weeks.append(week)

    return month_year, weeks


def generate_html(month_year, weeks):
    """Génère le HTML complet de programmation.html."""

    # ── Desktop calendar ───────────────────────────────────────────────────
    desktop_rows = []
    for week in weeks:
        cells = []
        # On construit 7 colonnes
        day_map = {day["weekday"]: day for day in week}
        for wd in WEEKDAYS:
            if wd in day_map:
                d = day_map[wd]
                ev_html = "\n".join(
                    f'                <span class="event {classify_event(ev)}">{ev}</span>'
                    for ev in d["events"]
                )
                cells.append(
                    f"""              <td>
                <div class="day-num">{d["day"]}</div>
{ev_html}
              </td>"""
                )
            else:
                cells.append(
                    '              <td class="empty">\n                <div class="day-num"></div>\n              </td>'
                )
        desktop_rows.append("            <tr>\n" + "\n".join(cells) + "\n            </tr>")

    desktop_html = "\n".join(desktop_rows)

    # ── Mobile calendar ────────────────────────────────────────────────────
    mobile_parts = []
    for w_idx, week in enumerate(weeks, start=1):
        # Séparateur de semaine (sauf avant la première)
        if w_idx > 1:
            mobile_parts.append(
                f'          <div class="week-separator"><span>Semaine {w_idx}</span></div>'
            )

        # Banner résidence (si la semaine contient des résidences)
        res_days = [d for d in week if any(classify_event(ev) == "ev-residence" for ev in d["events"])]
        if res_days:
            first_r = res_days[0]["day"]
            last_r = res_days[-1]["day"]
            mobile_parts.append(
                f'          <div class="residence-banner">📅 {first_r}–{last_r} juin : Résidence « Académie libre et éclairé » (Béryl)</div>'
            )

        for d in week:
            if not d["events"]:
                continue
            ev_html = "\n".join(
                f'              <span class="event {classify_event(ev)}">{ev}</span>'
                for ev in d["events"]
            )
            month_name = month_year.split()[0]  # ex: "Juin"
            mobile_parts.append(
                f"""          <div class="mobile-day mobile-week-{w_idx}">
            <div class="mobile-day-header"><span class="mobile-day-name">{d["weekday"]}</span> <span class="mobile-day-date">{d["day"]} {month_name.lower()}</span></div>
            <div class="mobile-day-body">
{ev_html}
            </div>
          </div>"""
            )

    mobile_html = "\n".join(mobile_parts)

    # ── Legend ─────────────────────────────────────────────────────────────
    # Détecter les classes présentes ce mois-ci
    present_classes = set()
    for week in weeks:
        for d in week:
            for ev in d["events"]:
                present_classes.add(classify_event(ev))

    legend_items = []
    if "ev-special" in present_classes:
        legend_items.append(
            '<div class="legend-item"><div class="legend-dot" style="background: var(--sky);"></div> Événements</div>'
        )
    if "ev-jeu" in present_classes:
        legend_items.append(
            '<div class="legend-item"><div class="legend-dot" style="background: var(--mint);"></div> Jeux</div>'
        )
    if "ev-artistique" in present_classes:
        legend_items.append(
            '<div class="legend-item"><div class="legend-dot" style="background: #D4A373;"></div> Artistique</div>'
        )
    if "ev-residence" in present_classes:
        legend_items.append(
            '<div class="legend-item"><div class="legend-dot" style="background: #9B8CB8;"></div> Résidence Académie libre et éclairé</div>'
        )

    legend_html = "\n          ".join(legend_items)
    if legend_html:
        legend_html += '\n          <div class="legend-note">Ateliers, boissons et nourriture sont à prix libre !</div>'

    # ── CSS dynamique pour les semaines mobile ────────────────────────────
    num_weeks = len(weeks)
    week_css = ""
    for i in range(1, num_weeks + 1):
        bg, fg = WEEK_HEADER_COLORS[(i - 1) % len(WEEK_HEADER_COLORS)]
        week_css += f"""
    .mobile-week-{i} .mobile-day-header {{ background: {bg}; }}
    .mobile-week-{i} .mobile-day-header,
    .mobile-week-{i} .mobile-day-header .mobile-day-name,
    .mobile-week-{i} .mobile-day-header .mobile-day-date {{ color: {fg}; }}"""

    # ── Assemblage final ───────────────────────────────────────────────────
    html_out = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Programmation {month_year} — KiCaféÇa</title>
  <meta name="description" content="Calendrier des activités et événements du KiCaféÇa à Joyeuse pour le mois de {month_year.lower()}.">
  <meta name="author" content="KiCaféÇa">
  <meta name="keywords" content="kicafeca, programme, calendrier, {month_year.lower()}, ateliers, événements, joyeuse, ardèche">

  <!-- Open Graph / Social Media -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="Programmation {month_year} — KiCaféÇa">
  <meta property="og:description" content="Calendrier des activités et événements du mois de {month_year.lower()}.">
  <meta property="og:url" content="https://www.kicafeca.fr/programmation.html">
  <meta property="og:image" content="https://www.kicafeca.fr/images/Logo.png">
  <meta property="og:image:width" content="1970">
  <meta property="og:image:height" content="2190">

  <!-- Favicon -->
  <link rel="icon" href="images/favicon.ico">
  <link rel="apple-touch-icon" href="images/Logo.png">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@400;500;600;700&family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <div id="header-placeholder"></div>
  <script src="js/components.js"></script>

  <!-- Hero Section -->
  <section class="programmation-hero">
    <div class="container">
      <h1 class="section-title">Programmation {month_year}</h1>
      <p class="section-subtitle">Ateliers, conférences, jeux et événements spéciaux</p>
    </div>
  </section>

  <!-- Calendar Section -->
  <section class="programmation-calendar">
    <div class="container">
      <div class="calendar-container">
        <!-- Header with logo and title -->
        <div class="calendar-header">
          <img src="images/Logo.png" alt="KiCaféÇa" class="calendar-logo">
          <div class="calendar-title">
            <h1>Programmation {month_year}</h1>
            <p>KiCaféÇa &middot; Joyeuse, Ardèche</p>
          </div>
        </div>

        <!-- Desktop Calendar -->
        <div class="calendar-desktop">
        <table class="calendar-grid">
          <thead>
            <tr>
              <th>Lundi</th>
              <th>Mardi</th>
              <th>Mercredi</th>
              <th>Jeudi</th>
              <th>Vendredi</th>
              <th>Samedi</th>
              <th>Dimanche</th>
            </tr>
          </thead>
          <tbody>
{desktop_html}
          </tbody>
        </table>
        </div>

        <!-- Mobile Calendar -->
        <div class="calendar-mobile">
{mobile_html}
        </div>

        <!-- Legend -->
        <div class="calendar-legend">
          {legend_html}
        </div>
      </div>
    </div>
  </section>

  <div id="footer-placeholder"></div>
  <script src="js/main.js"></script>
  <script>
    /* Surbrillance du jour actuel */
    (function() {{
      var today = new Date();
      var dayNum = today.getDate();
      var month = today.getMonth();
      var year = today.getFullYear();

      /* Détection du mois courant depuis le titre */
      var monthMatch = document.querySelector('.section-title').textContent.match(/([A-Za-zûéèêàçô]+)\\s+(\\d{{4}})/);
      if (monthMatch) {{
        var monthNames = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"];
        var docMonth = monthNames.indexOf(monthMatch[1].toLowerCase());
        var docYear = parseInt(monthMatch[2], 10);
        if (docMonth === month && docYear === year) {{
          /* Desktop */
          document.querySelectorAll('.calendar-grid tbody td').forEach(function(td) {{
            var numDiv = td.querySelector('.day-num');
            if (numDiv && parseInt(numDiv.textContent, 10) === dayNum) {{
              td.classList.add('today');
            }}
          }});
          /* Mobile */
          document.querySelectorAll('.mobile-day').forEach(function(day) {{
            var dateSpan = day.querySelector('.mobile-day-date');
            if (dateSpan) {{
              var m = dateSpan.textContent.match(/(\\d+)\\s+([a-zûéèêàçô]+)/i);
              if (m) {{
                var d = parseInt(m[1], 10);
                var mn = monthNames.indexOf(m[2].toLowerCase());
                if (d === dayNum && mn === month) {{
                  day.classList.add('today');
                }}
              }}
            }}
          }});
        }}
      }}
    }})();
  </script>
  <style>
    /* Couleur semaine mobile — header coloré selon la semaine */
{week_css}

    /* Surbrillance jour actuel */
    .calendar-grid tbody td.today {{
      box-shadow: inset 0 0 0 3px var(--terracotta);
      background: #fff5f0 !important;
    }}
    .calendar-grid tbody td.today .day-num {{
      color: var(--terracotta);
      font-size: 1.35rem;
    }}
    .mobile-day.today {{
      box-shadow: inset 0 0 0 2px var(--terracotta);
      background: #fff5f0;
    }}
    .mobile-day.today .mobile-day-header {{
      background: var(--terracotta);
      color: #fff;
      border-radius: 8px 8px 0 0;
    }}
    .mobile-day.today .mobile-day-header .mobile-day-name,
    .mobile-day.today .mobile-day-header .mobile-day-date {{
      color: #fff;
    }}

    /* Couleur artistique */
    .ev-artistique {{
      background: #D4A373;
      color: #fff;
    }}

    /* Résidence Académie */
    .ev-residence {{
      background: #9B8CB8;
      color: #fff;
    }}
    .residence-banner {{
      background: #9B8CB8;
      color: #fff;
      text-align: center;
      padding: 10px 14px;
      border-radius: 10px;
      margin: 8px 0 12px 0;
      font-weight: 600;
      font-size: 0.95rem;
    }}
  </style>
</body>
</html>
"""
    return html_out


def main():
    print("[DOWNLOAD] Telechargement du Google Doc...")
    month_year, weeks = parse_google_doc()
    print(f"[INFO] Mois detecte : {month_year}")
    print(f"[INFO] Semaines trouvees : {len(weeks)}")
    total_events = sum(len(d["events"]) for w in weeks for d in w)
    print(f"[INFO] Evenements trouves : {total_events}")

    html_content = generate_html(month_year, weeks)
    out_path = os.path.abspath(OUTPUT_FILE)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[OK] Fichier genere : {out_path}")


if __name__ == "__main__":
    main()
