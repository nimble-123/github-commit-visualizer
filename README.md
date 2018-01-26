# github-commit-visualizer
Python script to visualize multiple github repositories commit history with gource.io

Clone this repo

Run docker with following arguments

```
sudo docker run -d --env-file ./.env nlsltz/github-commit-visualizer -v logs:logs -v repos:repos -v output:output
```
