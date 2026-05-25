# Research Protocol: Quantitative Content Analysis
## News Coverage of Modern Day Marine 2026
### Using ProQuest Newsstream + Claude AI

---

## Overview

This protocol guides you through collecting, coding, and analyzing news articles about
the Modern Day Marine 2026 conference in Washington, D.C. using a hybrid workflow
combining ProQuest Newsstream, pq_parser, and Claude AI.

**Estimated corpus size:** ~320 articles  
**Estimated total API cost:** $0.50–$2.50  
**Tools required:** ProQuest library access, Claude Pro subscription, Python, Claude Code

---

## Phase 1: Preparation (Do This First)

### Step 1 — Finalize Your Codebook

Before collecting a single article, make sure your codebook is substantially complete.
You do not need it to be perfect, but the core variables and categories should be defined.

- Review each variable for clarity and mutual exclusivity of categories
- Note any variables that may require judgment calls — these will need extra attention
  when writing the coding prompt
- Save your codebook as a Word or PDF document

### Step 2 — Translate Your Codebook Into a Claude Coding Prompt

Share your codebook with Claude on claude.ai and ask:

> *"Help me turn this codebook into a structured system prompt for use with the
> Anthropic Batch API. Each article will be submitted individually, and I need
> Claude to return a JSON object with one field per variable."*

Work through the prompt iteratively until every variable is clearly defined and the
output format is consistent. Save the finalized prompt — you will paste it into your
batch processing script later.

**Example output format to aim for:**
```json
{
  "article_id": "001",
  "topic_focus": "equipment",
  "tone": "neutral",
  "source_types": ["military official", "industry representative"],
  "framing": "thematic",
  "geographic_focus": "national"
}
```

### Step 3 — Install Claude Code

1. Go to claude.ai and confirm you have a Pro subscription ($20/month or higher)
2. Download the Claude Code desktop app for your operating system (macOS or Windows)
   from the Claude Code documentation page, or install via your terminal
3. Windows users: install Git for Windows first if you do not already have it
4. Open Claude Code, authenticate with your Anthropic account via the one-time
   OAuth process
5. Confirm Claude Code is working by opening it in any folder and typing a test
   message

### Step 4 — Confirm Python Is Installed

Open a terminal (or ask Claude Code to check) and type:
```
python --version
```
You need Python 3.7 or higher. If it is not installed, download it from python.org
or ask Claude Code to walk you through installation.

---

## Phase 2: Corpus Collection

### Step 5 — Search ProQuest Newsstream

Log into ProQuest via your university library and navigate to U.S. Newsstream and/or
International Newsstream.

**Suggested search strategy:**
- Search terms: `"Modern Day Marine"` — use exact phrase search (quotes)
- Date range: set the start date approximately one week before the conference
  opens and extend two to three weeks after it closes to capture advance coverage
  and post-event reporting
- Source filters: apply any outlet-type filters your research design calls for
  (e.g., newspapers only, exclude wire services, etc.)
- Review the result count — if well over 320, consider narrowing by date range,
  outlet type, or geography; if under 320, consider widening

**Document your search decisions.** Record the exact search string, date range,
and any filters applied. This is essential for your methods section.

### Step 6 — Export as Full-Text File

1. Select all results (or your filtered sample)
2. Click the export/save button
3. Choose **Text file (.txt)** as the format — not CSV or Excel
4. When prompted for content options, select **Full text**
5. Complete the export — ProQuest will either download the file directly or email
   it to you depending on result size
6. Save the .txt file to a dedicated project folder on your computer
   (e.g., `MDM2026_Research/`)

> **Note:** ProQuest allows up to 10,000 results exported twice per day. Your
> corpus of ~320 articles is well within this limit.

---

## Phase 3: Corpus Preparation

### Step 7 — Parse the ProQuest Export Into a Structured CSV

Open Claude Code in your project folder and say:

> *"I have a ProQuest Newsstream text export file called [filename.txt] in this
> folder. Please download the pq_parser tool from
> https://github.com/chennesy/pq_parser, install any required Python libraries,
> run it on my file, and save the output as articles.csv with one row per article
> including all metadata fields and the full article text."*

Claude Code will handle the download, dependency installation, and parsing. When
it finishes, confirm that `articles.csv` exists in your project folder and open it
to spot-check that:

- Each row is a single article
- The full text column is populated (not blank)
- Metadata fields (headline, publication, date, author) look correct

### Step 8 — Clean and Review the Dataset

Ask Claude Code:

> *"Please review articles.csv and tell me: how many articles are there, are there
> any rows with missing full text, any obvious duplicates, and do the publication
> dates fall within my expected date range?"*

Address any issues Claude Code flags — remove true duplicates, note articles with
missing text. Document how many articles remain after cleaning. This becomes your
final N for the methods section.

### Step 9 — Assign Article IDs

If pq_parser did not assign unique IDs, ask Claude Code to add an `article_id`
column with sequential numbers (001, 002, 003...). This is essential for merging
your coded output back to the original data later.

---

## Phase 4: Pilot Testing

### Step 10 — Draw a Pilot Sample

Ask Claude Code to randomly select 25–30 articles from your dataset and save them
as `pilot_sample.csv`. Using a random sample (rather than the first 25 articles)
is better practice and more defensible methodologically.

### Step 11 — Hand-Code the Pilot Sample

Set aside time to manually code all 25–30 pilot articles yourself using your
codebook. Record your codes in a spreadsheet with the article ID and one column
per variable. Save this as `human_coded_pilot.csv`.

This step cannot be skipped — it is what allows you to measure how well Claude's
coding matches your own judgment.

### Step 12 — Have Claude Code the Pilot Sample

Return to claude.ai and say:

