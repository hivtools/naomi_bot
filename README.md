# naomi_bot

A bot for creating hintr PRs from naomi PRs

When there is a new PR in naomi https://github.com/mrc-ide/naomi which updates the version number this bot will:
  * Create a new branch in hintr https://github.com/mrc-ide/hintr called naomi-<version_number>
  * Update the version of naomi in the `DESCRIPTION`
  * Pin the docker build script to the head branch of the naomi PR
  * Create a PR for the new branch into master

The intention is that this will trigger builds for hintr, if the build passes we can have some confidence that we can merge the new naomi PR and the app won't break. We could also deploy the new naomi PR to staging if the hintr tests pass. After this passes to get the naomi changes onto production we need to:
  * Merge naomi PR into master
  * Remove branch pins in docker build
  * Merge the hintr PR
  * Wait for `master` buildkite build to finish
  * Redeploy production

## Running

To run the service locally use the docker image

`docker/run`

You may have to build first, if so

`docker/build`

## Deployment

At the moment this is deployed on support to update ssh onto support

`ssh montagu@support.montagu.dide.ic.ac.uk`

Kill running image and run up a new one

```
cd naomi_bot
docker kill naomi_bot
./docker/run
```

## Tests

There is pretty minimal testing of this at the moment but tests can be run by running `pytest` from the repository root.

There is also a `GET` endpoint which runs the branch updates which I have been used for testing. You can hit this using `curl` for a quick development cycle by:
  * Deploy the app locally - from the root of this project run `python -m naomi_bot`
  * Hit the `GET` endpoint using `curl localhost:8080`