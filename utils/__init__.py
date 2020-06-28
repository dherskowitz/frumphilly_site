import re
from io import BytesIO
from PIL import Image
from django.core.files import File


def compress(image):
    """"Compress submitted images"""
    size = 600, 600
    im = Image.open(image)
    # create a BytesIO object
    im_io = BytesIO()
    # save image to BytesIO object
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(im_io, "JPEG", quality=70)
    # create a django-friendly Files object
    new_image = File(im_io, name=image.name)
    return new_image


def get_video(video_link):
    """Parse submitted data for video id or iFrame src and normalize url"""
    video = video_id = ""
    if re.search("iframe", video_link):
        """If video is iFrame grab src and set as video"""
        source = re.findall('src\s*=\s*"(.+?)"', video_link)
        if len(source) > 0:
            video = source[0]
    elif re.search("youtube", video_link) or re.search("youtu.be", video_link):
        """If video is youtube link get video id and build url for video"""
        if re.search("youtube.com/watch", video_link):
            video_id = video_link.split("v=")[1]
            if re.search("&", video_link):
                temp = video_link.split("&")[0]
                video_id = temp.split("v=")[-1]
        elif re.search("youtu.be", video_link) or re.search(
            "youtube.com/embed", video_link
        ):
            video_id = video_link.split("/")[-1]
        video = f"https://youtube.com/embed/{video_id}"
    elif re.search("vimeo", video_link):
        """If video is vimeo link get video id and build url for video"""
        video_id = video_link.split("/")[-1]
        video = f"https://player.vimeo.com/video/{video_id}"
    return video
