import os
import datetime
import argparse
import pathlib
from urllib.parse import urlparse
import urllib.request, json

def get_url_string(username, page):
    return f"https://dev.to/api/articles?username={username}&page={page}"


def get_articles(username):
    page = 1
    all_results = []
    url_string = get_url_string(username, page)
    while True:
        with urllib.request.urlopen(url_string) as url:
            data = url.read().decode()
            results = json.loads(data)
            if len(results) == 0:
                return all_results

            all_results += results

            page +=1
            url_string = get_url_string(username, page)


def get_article_contents(article_id):
    url_string = f"https://dev.to/api/articles/{article_id}"
    with urllib.request.urlopen(url_string) as url:
        data = url.read().decode()
        results = json.loads(data)
        return results


def get_contents_for_all_articles(username):
    articles_detailed_contents = []
    articles = get_articles(username)
    for article in articles:
        contents = get_article_contents(article['id'])
        articles_detailed_contents.append(contents)

    return articles_detailed_contents


def get_article_filename(article_url, article_id, published_date):
    url_path = pathlib.Path(urlparse(article_url).path)
    dt = datetime.datetime.strptime(published_date, '%Y-%m-%dT%H:%M:%S%z')

    filename = (f"{dt.strftime('%Y%m%d')}-"
                + url_path.name
                + f".{article_id}.md")
    return filename


def save_article(output_dir_path, article_contents):
    article_url = article_contents['url']
    article_id = article_contents['id']
    article_markdown = article_contents['body_markdown']
    published_date_string = article_contents['published_at']

    article_filename = get_article_filename(article_url, article_id,
                                            published_date_string)

    article_path = output_dir_path / article_filename
    with article_path.open("w", encoding="utf8", newline="\n") as f:
        f.write(article_markdown)


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="whose articles to download")
    parser.add_argument("dir", help="output files directory")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_command_line_args()

    username = args.username
    articles_detailed_contents = get_contents_for_all_articles(username)

    output_dir_path = pathlib.Path(args.dir)
    os.makedirs(output_dir_path)

    for article_detailed_contents in articles_detailed_contents:
        save_article(output_dir_path, article_detailed_contents)
