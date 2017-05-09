#!/bin/bash
# 
# Cleans and deploys the project to S3.
#
# Usage:
#   ./deploy.sh <AWS_ACCESS_KEY_ID> <AWS_SECRET_ACCESS_KEY>

# Initialize some vars
export AWS_ACCESS_KEY_ID="$1"
export AWS_SECRET_ACCESS_KEY="$2"
export AWS_DEFAULT_REGION="eu-west-1"
export BUCKET="opengazettes.or.ke"

export DEPLOY_DIR=".deploy"

jekyll build

# Copy the site directory to a temporary location so that modifications we make don't get overwritten by the Jekyll server
# that is potentially running
mkdir -p $DEPLOY_DIR
cp -a _site/. $DEPLOY_DIR

for file in $DEPLOY_DIR/gazettes/KE/*.html; do
    if [ $file != "$DEPLOY_DIR/gazettes/KE/index.html" ];
    then
        mv "$file" "$DEPLOY_DIR/gazettes/KE/`basename "$file" .html`"
    fi
done

for file in $DEPLOY_DIR/*.html; do
    if [ $file != "$DEPLOY_DIR/index.html" ];
    then
        mv "$file" "$DEPLOY_DIR/`basename "$file" .html`"
    fi
done

s3_website push --site=$DEPLOY_DIR

# Cleanup
rm -r $DEPLOY_DIR
