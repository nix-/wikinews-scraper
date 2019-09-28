# wikinews-scraper
> Wikinews article-content scraper written in Python.

The code provides to developer easy way for scraping the content of [Wikinews](https://en.wikinews.org/wiki/Main_Page).

Components that can be easly access are:
- headline,
- body,
- date,
- photos,
- entities,
- related-articles,
- source-articles and etc.

![Wikinews Article](img/wikin-article.png)

## Dependencies

The folowing packages are required:
- [requests](https://pypi.org/project/requests/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

If you do not have them, for more info how to install them according your OS please find more information on the internet.

## Starting the demo

The demo.py is the first point that need to be addressed.

Script first is scraping (from the main page) all of the article's links.
Second scraping-stage is getting the elements of the whole article (given throught article's link).

Linux:

```sh
python3 demo.py
```
