#!/bin/bash
#
# Cleans and deploys the project to S3.
#
# Usage:
#   ./deploy.sh
#
# This script gets the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY from your .env file
# It will fail if those are not present

# Initialize some vars
. .env
export DEPLOY_DIR=".deploy"

bundle exec jekyll build

# Copy the site directory to a temporary location so that modifications we make
# don't get overwritten by the Jekyll server that is potentially running
mkdir -p $DEPLOY_DIR
cp -a _site/. $DEPLOY_DIR

for file in $DEPLOY_DIR/gazettes/$JURISDICTION_CODE/*.html; do
    if [ $file != "$DEPLOY_DIR/gazettes/$JURISDICTION_CODE/index.html" ];
    then
        mv "$file" "$DEPLOY_DIR/gazettes/$JURISDICTION_CODE/`basename "$file" .html`"
    fi
done

for file in $DEPLOY_DIR/*.html; do
    if [ $file != "$DEPLOY_DIR/index.html" ];
    then
        mv "$file" "$DEPLOY_DIR/`basename "$file" .html`"
    fi
done

# Go through sitemap.xml and remove occurences of `.html`
sed -e 's/.html//g' _site/sitemap.xml > $DEPLOY_DIR/sitemap.xml

s3_website push --site=$DEPLOY_DIR

# Cleanup
rm -r $DEPLOY_DIR
