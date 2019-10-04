Scripts that help back up and manage dev.to blog articles.

To download a user's articles as markdown from dev.to:

* `python download_devto_articles.py <username> <dir> --article <article>`

This script downloads all of a user's published articles, and saves each article as a markdown file in the `dir` folder. The filename created for each article corresponds to the last portion of its url, but prepends the publication date, and appends the article's dev.to `id`, to the filename (just before the `.md` suffix).

> `article` is an optional argument corresponding to the article's name in the url on dev.to. When provided, only that article will be downloaded. For this use case, `dir` must already exist.

To download and save article images:

* `python download_images.py <dir> --article <article>`

This script reads through markdown files in the `dir` folder and downloads the images referenced in each file. The images are saved into a folder with the same name as the corresponding markdown file (excluding the file extension). The images are saved with filenames that match the filename for the url referenced in the markdown file.

> `article` is an optional argument corresponding to the article's name in the url on dev.to. When provided, only the images for that article will be downloaded. For this use case, `dir` must already exist.

To create a copy with local image references:

* `python copy_with_local_images.py <srcdir> <destdir>`

This script will make a copy of the markdown files and image folders in `srcdir`, and place them in the `destdir` directory. All image urls in the markdown files will be modified to reference the local files. The resulting files can be used for a self-hosted version of the blog.

> * `article` is an optional argument corresponding to the article's name in the url on dev.to. When provided, only that article will be updated. For this use case, `destdir` must already exist.
> * This script does not currently re-write links to one's own articles on dev.to that may be in the markdown files. It also does not have special handling for frontmatter, liquid tags, etc.

To combine the previous three steps, run:

* `python download_articles_images_and_create_localized_copies.py <username> <download_dir> <localized_dir> -- article <article>`

`download_dir` is the directory into which to download the markdown files and images. `localized_dir` is the directory into which to copy these files when updating the markdown files to use local image references. `article` is the optional parameter that specifies the name of a single file. As before, when it's used, only the file with that name in its url will be processed.
