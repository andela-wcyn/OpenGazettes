# Gazette listing

This is a simple Jekyll website listing Gazettes that we have scraped and indexed and stored in S3 as part of our [gazette liberation project](https://medium.com/code-for-africa/liberating-the-data-in-government-gazettes-380ec068077e).

The structure is simple. Each jurisdiction (country/province) and year has an entry in the ``_gazettes`` directory, which Jekyll treats as a collection. All the gazette info is taken from ``_data/gazettes.json`` which is grouped by jurisdiction and year. Jekyll then does the hard work of generating the listings for each jurisdiction and year.

# Running locally

1. Clone the repo
2. Run ``bundle install``
3. Run ``jekyll server --watch``

# Updating

To update this list from the production index:

    curl http://archive.opengazettes.or.ke/index/gazette-index-latest.jsonlines -O
    python bin/build-index.py

# Build process

The website is built automatically by GitHub pages based on the Gazette information already in the repository.

The [build branch](https://github.com/OpenGazettes/OpenGazettes/tree/build) has code that updates the information in the repository from the Gazette index in S3. A Travis build for this branch is triggered automatically when we archive new Gazettes in S3.

# License

MIT License.
