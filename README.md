## Files and purpose (Include/)

  - Notes:
    - Paths in the script sometimes use backslashes (`.\\datasets\\{file}`) and other times forward slashes (`./datasets/`); adapt them to your OS/working directory when running.
    - The script depends on `pandas`, `scikit-learn` and the standard `csv` module.

- raw1label.csv
  - A CSV data sample included under `Include/`.
  - Observed columns (from the preview):
    - aggressivite (float) — normalized measure of aggressiveness per user/tweet
    - visibilite (float) — visibility metric (e.g., fraction or normalized)
    - nombreUrl (int) — number of URLs in tweet(s)
    - id (numeric / possibly Twitter id)
    - frequence_tweet (float) — frequency of tweeting
    - label (1 or -1) — label assigned (1 or -1) — consistent with the labeling scheme in `DataSegmentation_kmeans.py`
  - The file contains many rows (preview shows numerous examples). It appears to be a processed sample with labels already attached.





## Directory structure (relevant part)

Include/
- Acp.ipynb
- DataSegmentation_kmeans.py
- Data_Exploration.ipynb
- kmeans.ipynb
- kmeans.py
- mongos.ipynb
- raw1label.csv
- Label/
  - Directory used to store labeled/segmented files.
  - Contains a `DONE/` subdirectory in the repository — likely used to mark completed outputs or to store finished label files.
  - DONE/

##Author

Repository owner: thibaut7

If you want, I can:
- produce a cleaned README file in repository format,
- extract and document column definitions from `kmeans.csv` (if you point me to the file),
- or adapt the segmentation script to run on different chunk sizes or cluster counts.
