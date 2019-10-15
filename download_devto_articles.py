import os
import datetime
import json
import argparse
import pathlib
from urllib.parse import urlparse
import urllib.request, json

from common import get_articles_root_path, replace_colon, ARTICLES_DICT_FILE

articles_dict = {}

def download_and_save_articles(username, dirname, article_name):
    output_dir_path = get_articles_root_path(pathlib.Path(dirname))

    if not article_name:
        os.makedirs(output_dir_path)

    contents_of_articles = get_contents_of_articles(username, article_name)
    for article_contents in contents_of_articles:
        save_article(output_dir_path, article_contents)

    with open(ARTICLES_DICT_FILE, 'w', encoding='utf-8') as f:
        json.dump(articles_dict, f, ensure_ascii=False, indent=4)


def get_contents_of_articles(username, article_name):
    contents_of_articles = []
    articles = get_articles(username)
    for article in articles:
        if not article_name or article_name in article['url']:
            contents = get_article_contents(article['id'])
            contents_of_articles.append(contents)

    return contents_of_articles


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


def get_url_string(username, page):
    return f"https://dev.to/api/articles?username={username}&page={page}"


def get_article_contents(article_id):
    url_string = f"https://dev.to/api/articles/{article_id}"
    with urllib.request.urlopen(url_string) as url:
        data = url.read().decode()
        results = json.loads(data)
        return results


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

    key = f"{output_dir_path.name}/{article_filename}"
    title = replace_colon(article_contents["title"]).strip()
    articles_dict[key] = {"title": title}


def get_article_filename(article_url, article_id, published_date):
    url_path = pathlib.Path(urlparse(article_url).path)
    dt = datetime.datetime.strptime(published_date, '%Y-%m-%dT%H:%M:%S%z')

    filename = (f"{dt.strftime('%Y-%m-%d')}-"
                + url_path.name
                + f".{article_id}.md")
    return filename


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="whose articles to download")
    parser.add_argument("download_dir", help="output files directory")
    parser.add_argument("--article", help="article to download")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_command_line_args()
    download_and_save_articles(args.username, args.download_dir, args.article)
