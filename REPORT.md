\# Customer Support Automation Report



\## 1. Problem



The goal of this project is to build a lightweight customer-support

automation pipeline that can classify customer messages and decide whether

a message can receive an automated response or should be escalated to a

human support agent.



The system is designed for public customer-support conversations and does

not attempt to expose or infer private customer information.



\---



\## 2. Dataset



The project uses the Customer Support on Twitter dataset.



The pipeline filters the data for the selected support brand and builds

customer-support conversation pairs from customer messages and brand

responses.



The main processing stages are:



1\. Dataset profiling

2\. Brand filtering

3\. Conversation-pair construction

4\. Conversation inspection

5\. Keyword-based classification

6\. Golden-set creation

7\. Baseline evaluation

8\. Support-agent response generation

9\. TF-IDF baseline evaluation

10\. Final agent evaluation



\---



\## 3. Intent Taxonomy



The system uses the following intents:



\- `delivery\_issue`

\- `delivery\_date\_confusion`

\- `refund\_cancellation`

\- `product\_replacement`

\- `prime\_membership\_billing`

\- `account\_order\_privacy`

\- `technical\_device\_issue`

\- `digital\_content\_support`

\- `general\_feedback`



The taxonomy was intentionally kept small and operational so that each

intent can be connected to a practical support action.



\---



\## 4. Handling Decisions



Each message receives one of two handling decisions:



\### `auto\_handle`



The message receives a safe, generic response based on the predicted intent.



The response does not request private order information in public.



\### `escalate`



The message is directed to private support or human review.



Escalation is used for messages involving potentially sensitive, account-

specific, technical, replacement, or digital-content issues.



\---



\## 5. System Design



The current implementation is a deterministic baseline.



The main components are:



\- Pandas for data processing

\- Keyword matching for intent classification

\- Rule-based escalation

\- Template-based response generation

\- Scikit-learn metrics for evaluation

\- Optional TF-IDF and Logistic Regression baseline



This design was selected because it is:



\- Easy to inspect

\- Easy to debug

\- Low cost

\- Deterministic

\- Suitable for a first support-automation prototype



\---



\## 6. Evaluation



The main evaluation uses the manually labeled golden set.



The following metrics are reported:



\- Intent accuracy

\- Intent macro F1

\- Handling-decision accuracy

\- Handling-decision macro F1

\- Classification reports

\- Confusion matrices

\- Majority baseline accuracy

\- Handling mismatches

\- Agent-output validation



Run the evaluation with:



```powershell

python scripts\\10\_evaluate\_agent.py