> *"Here is my coding prompt [paste prompt] and here are 30 articles [paste or
> upload pilot_sample.csv]. Please code each article and return a table with one
> row per article and one column per variable."*

Save Claude's output as `claude_coded_pilot.csv`.

### Step 13 — Calculate Intercoder Reliability

Upload both `human_coded_pilot.csv` and `claude_coded_pilot.csv` to claude.ai
and ask:

> *"Please calculate Cohen's Kappa for each variable comparing the human codes to
> Claude's codes. Present the results in a table and flag any variable below 0.80."*

**Interpreting results:**
- κ ≥ 0.80: Strong agreement — proceed with this variable
- κ 0.67–0.79: Moderate agreement — review coding prompt definition for that
  variable and consider revising before the full run
- κ < 0.67: Poor agreement — the variable definition needs significant revision;
  re-test before proceeding

### Step 14 — Revise and Re-Test If Needed

For any variable below threshold, review the cases where you and Claude disagreed.
Look for patterns — is Claude misunderstanding a category boundary? Is the
definition ambiguous? Revise the relevant portion of your coding prompt and
re-run the pilot. Repeat until all variables reach acceptable reliability.

Document which version of the coding prompt was used for the final run.

---

## Phase 5: Full Corpus Coding

### Step 15 — Set Up the Batch API Script

In Claude Code, say:

> *"I want to code all 320 articles in articles.csv using the Anthropic Batch API.
> Here is my finalized coding prompt: [paste prompt]. Please write a Python script
> that reads each article from the CSV, submits all articles as a single batch
> job using claude-haiku-4-5, and saves the coded results as coded_output.csv
> with the article_id and one column per coding variable."*

Review the script with Claude Code before running it. Ask it to explain what the
script does in plain English if anything is unclear.

> **Model guidance:** Use claude-haiku-4-5 for straightforward categorical coding
> (fastest and cheapest). Use claude-sonnet-4-6 if your variables involve nuanced
> judgment like framing or narrative tone.

### Step 16 — Set Up Your API Key

You will need an Anthropic API key to run the batch script (separate from your
Claude Pro login). To get one:

1. Go to console.anthropic.com
2. Create an account or log in
3. Navigate to API Keys and generate a new key
4. Add a small amount of credit (a few dollars is more than sufficient)
5. Provide the key to Claude Code when prompted — it will store it securely

### Step 17 — Run the Batch Job

Ask Claude Code to run the script. The batch will be submitted to Anthropic and
processed asynchronously — typically within a few minutes for a corpus this size,
though up to 24 hours is possible. Claude Code can monitor the job status and
notify you when it is complete.

### Step 18 — Merge and Validate the Output

When the batch completes, ask Claude Code:

> *"Please merge coded_output.csv with articles.csv on article_id, check that all
> 320 articles received codes and no rows are missing, and save the merged file
> as final_dataset.csv."*

Spot-check 10–15 rows manually to confirm the codes look reasonable.

---

## Phase 6: Analysis

### Step 19 — Descriptive Statistics

Upload `final_dataset.csv` to claude.ai and begin your analysis conversationally.
Start with basic frequencies and distributions:

> *"Give me a frequency table for each categorical variable showing counts and
> percentages."*

> *"Which topic categories were most common? Show this as a bar chart."*

> *"How did coverage volume vary by day across the conference period?"*

### Step 20 — Inferential Analysis

Move to relationships between variables:

> *"Is there a statistically significant relationship between outlet type and
> tone? Run a chi-square test and interpret the result."*

> *"Do national outlets and regional outlets differ significantly in their topic
> focus? Test this and report the appropriate statistic."*

Claude will run the tests, report the statistics, and interpret the findings in
plain language.

### Step 21 — Visualizations

Ask Claude to generate charts for any findings you want to present:

> *"Create a stacked bar chart showing framing types broken down by publication,
> with a clean professional style suitable for a research paper."*

Charts can be downloaded directly from the conversation.

---

## Phase 7: Documentation

### Step 22 — Write Your Methods Section

Your methods section should document:

- **Search strategy:** exact search terms, databases, date range, filters applied
- **Corpus size:** initial results, any exclusions, final N after cleaning
- **Codebook:** define every variable and its categories (can be included as an
  appendix)
- **Coding procedure:** describe that AI-assisted coding was used, identify the
  model, include the coding prompt as an appendix or supplementary file
- **Reliability:** report Cohen's Kappa for each variable with the pilot sample
  size; note any variables revised after piloting
- **Analysis:** describe the statistical tests used

Being transparent about AI-assisted coding is increasingly standard in the field.
Describe it the same way you would describe using a trained human coder — note the
"coder," the training process (prompt development and piloting), and the reliability
achieved.

### Step 23 — Archive Your Materials

Before considering the project complete, save and archive:

- [ ] Original ProQuest .txt export file
- [ ] articles.csv (cleaned corpus)
- [ ] Codebook document
- [ ] Finalized coding prompt (text file)
- [ ] pilot_sample.csv
- [ ] human_coded_pilot.csv and claude_coded_pilot.csv
- [ ] Reliability table
- [ ] final_dataset.csv
- [ ] Analysis scripts or conversation logs
- [ ] All figures and charts

---

## Quick Reference: Tools and Accounts Needed

| Tool | Purpose | Cost |
|---|---|---|
| ProQuest Newsstream | Article collection | Free via university library |
| claude.ai (Pro) | Codebook development, analysis | $20/month |
| Claude Code | Parsing, scripting, batch setup | Included with Pro |
| Anthropic API key | Running the batch coding job | ~$1–3 for this project |
| Python | Running pq_parser and batch script | Free |

---

*Protocol developed for Modern Day Marine 2026 coverage study.*  
*Generated with Claude Sonnet 4.6 on April 26, 2026.*
