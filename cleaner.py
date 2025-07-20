import csv, re, os, sys

INPUT_TSV      = "original_dataset.tsv"
OUTPUT_TSV     = "cleaned_dataset.tsv"


# Regular expressions for various checks

ENG_LETTER_RE     = re.compile(r"[A-Za-z]")
DEV_START, DEV_END = 0x0900, 0x097F
ANGLE_RE           = re.compile(r"[<>]")
REPEATED_PUNCT_RE  = re.compile(r'([!"#\$%&\'\(\)\*\+,\-./:;<=>\?@\[\]\\\^_`{\|}~])\1{5,}')
HTML_TAG_RE        = re.compile(r"<\s*[^>]+>")
SHAPE_RE           = re.compile(r"[\u25A0-\u25FF]")
EMOJI_RE           = re.compile(
    r"[\U0001F300-\U0001F5FF"  
    r"\U0001F600-\U0001F64F"  
    r"\U0001F680-\U0001F6FF"   
    r"\U0001F900-\U0001F9FF]"   
)

REPEATED_NUM_RE    = re.compile(r"(?:\d+)(?:\D+\d+){5,}")            
BRACKET_NUM_RE     = re.compile(r"(?:\[\d+\])(?:\s*\[\d+\]){5,}") 
REPEATED_WORD_RE   = re.compile(r"\b(\w+)(?:[,\s]+\1){2,}", re.IGNORECASE)
REPEATED_PHRASE_RE = re.compile(r"\b(.{3,}?)\s+\1\s+\1", re.IGNORECASE)


# Functions to check various conditions in the text

def has_english(s):      return bool(ENG_LETTER_RE.search(s))
def count_deva(s):       return sum(DEV_START <= ord(ch) <= DEV_END for ch in s)
def has_hindi(s):        return count_deva(s) >= 2
def has_angle(s):        return bool(ANGLE_RE.search(s))
def has_rep_punct(s):    return bool(REPEATED_PUNCT_RE.search(s))
def has_html(s):         return bool(HTML_TAG_RE.search(s))
def has_shape(s):        return bool(SHAPE_RE.search(s))
def has_emoji(s):        return bool(EMOJI_RE.search(s))
def has_rep_num(s):      return bool(REPEATED_NUM_RE.search(s) or BRACKET_NUM_RE.search(s))
def has_rep_word(s):     return bool(REPEATED_WORD_RE.search(s))
def has_rep_phrase(s):   return bool(REPEATED_PHRASE_RE.search(s))
def is_empty(s):         return (s is None) or (not s.strip())


# Initialize counts for various conditions

counts = {
    "total":              0,
    "empty_src":          0,
    "empty_tgt":          0,
    "bad_src_eng":        0,
    "bad_src_hindi":      0,
    "bad_tgt_hindi":      0,
    "angle":              0,
    "html":               0,
    "rep_punct":          0,
    "rep_punct_tgt":      0,
    "shape":              0,
    "emoji":              0,
    "rep_num":            0,
    "rep_word":           0,
    "rep_phrase":         0,
}


# Main processing loop

with open(INPUT_TSV, encoding="utf-8", newline="") as fin, \
     open(OUTPUT_TSV, "w", encoding="utf-8", newline="") as fout:

    reader = csv.reader(fin, delimiter="\t")
    writer = csv.writer(fout, delimiter="\t")

    for row in reader:
        counts["total"] += 1
        if len(row) < 2:
            continue
        src, tgt = row[0], row[1]
        if is_empty(src):
            counts["empty_src"] += 1; continue
        if is_empty(tgt):
            counts["empty_tgt"] += 1; continue
        if has_english(src):
            counts["bad_src_eng"] += 1; continue
        if has_hindi(src):
            counts["bad_src_hindi"] += 1; continue
        if has_hindi(tgt):
            counts["bad_tgt_hindi"] += 1; continue
        if has_angle(src) or has_angle(tgt):
            counts["angle"] += 1; continue
        if has_html(src) or has_html(tgt):
            counts["html"] += 1; continue
        if has_rep_punct(src):
            counts["rep_punct"] += 1; continue
        if has_rep_punct(tgt):
            counts["rep_punct_tgt"] += 1; continue
        if has_shape(src) or has_shape(tgt):
            counts["shape"] += 1; continue
        if has_emoji(src) or has_emoji(tgt):
            counts["emoji"] += 1; continue
        if has_rep_num(src) or has_rep_num(tgt):
            counts["rep_num"] += 1; continue
        if has_rep_word(src) or has_rep_word(tgt):
            counts["rep_word"] += 1; continue
        if has_rep_phrase(tgt):
            counts["rep_phrase"] += 1; continue
        writer.writerow([src, tgt])
kept = counts["total"] - sum(v for k,v in counts.items() if k!="total")

# Print summary of counts and kept rows

print(f"Total rows processed     : {counts['total']}")
print(f"Empty src                : {counts['empty_src']}")
print(f"Empty tgt                : {counts['empty_tgt']}")
print(f"Src with English letters : {counts['bad_src_eng']}")
print(f"Src with Hindi           : {counts['bad_src_hindi']}")
print(f"Tgt with Hindi           : {counts['bad_tgt_hindi']}")
print(f"Angle brackets           : {counts['angle']}")
print(f"HTML tags                : {counts['html']}")
print(f"Rep. punct in src        : {counts['rep_punct']}")
print(f"Rep. punct in tgt        : {counts['rep_punct_tgt']}")
print(f"Geometric shapes         : {counts['shape']}")
print(f"Emojis                    : {counts['emoji']}")
print(f"Rep. numbers             : {counts['rep_num']}")
print(f"Rep. single word         : {counts['rep_word']}")
print(f"Rep. phrase in tgt       : {counts['rep_phrase']}")
print(f"Rows kept                : {kept}")
print(f"Cleaned data written to: {OUTPUT_TSV}")