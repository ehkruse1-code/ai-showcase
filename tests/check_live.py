"""Check the public landing page and the retired direct video URLs."""
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from test_site import Page

base = 'https://ehkruse1-code.github.io/ai-showcase/'
with urlopen(base, timeout=30) as response:
    assert response.status == 200
    html = response.read().decode('utf-8')
page = Page()
page.feed(html)
assert 'Video unavailable' in html
assert not set(page.tags) & {'video', 'source', 'iframe', 'button'}
assert not any('.mp4' in url or '/releases/download/' in url for url in page.urls)
retired = [
    base + 'assets/showcase-v18-4k.mp4',
    'https://github.com/ehkruse1-code/ai-showcase/releases/download/v18/Nissan-AI-Showcase-Complete-v18-Native4K-Explosion-Silent-4K.mp4',
    'https://github.com/ehkruse1-code/ai-showcase/releases/download/v17/Nissan-AI-Showcase-Complete-v17-Loop-Fade-Silent-4K.mp4',
]
for url in retired:
    try:
        with urlopen(Request(url, method='HEAD'), timeout=30) as response:
            raise AssertionError(f'Video still accessible: {url} ({response.status})')
    except HTTPError as error:
        assert error.code == 404, (url, error.code)
    print('404:', url)
print('PASS: landing page online; player and links absent; retired videos return 404.')
