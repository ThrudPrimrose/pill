# pill

Downloads all posts and comments from given subreddit. One can also change it generate text output from images.

## Dependencies

```bash
pmaw, praw, datetime, requests, matplotlib, nltk, pytesseract, pandas, opencv, pillow
```

## Usage

Pull data from the given subreddits, to change the subreddit find it's name give it a shortened name and
add it to the subreddits file in constants, to find data from a different time period change the years and years_asc fields
in years. Do not touch months, or modify the scripts accordingly.

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