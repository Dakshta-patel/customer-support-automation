\# Hiver Customer Support Agent



A customer-support automation and evaluation project built using the Customer Support on Twitter dataset.



\## Objective



The goal is to build a support agent that can:



\- Understand customer-support queries

\- Identify support intents

\- Retrieve relevant historical resolutions

\- Generate grounded responses

\- Decide when a case should be escalated

\- Evaluate response quality using a labelled golden set

\- Compare the system against simple baselines

\- Measure response quality using automated and human evaluation



\## Project Status



Initial project setup.



\## Planned Components



\- Dataset inspection

\- Brand selection

\- Intent definition

\- Historical-resolution retrieval

\- Response generation

\- Escalation classification

\- Golden-set creation

\- Baseline systems

\- LLM-as-judge evaluation

\- Human agreement analysis

\- Final report

\- Decision log



\## Project Structure



```text

hiver-support-agent/

│

├── backend/

│   └── app/

│       ├── \_\_init\_\_.py

│       └── main.py

│

├── data/

│   ├── raw/

│   ├── processed/

│   └── golden\_set/

│

├── docs/

│   └── decision\_log.md

│

├── reports/

├── tests/

├── requirements.txt

├── README.md

└── .gitignore

