Scripts that help back up and manage dev.to blog articles.

To download a user's articles as markdown from dev.to:

* `python download_devto_articles.py <username> <dir>`

This script downloads all of a user's published articles, and saves each article as a markdown file in the `dir` folder. The name of each article corresponds to the last portion of its url, but prepends the publication date, and appends the article's dev.to `id` to the filename (just before the `.md` suffix).

To download and save article images:

* `python download_images.py <dir>`

This script reads through markdown files in the `dir` folder and downloads the images contained in each file. The images are saved into a folder with the same name as the corresponding markdown file (excluding the file extension). The images are saved with filenames that match the filename for the url referenced in the markdown file.

To create a copy with local image references:

* `python copy_with_local_images.py <srcdir> <destdir>`

This script will copy the `srcdir` folder containing markdown files and image folders and place it in the `destdir` directory. All image urls in the markdown files will be modified to reference the local files. The resulting files can be used for a self-hosted version of the blog.

> This script does not currently re-write links to one's own articles on dev.to that may be in the markdown files.
