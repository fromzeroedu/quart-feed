FROM python:3.9-slim

# Install ImageMagick for Wand
RUN apt-get update && apt-get install -y
RUN apt-get install -y \
    imagemagick \
    libmagickwand-dev

# Install pipenv
RUN pip install pipenv

# Make a local directory
RUN mkdir /quarteed_app

# Set "quarteed_app" as the working directory
WORKDIR /quartfeed_app

# Copy all the files in the present directory to "quartfeed_app"
ADD . .

# pipenv install
RUN pipenv install

# Listen to port 5000 at runtime
EXPOSE 5000

# Define our command to be run when launching the container
CMD pipenv run quart run --host 0.0.0.0
