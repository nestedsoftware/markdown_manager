Scripts that download and transform dev.to blog articles.

The `main.py` script runs three subordinate scripts, `download_articles.py`, `download_images.py`, and `copy_and_transform.py`. The following will run the main script, which downloads articles, images, and then makes copies which transform the original markdown content:

* `python main.py <username> <download dir> <transform dir> <root dir> --article <article name>`

Options:

* `username` refers to the dev.to user whose articles will be downloaded
* `download dir` is the directory to which the markdown files and image files that will be downloaded
* `transform dir` copies the contents of `download dir` and applies changes to the markdown (localizes links and fixes some markdown to work with jekyll)
* `root dir` determines which path the files are downloaded to - defaults to the current directory.
* `article name` is optional. Once this script has been run for all existing articles, this option can be used to download and transform additional articles one at a time. This option assumes that the directory structure has already been generated previously. The article name refers to the name of the article in the dev.to url - a wildcard match to this parameter is applied.

When `download_articles.py` runs, it generates an `articles_dict.json` file. This file stores key-value pair mappings of article names to article titles. This is used by the `copy_and_transform.py` script to produce links when an article has a link to another article by the current author as specified by 'username'.

By default, these scripts download the markdown files to the `_posts` subdirectory, and the images to the `assets/images` subdirectory, to match the structure expected by the jekyll static site generator.

To delete an article, run:

* `python delete_matching <article name> <root dir>`

This will delete matching markdown files and image directories, and will also remove the mapping for that article from `articles_dict.json`.
