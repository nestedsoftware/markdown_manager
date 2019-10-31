from common import cover_image_pattern, image_pattern
from copy_and_transform import (link_pattern, md_link_pattern, title_pattern,
                                gist_pattern, github_pattern, heading_pattern,
                                filename_pattern)

def test_cover_image():
    cover_part = "cover_image:"
    url_part = "https://thepracticaldev.s3.amazonaws.com/i/2mc3q85i0wzquufl1j82.jpg"

    text = f"{cover_part}{url_part}"

    result = cover_image_pattern.match(text)

    url = result.group("url")
    assert url == url_part


def test_image_link():
    alt_part = "2x3 network activations"
    url_part = "https://thepracticaldev.s3.amazonaws.com/i/063o18p485i8ba6v3pvm.png"
    title_part = "this is the title"

    text = f'![{alt_part}]({url_part} "{title_part}")'

    result = image_pattern.match(text)

    url = result.group("url")
    alttext = result.group("alttext")
    titletext = result.group("titletext")

    assert url == url_part
    assert alttext == alt_part
    assert titletext == title_part


def test_title():
    title_header = "title:"
    title_body = "Neural Networks Primer"

    text = f"{title_header} {title_body}"

    result = title_pattern.match(text)

    title = result.group("title")
    assert title == title_body


def test_gist():
    gist_part = "gist"
    url_part = "https://gist.github.com/nestedsoftware/"
    id_part = "8d1ac438dec30027e304c489fca23cfb"

    text = f"{{% {gist_part} {url_part}{id_part} %}}"

    result = gist_pattern.match(text)

    url = result.group("url")
    gistid = result.group("gistid")

    assert url == f"{url_part}{id_part}"
    assert gistid == id_part


def test_github():
    github_part = "github"
    url_part = "https://github.com/nestedsoftware/iterative_stats"

    text = f"{{% {github_part} {url_part} %}}"

    result = github_pattern.match(text)

    url = result.group("url")

    assert url == url_part


def test_heading():
    text = "##This is a heading"

    result = heading_pattern.match(text)

    assert result.group(0) == "##"


def test_filename():
    date_part = "2017-05-16"
    main_part = "how-does-your-organization-pass-secret-keys-around"
    end_part = ".3854.md"

    text = f"{date_part}-{main_part}{end_part}"

    result = filename_pattern.match(text)

    main = result.group("main")
    assert main == main_part


def test_liquid_link_tag():
    http_part = "http"
    domain_part = "://dev.to"
    username_part = "ben"
    filename_part = "what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"
    comment_part = "/comments"

    text = f"{{% link {http_part}s{domain_part}/{username_part}/{filename_part} %}}"
    result = link_pattern.match(text)
    assert result.group(0) == text
    assert result.group("url") == r"https://dev.to/ben/what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"
    assert result.group("username") == r"ben"
    assert result.group("filename") == r"what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"

    text = f"{{% link {http_part}s{domain_part}/{username_part}/{filename_part}{comment_part} %}}"
    result = link_pattern.match(text)
    assert result.group(0) == text
    assert result.group("url") == r"https://dev.to/ben/what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn/comments"
    assert result.group("username") == r"ben"
    assert result.group("filename") == r"what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn/comments"

    text = f"{{% link {http_part}{domain_part}/{username_part}/{filename_part} %}}"
    result = link_pattern.match(text)
    assert result.group(0) == text
    assert result.group("url") == r"http://dev.to/ben/what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"
    assert result.group("username") == r"ben"
    assert result.group("filename") == r"what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"

    text = f"{{%      link     {http_part}s{domain_part}/{username_part}/{filename_part}     %}}"
    result = link_pattern.match(text)
    assert result.group(0) == text
    assert result.group("url") == r"https://dev.to/ben/what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"
    assert result.group("username") == r"ben"
    assert result.group("filename") == r"what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"

    text = f"{{% link {username_part}/{filename_part} %}}"
    result = link_pattern.match(text)
    assert result.group(0) == text
    assert result.group("url") == r"ben/what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"
    assert result.group("username") == r"ben"
    assert result.group("filename") == r"what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"

    text = f"{{% link /{username_part}/{filename_part} %}}"
    result = link_pattern.match(text)
    assert result.group(0) == text
    assert result.group("url") == r"/ben/what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"
    assert result.group("username") == r"ben"
    assert result.group("filename") == r"what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"


def test_markdown_link_tag():
    title_part = "worst security practices"
    http_part = "http"
    domain_part = "://dev.to"
    username_part = "ben"
    filename_part = "what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"
    comment_part = "/comments"

    text = f"[{title_part}]({http_part}s{domain_part}/{username_part}/{filename_part})"
    result = md_link_pattern.match(text)
    assert result.group(0) == text
    assert result.group("url") == r"https://dev.to/ben/what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"
    assert result.group("username") == r"ben"
    assert result.group("filename") == r"what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"

    text = f"[{title_part}]({http_part}s{domain_part}/{username_part}/{filename_part}{comment_part})"
    result = md_link_pattern.match(text)
    assert result.group(0) == text
    assert result.group("url") == r"https://dev.to/ben/what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn/comments"
    assert result.group("username") == r"ben"
    assert result.group("filename") == r"what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn/comments"

    text = f"[{title_part}]({http_part}{domain_part}/{username_part}/{filename_part})"
    result = md_link_pattern.match(text)
    assert result.group(0) == text
    assert result.group("url") == r"http://dev.to/ben/what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"
    assert result.group("username") == r"ben"
    assert result.group("filename") == r"what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"

    text = f"[   {title_part}   ](   {http_part}s{domain_part}/{username_part}/{filename_part}   )"
    result = md_link_pattern.match(text)
    assert result.group(0) == text
    assert result.group("url") == r"https://dev.to/ben/what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"
    assert result.group("username") == r"ben"
    assert result.group("filename") == r"what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"

    text = f"[{title_part}](/{username_part}/{filename_part})"
    result = md_link_pattern.match(text)
    assert result.group(0) == text
    assert result.group("url") == r"/ben/what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"
    assert result.group("username") == r"ben"
    assert result.group("filename") == r"what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"

    text = f"[{title_part}]({username_part}/{filename_part})"
    result = md_link_pattern.match(text)
    assert result.group(0) == text
    assert result.group("url") == r"ben/what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"
    assert result.group("username") == r"ben"
    assert result.group("filename") == r"what-are-the-worst-security-practices-you-ve-ever-witnessed-2lmn"


def test_markdown_link_tag_multiple_matches():
    text = "In [Neural Networks Primer](https://dev.to/nestedsoftware/neural-networks-primer-374i), we went over the details of how to implement a basic neural network from scratch. We saw that this simple neural network, while it did not represent the state of the art in the field, could nonetheless do a very good job of recognizing hand-written digits from the [mnist](http://yann.lecun.com/exdb/mnist/) database. An accuracy of about 95% was quite easy to achieve."

    results = md_link_pattern.finditer(text)

    result = next(results)
    assert result.group("url") == "https://dev.to/nestedsoftware/neural-networks-primer-374i"
    assert result.group("username") == "nestedsoftware"
    assert result.group("filename") == "neural-networks-primer-374i"

    result = next(results)
    assert result.group("url") == "http://yann.lecun.com/exdb/mnist/"
    assert result.group("username") == "http:"
    assert result.group("filename") == "/yann.lecun.com/exdb/mnist/"
