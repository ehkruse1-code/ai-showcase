from html.parser import HTMLParser
from pathlib import Path
import unittest


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.urls = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        self.urls.extend(value for key, value in attrs if key in ('href', 'src') and value)


class SiteTests(unittest.TestCase):
    def test_withdrawn_video_has_no_playback_or_download_path(self):
        root = Path(__file__).resolve().parents[1]
        html = (root / 'index.html').read_text(encoding='utf-8')
        page = Page()
        page.feed(html)
        self.assertIn('Video unavailable', html)
        self.assertIn('Nissan AI Showcase', html)
        self.assertFalse(set(page.tags) & {'video', 'source', 'iframe', 'button'})
        self.assertFalse(any('.mp4' in url or '/releases/download/' in url for url in page.urls))
        self.assertFalse(list((root / 'assets').glob('*.mp4')))


if __name__ == '__main__':
    unittest.main()
