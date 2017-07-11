# Gazette listing

This is a simple Jekyll website listing Gazettes that we have scraped and indexed and stored in S3 as part of our [gazette liberation project](https://medium.com/code-for-africa/liberating-the-data-in-government-gazettes-380ec068077e).

The structure is simple. Each jurisdiction (country/province) and year has an entry in the ``_gazettes`` directory, which Jekyll treats as a collection. All the gazette info is taken from ``_data/gazettes.json`` which is grouped by jurisdiction and year. Jekyll then does the hard work of generating the listings for each jurisdiction and year.

# Running locally

1. Clone the repo
2. Run ``bundle install``
3. Run ``jekyll server --watch``

# Updating

To update this list from the production index:

    curl https://s3-eu-west-1.amazonaws.com/cfa-opengazettes-ng/gazettes/gazettes_index.jsonlines -O
    python bin/build-index.py

# Deploying to S3

The website is deployed to S3 using [s3_website](https://github.com/laurilehmijoki/s3_website)

To deploy:

- Make a copy of the `.env.example` file and name it `.env`
- Add your `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` to the `.env` file
- Run `./deploy.sh` from the root directory
- You're done!

# License

MIT License.
