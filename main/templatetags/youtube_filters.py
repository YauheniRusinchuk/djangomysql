import re
from django import template

register = template.Library()


@register.filter
def youtube_embed_url(url):
    """
    Convert YouTube URL to embed URL
    Examples:
        https://www.youtube.com/watch?v=VIDEO_ID -> https://www.youtube.com/embed/VIDEO_ID
        https://youtu.be/VIDEO_ID -> https://www.youtube.com/embed/VIDEO_ID
    """
    if not url:
        return ''

    # Regular expression to match YouTube URLs
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        video_id = youtube_regex_match.group(6)
        return f'https://www.youtube.com/embed/{video_id}'

    return url
