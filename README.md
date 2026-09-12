# Customer Support Automation Agent

A customer-support automation pipeline built using the Kaggle **Customer Support on Twitter** dataset.

The project classifies customer messages into support intents, decides whether the message can be handled automatically or should be escalated, and generates a response draft for the customer.

## 1. Problem Statement

Customer-support teams receive a large number of repetitive messages related to:

- Delivery and shipment issues
- Refunds and cancellations
- Product replacements
- Prime membership and billing
- Account and order privacy
- Technical and device issues
- Digital content
- General feedback

The goal is to build a lightweight support automation pipeline that:

1. Understands the customer’s intent.
2. Decides whether the request can be auto-handled or escalated.
3. Generates a suitable response draft.
4. Evaluates the system on a manually labelled golden set.

This is a prototype for evaluation and experimentation, not a production customer-support system.

---

## 2. Dataset

The project uses the Kaggle dataset:

**Customer Support on Twitter**

Source:

https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter

The original dataset contains Twitter customer-support conversations with the following fields:

- `tweet_id`
- `author_id`
- `inbound`
- `created_at`
- `text`
- `response_tweet_id`
- `in_response_to_tweet_id`

### Dataset processing

The pipeline:

1. Profiles the raw dataset.
2. Selects the `AmazonHelp` support account.
3. Extracts customer messages and brand responses.
4. Builds customer-support conversation pairs.
5. Classifies the customer messages.
6. Generates support-agent outputs.

Raw and generated datasets are intentionally excluded from Git because of their size.

---

## 3. Project Structure

```text
.
├── backend/
│   └── app/
│       ├── __init__.py
│       └── main.py
├── data/
│   ├── golden_set/
│   │   ├── golden_set_labeled.csv
│   │   └── golden_set_template.csv
│   ├── processed/
│   └── raw/
├── docs/
│   └── decision_log.md
├── scripts/
│   ├── 01_profile_dataset.py
│   ├── 02_extract_brand_data.py
│   ├── 03_build_conversations.py
│   ├── 04_inspect_conversations.py
│   ├── 05_keyword_classifier.py
│   ├── 06_create_golden_set.py
│   ├── 07_evaluate_baselines.py
│   ├── 08_support_agent.py
│   ├── 09_tfidf_baseline.py
│   ├── 10_evaluate_agent.py
│   ├── 12_llm_judge.py
│   └── 13_evaluate_judge_agreement.py
├── .env.example
├── .gitignore
├── REPORT.md
├── README.md
└── requirements.txt