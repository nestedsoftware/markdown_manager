import re

cover_image_regex = r'cover_image:\s*(?P<url>[^\s]+)\s*'
cover_image_pattern = re.compile(cover_image_regex)

alt = r'!\[(?P<alttext>[^\]]*)\]'
url = r'\(\s*(?P<url>[^\s]+)\s*'
title = r'(\"(?P<titletext>[^\"]*)\")?\)'
image_regex = alt + url + title
image_pattern = re.compile(image_regex)
