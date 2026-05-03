"""
Scraper for MDM 2026 conference schedule at marinemilitaryexpos.com
Produces:
  - mdm2026_schedule_raw.json
  - mdm2026_speaker_stage_lookup.csv
"""

import asyncio
import json
import csv
import re
import sys
from playwright.async_api import async_playwright

SCHEDULE_URL = "https://marinemilitaryexpos.com/pme-sessions/"
SPEAKERS_URL = "https://marinemilitaryexpos.com/session-speakers/"

# Expected conference days
DAYS = ["April 28", "April 29", "April 30"]


async def scrape_schedule(page) -> list[dict]:
    print(f"Loading schedule: {SCHEDULE_URL}")
    await page.goto(SCHEDULE_URL, wait_until="domcontentloaded", timeout=60000)
    await page.wait_for_load_state("load", timeout=30000)
    await page.wait_for_timeout(2000)

    # Dump the page HTML for inspection
    html_snippet = await page.content()
    with open("schedule_page_debug.html", "w") as f:
        f.write(html_snippet)
    print(f"  Page title: {await page.title()}")
    print(f"  HTML saved to schedule_page_debug.html ({len(html_snippet)} bytes)")

    sessions = []

    # Find tab elements — try common patterns used by conference sites
    # Pattern 1: anchor/button tabs with day labels
    tab_selectors = [
        "li[role='tab']",
        "a[role='tab']",
        "button[role='tab']",
        ".tab-title a",
        ".tabs-title a",
        ".nav-tab",
        ".fc-tab",
        "[data-tab]",
        ".etn-tab",          # EventOn / tribe-style
        ".tribe-events-tabs a",
        ".tab a",
        ".tabs li a",
    ]

    tabs_found = []
    for sel in tab_selectors:
        tabs = await page.query_selector_all(sel)
        if tabs:
            print(f"  Found {len(tabs)} tab elements with selector: {sel}")
            tabs_found = tabs
            break

    if not tabs_found:
        print("  No tab elements found — will try to read whole page as single day")
        sessions += await extract_sessions_from_page(page, day_label="")
        return sessions

    for i, tab in enumerate(tabs_found):
        tab_text = (await tab.inner_text()).strip()
        print(f"  Clicking tab {i}: '{tab_text}'")
        await tab.click()
        await page.wait_for_timeout(1500)

        day_label = tab_text
        sessions += await extract_sessions_from_page(page, day_label=day_label)

    return sessions


async def extract_sessions_from_page(page, day_label: str) -> list[dict]:
    """
    Try multiple structural patterns to extract sessions from the visible DOM.
    Returns list of session dicts.
    """
    sessions = []

    # --- Pattern A: tribe_events / Modern Tribe schedule tables ---
    # .tribe-events-schedule, .tribe-event-schedule-list
    tribe_sessions = await page.query_selector_all(".tribe-event-schedule-list-item, .type-tribe_events")
    if tribe_sessions:
        print(f"    Found {len(tribe_sessions)} Tribe events")
        for el in tribe_sessions:
            s = await parse_tribe_session(el, day_label)
            if s:
                sessions.append(s)
        return sessions

    # --- Pattern B: EventOn (.etn-*) ---
    evo_sessions = await page.query_selector_all(".etn-event, .eventon_list_event")
    if evo_sessions:
        print(f"    Found {len(evo_sessions)} EventOn events")
        for el in evo_sessions:
            s = await parse_generic_session(el, day_label)
            if s:
                sessions.append(s)
        return sessions

    # --- Pattern C: generic .session / .schedule-session blocks ---
    generic_sessions = await page.query_selector_all(
        ".session, .schedule-session, .conf-session, .wpb_wrapper .session, "
        ".event-item, .schedule-item, .sched-session"
    )
    if generic_sessions:
        print(f"    Found {len(generic_sessions)} generic session blocks")
        for el in generic_sessions:
            s = await parse_generic_session(el, day_label)
            if s:
                sessions.append(s)
        return sessions

    # --- Pattern D: table rows ---
    rows = await page.query_selector_all("table.schedule tr, table.sessions tr")
    if rows:
        print(f"    Found {len(rows)} table rows")
        for row in rows[1:]:  # skip header
            s = await parse_table_row(row, day_label)
            if s:
                sessions.append(s)
        return sessions

    # --- Pattern E: scrape everything visible in structured headings ---
    sessions += await scrape_by_headings(page, day_label)

    return sessions


