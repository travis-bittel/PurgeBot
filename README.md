# PurgeBot
A trivial bot used to conditionally purge (kick) users from a Discord server following a configurable schedule and set 
of conditions.

This repo uses the Discord.py library to do the kicking. That code is freely available in case it proves useful to 
anyone out there.

This repo *also* contains the Terraform definitions of the serverless AWS infrastructure I have used to run this bot,
which I suppose you can also copy if that's the way you'd like to go.

## Installation
This project uses Poetry for package management, mainly because I needed to get comfortable with it for use at work.

To install Poetry you need pipx:
* Windows: `py -m pip install --user pipx && py -m pipx ensurepath`
* Mac: `brew install pipx`
* Linux: `brew install pipx`

Then use `pipx` to install Poetry:
* Windows: `pipx install poetry`
* Mac: `pipx install poetry`
* Linux: `pipx install poetry`

Then install the project dependencies:
1. `poetry lock`
2. `poetry update`
3. `poetry install --extras dev-dependencies`

## Unit Tests
From the base directory, run: `poetry run pytest`

## Deployment
1. From the base directory: `poetry build-lambda`
2. From the `aws` directory: `terraform apply`

