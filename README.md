# pill

Downloads all posts and comments from given subreddit. One can also change it generate text output from images.

## Important

This project relies on 3rd Party API that relies on the reddit API, due to the recent changes in the reddit API pricing, thisproject may malfunction.
And update with web scrappers might be necessary.

## Dependencies

```bash
pmaw, praw, datetime, requests, matplotlib, nltk, pytesseract, pandas, opencv, pillow
```

## Usage

Pull data from the given subreddits, to change the subreddit find it's name give it a shortened name and
add it to the subreddits file in constants, to find data from a different time period change the years and years_asc fields
in years. Do not touch months, or modify the scripts accordingly.

Currently the data is collected and dictionaries are created for dating-related subredddits. It could also work for other subreddits.
To change the subreddits, the dictionaries, the data collection time span you would need to adapt the contants.py file.

```python
# get the first $limit posts between the $after and $before dates
# This will be usefull when data is collected from a huge subreddit
limit = 10000000

# You can add years to collect the data from other years
# Years_asc used internally, you could copy over the years listi
years = [2018, 2019, 2020, 2021]
years_asc = [2018, 2019, 2020, 2021]

# Months where the data should be collected (replicated through every year)
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# List of subreddits to collect
subreddits = [
    ("PurplePillDebate", "pp"),
    ("MensRights", "mr"),
    ("BlackPillScience", "bps"),
    ("TheRedPill", "trp"),
    ("FemaleDatingStrategy", "fds")
]
```


```bash
python3 src/raw_collector.py
```

And lemmetize (and tokenize) text with

```bash
python3 src/tokenizer.py
```

After getting data user can check for:

1. Percentage of deleted posts of deleted comments (raw data)
```bash
python3 src/deleted_percentage.py
```

2. Printing users' last active status and active posters and commenters over months (raw data)
```bash
python3 src/user_statistics.py
```

3. Users' activity over months with some regression (raw data)
```bash
python3 src/user_activity_over_months.py
```

4. Froquency of jargon, hate words and gatekeeping related words (lemmetized data)
```bash
python3 src/word_frequency.py
```
5. Possible gatekeeping posts per sub. For this user needs to first analyze texts of images, which will be
be done through a call to image_to_text.py then the tokenizer needs to be changed to use files that have "-img.csv" as an
ending after those files are created user can check for the amount of possible unique gatekeeping posts by
```bash
python3 src/gatekeep_detector.py
```