async def parse_tribe_session(el, day_label: str) -> dict | None:
    try:
        title_el = await el.query_selector(".tribe-event-url, .tribe-events-list-event-title a, h2 a, h3 a")
        title = (await title_el.inner_text()).strip() if title_el else ""

        time_el = await el.query_selector(".tribe-events-schedule abbr, time, .tribe-event-time")
        time_str = (await time_el.inner_text()).strip() if time_el else ""
        if time_el:
            dt = await time_el.get_attribute("title") or ""
            if dt:
                time_str = dt

        venue_el = await el.query_selector(".tribe-venue, .tribe-events-address")
        stage = (await venue_el.inner_text()).strip() if venue_el else ""

        speakers = await extract_speakers(el)

        return {
            "day": day_label,
            "time": time_str,
            "stage": stage,
            "title": title,
            "speakers": speakers,
            "raw_html": await el.inner_html(),
        }
    except Exception as e:
        print(f"    Warning: tribe parse error: {e}")
        return None


async def parse_generic_session(el, day_label: str) -> dict | None:
    try:
        # title
        title_el = await el.query_selector("h1, h2, h3, h4, .session-title, .event-title, .title")
        title = (await title_el.inner_text()).strip() if title_el else (await el.inner_text()).strip()[:120]

        # time
        time_el = await el.query_selector("time, .time, .session-time, .event-time, [class*='time']")
        time_str = ""
        if time_el:
            time_str = (await time_el.inner_text()).strip()
            dt = await time_el.get_attribute("datetime") or await time_el.get_attribute("title") or ""
            if dt:
                time_str = dt

        # stage / room / track
        stage_el = await el.query_selector(".room, .stage, .track, .location, .venue, [class*='room'], [class*='stage'], [class*='track']")
        stage = (await stage_el.inner_text()).strip() if stage_el else ""

        speakers = await extract_speakers(el)

        return {
            "day": day_label,
            "time": time_str,
            "stage": stage,
            "title": title,
            "speakers": speakers,
            "raw_html": await el.inner_html(),
        }
    except Exception as e:
        print(f"    Warning: generic parse error: {e}")
        return None


async def parse_table_row(row, day_label: str) -> dict | None:
    try:
        cells = await row.query_selector_all("td")
        if len(cells) < 2:
            return None
        texts = [((await c.inner_text()).strip()) for c in cells]
        return {
            "day": day_label,
            "time": texts[0] if len(texts) > 0 else "",
            "stage": texts[1] if len(texts) > 1 else "",
            "title": texts[2] if len(texts) > 2 else "",
            "speakers": [texts[3]] if len(texts) > 3 else [],
            "raw_html": await row.inner_html(),
        }
    except Exception as e:
        print(f"    Warning: table row parse error: {e}")
        return None


async def scrape_by_headings(page, day_label: str) -> list[dict]:
    """
    Fallback: walk h2/h3/h4 tags and collect text blocks between them.
    Tries to identify stage/time/speaker patterns via regex.
    """
    sessions = []
    print(f"    Fallback: scraping by headings for day='{day_label}'")

    # Grab all text content from the visible body, structured as lines
    body_text = await page.inner_text("body")
    lines = [l.strip() for l in body_text.splitlines() if l.strip()]

    time_re = re.compile(r'\b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)\b')
    current_stage = ""
    current_time = ""
    current_title = ""
    current_speakers: list[str] = []

    def flush():
        nonlocal current_stage, current_time, current_title, current_speakers
        if current_title:
            sessions.append({
                "day": day_label,
                "time": current_time,
                "stage": current_stage,
                "title": current_title,
                "speakers": list(current_speakers),
            })
        current_title = ""
        current_speakers = []

    stage_keywords = ["stage", "theater", "theatre", "room", "hall", "pavilion", "arena", "track", "lab", "mainstage"]

    for line in lines:
        lower = line.lower()
        is_stage = any(kw in lower for kw in stage_keywords) and len(line) < 80
        has_time = bool(time_re.search(line))

        if is_stage and not has_time:
            flush()
            current_stage = line
            current_time = ""
        elif has_time:
            flush()
            current_time = line
        elif current_time and not current_title:
            current_title = line
        elif current_title and len(line) > 3 and len(line) < 100:
            # Could be a speaker name
            current_speakers.append(line)

    flush()
    print(f"    Fallback extracted {len(sessions)} sessions")
    return sessions


async def extract_speakers(el) -> list[str]:
    """Try common speaker markup patterns."""
    speakers = []
    selectors = [
        ".speaker-name", ".speakers", ".presenter", ".panelist",
        ".speaker", "[class*='speaker']", "[class*='presenter']",
        "cite", ".author",
    ]
    for sel in selectors:
        els = await el.query_selector_all(sel)
        for e in els:
            name = (await e.inner_text()).strip()
            if name and name not in speakers:
                speakers.append(name)
    return speakers


