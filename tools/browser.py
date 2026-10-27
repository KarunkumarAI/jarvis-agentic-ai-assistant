from urllib.parse import quote_plus

from playwright.sync_api import Browser, Page, Playwright, sync_playwright


_playwright: Playwright | None = None
_browser: Browser | None = None
_page: Page | None = None


def start_browser() -> Page:
    global _playwright, _browser, _page

    if _page:
        return _page

    _playwright = sync_playwright().start()
    _browser = _playwright.chromium.launch(headless=False)
    _page = _browser.new_page()

    return _page


def open_website(url: str) -> str:
    page = start_browser()
    page.goto(url)

    return f"Opened {url}"


def google_search(query: str) -> str:
    url = f"https://www.google.com/search?q={quote_plus(query)}"
    return open_website(url)



def youtube_search(query: str) -> str:
    url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
    return open_website(url)


def youtube_play(query: str) -> str:
    page = start_browser()

    try:
        search_url = (
            "https://www.youtube.com/results"
            f"?search_query={quote_plus(query)}"
        )

        page.goto(
            search_url,
            wait_until="domcontentloaded",
            timeout=30000,
        )

        # Find an actual video result, not a channel or playlist.
        video = page.locator(
            "ytd-video-renderer a#video-title"
        ).first

        video.wait_for(state="visible", timeout=15000)

        title = video.get_attribute("title") or query
        video.click()

        # Wait for the YouTube video player.
        page.locator("video.html5-main-video").wait_for(
            state="attached",
            timeout=15000,
        )

        # Try to start playback.
        page.locator("video.html5-main-video").evaluate(
            """async (video) => {
                video.muted = false;
                await video.play();
            }"""
        )

        # Check whether playback has actually started.
        page.wait_for_function(
            """() => {
                const video = document.querySelector(
                    'video.html5-main-video'
                );
                return video &&
                       !video.paused &&
                       video.readyState >= 2;
            }""",
            timeout=10000,
        )

        return f"Now playing on YouTube: {title}"

    except Exception as error:
        return (
            "Could not start YouTube playback automatically. "
            f"Reason: {error}"
        )



def close_browser() -> None:
    global _playwright, _browser, _page

    if _browser:
        _browser.close()

    if _playwright:
        _playwright.stop()

    _page = None
    _browser = None
    _playwright = None

def go_back() -> str:          # just for scroll and all if its not still works
    page = start_browser()
    page.go_back()
    return "Went back."


def scroll_down() -> str:
    page = start_browser()
    page.mouse.wheel(0, 700)
    return "Scrolled down."