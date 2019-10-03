To download a user's articles as markdown from dev.to:

* `python download_devto_articles.py <username> <dir>`

This script downloads all of a user's published articles, and saves each article as a markdown file in the `dir` folder. The name of each article corresponds to the last portion of its url, but also appends the article's dev.to `id` in the filename just before the `.md` suffix.

To download and save article images:

* `python download_images.py <dir>`

This script reads through markdown files in the `dir` folder and downloads the images contained in each file. The images are saved into a folder with the same name as the corresponding markdown file (excluding the file extension). The images are saved with filenames that match the filename for the url referenced in the markdown file.