async def scrape_speakers_page(page) -> dict[str, dict]:
    """
    Scrapes marinemilitaryexpos.com/session-speakers/ for additional speaker metadata.
    Returns dict keyed by speaker name.
    """
    print(f"\nLoading speakers page: {SPEAKERS_URL}")
    try:
        await page.goto(SPEAKERS_URL, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_load_state("load", timeout=30000)
        await page.wait_for_timeout(2000)
    except Exception as e:
        print(f"  Could not load speakers page: {e}")
        return {}

    html = await page.content()
    with open("speakers_page_debug.html", "w") as f:
        f.write(html)
    print(f"  Speakers page HTML saved ({len(html)} bytes)")

    speakers = {}

    # Try structured speaker cards first
    card_selectors = [
        ".speaker-card", ".speaker-profile", ".team-member",
        ".wpb_team_member", ".jet-team-member",
        "[class*='speaker']", ".person",
    ]
    cards = []
    for sel in card_selectors:
        cards = await page.query_selector_all(sel)
        if cards:
            print(f"  Found {len(cards)} speaker cards with selector: {sel}")
            break

    for card in cards:
        try:
            name_el = await card.query_selector("h2, h3, h4, .name, .speaker-name, strong")
            name = (await name_el.inner_text()).strip() if name_el else ""
            if not name:
                continue
            bio_el = await card.query_selector("p, .bio, .description")
            bio = (await bio_el.inner_text()).strip() if bio_el else ""
            title_el = await card.query_selector(".title, .role, .position, em, .job-title")
            role = (await title_el.inner_text()).strip() if title_el else ""
            speakers[name] = {"name": name, "role": role, "bio": bio}
        except Exception as e:
            print(f"  Warning: speaker card parse error: {e}")

    if not speakers:
        # Fallback: extract names from headings
        print("  No cards found — extracting names from headings")
        headings = await page.query_selector_all("h2, h3, h4")
        for h in headings:
            name = (await h.inner_text()).strip()
            if name and len(name) < 80:
                speakers[name] = {"name": name, "role": "", "bio": ""}

    print(f"  Extracted {len(speakers)} speakers from speakers page")
    return speakers


def build_lookup(sessions: list[dict], speakers_meta: dict[str, dict]) -> list[dict]:
    """
    Flatten sessions into per-speaker rows.
    Enriches with metadata from speakers page where available.
    """
    rows = []
    for session in sessions:
        spk_list = session.get("speakers", [])
        if not spk_list:
            # Include session with empty speaker so it's not lost
            rows.append({
                "speaker_name": "",
                "stage": session.get("stage", ""),
                "day": session.get("day", ""),
                "session_title": session.get("title", ""),
                "start_time": session.get("time", ""),
            })
        else:
            for spk in spk_list:
                rows.append({
                    "speaker_name": spk,
                    "stage": session.get("stage", ""),
                    "day": session.get("day", ""),
                    "session_title": session.get("title", ""),
                    "start_time": session.get("time", ""),
                })
    return rows


async def main():
    async with async_playwright() as pw:
        import os, glob
        # Find whatever chromium binary is present in the pw-browsers path
        chrome_candidates = glob.glob("/opt/pw-browsers/chromium*/chrome-linux*/chrome") + \
                            glob.glob("/opt/pw-browsers/chromium*/chrome-linux64/chrome")
        exec_path = chrome_candidates[0] if chrome_candidates else None
        if exec_path:
            print(f"Using Chromium at: {exec_path}")
        launch_kwargs = dict(
            headless=True,
            args=[
                "--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage",
                "--disable-quic", "--disable-http2",
            ],
        )
        if exec_path:
            launch_kwargs["executable_path"] = exec_path
        browser = await pw.chromium.launch(**launch_kwargs)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 900},
            ignore_https_errors=True,
        )
        page = await context.new_page()

        # Scrape schedule
        sessions = await scrape_schedule(page)
        print(f"\nTotal raw sessions extracted: {len(sessions)}")

        # Scrape speakers page
        speakers_meta = await scrape_speakers_page(page)

        await browser.close()

    # Save raw JSON
    raw_path = "mdm2026_schedule_raw.json"
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(
            {"sessions": sessions, "speakers_meta": speakers_meta},
            f, indent=2, ensure_ascii=False,
        )
    print(f"\nSaved raw JSON to {raw_path}")

    # Build and save CSV lookup
    rows = build_lookup(sessions, speakers_meta)
    csv_path = "mdm2026_speaker_stage_lookup.csv"
    fieldnames = ["speaker_name", "stage", "day", "session_title", "start_time"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved CSV lookup to {csv_path} ({len(rows)} rows)")

    # Summary
    speaker_names = set(r["speaker_name"] for r in rows if r["speaker_name"])
    stages = set(r["stage"] for r in rows if r["stage"])
    days = set(r["day"] for r in rows if r["day"])
    print(f"\nSummary:")
    print(f"  Sessions: {len(sessions)}")
    print(f"  Unique speakers: {len(speaker_names)}")
    print(f"  Stages: {stages}")
    print(f"  Days: {days}")


if __name__ == "__main__":
    asyncio.run(main())
