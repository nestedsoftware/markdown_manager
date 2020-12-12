Scripts that download and transform dev.to blog articles.

The `main.py` script runs three subordinate scripts, `download_articles.py`, `download_images.py`, and `copy_and_transform.py`. The following will run the main script, which downloads articles, images, and then makes copies which transform the original markdown content:

* `python main.py <username> --root <root dir> --download_dir <download dir> --transformed_dir <transform dir> --article <article name>`

Options:

* `username` refers to the dev.to user whose articles will be downloaded
* `root dir` determines which base path the files are downloaded to - defaults to the current directory.
* `download dir` is the directory to which the markdown files and image files will be downloaded - defaults to `downloaded_files`
* `transform dir` will contain a copy of the contents of `download dir` with changes applied to the markdown (localizes links and fixes some markdown to work with jekyll) - defaults to `transformed_files`
* Once this script has been run for all articles, the `--article` option can be used to download and transform additional articles one at a time. `article name` refers to the name of the article in the dev.to url - a wildcard match to this parameter is applied.

Example:

* `python main.py ben --root ~/downloaded_articles`

When `download_articles.py` runs, it generates an `articles_dict.json` file. This file stores key-value pair mappings of article names to article titles. This is used by the `copy_and_transform.py` script to produce local links when an article links another article by the current author, as specified by `username`.

By default, these scripts download the markdown files to the `_posts` subdirectory, and the images to the `assets/images` subdirectory, to match the structure expected by the jekyll static site generator. This can be modified in `common.py`.

To delete an article, run:

* `python delete_matching.py <article name> --root <root dir>`

This will delete matching markdown files and image directories, and will also remove the mapping for that article from `articles_dict.json`.
