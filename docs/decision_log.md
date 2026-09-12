\# Decision Log



\## 1. Use a deterministic baseline first



A deterministic keyword-based system was selected before introducing a

larger machine-learning or LLM-based solution.



Reason:



\- Easy to inspect

\- Easy to debug

\- Low cost

\- Predictable behavior

\- Suitable for a first prototype



\---



\## 2. Keep the intent taxonomy small



The system uses nine operational intents instead of a very large taxonomy.



Reason:



\- Easier to label

\- Easier to evaluate

\- Easier to connect with response templates

\- Reduces overlap between categories



\---



\## 3. Separate intent from handling decision



Intent and handling decision are separate fields.



For example, two messages can have the same intent but different handling

decisions depending on whether the issue appears account-specific or

sensitive.



\---



\## 4. Escalate sensitive requests



Account, privacy, security, unauthorized-charge, and order-specific issues

are candidates for escalation.



Reason:



Public support messages should not request or expose private details.



\---



\## 5. Use generic response templates



The system uses generic responses instead of pretending that a refund,

replacement, or account change has already been completed.



Reason:



The prototype does not have access to real customer accounts or support

systems.



\---



\## 6. Avoid public collection of private information



Responses direct customers to private support when account, order, billing,

or security details are needed.



Reason:



This reduces the risk of exposing sensitive information in public replies.



\---



\## 7. Use a manually labeled golden set



A manually labeled golden set is used to evaluate intent and handling

decisions.



Reason:



Automatic evaluation against keyword-generated labels would not provide an

independent quality measurement.



\---



\## 8. Report macro F1



Macro F1 is reported in addition to accuracy.



Reason:



Accuracy alone can hide poor performance on less frequent intents.



\---



\## 9. Include a majority baseline



The evaluation includes a corpus-majority intent baseline.



Reason:



The model should be compared against a simple baseline rather than

reporting accuracy alone.



\---



\## 10. Add a TF-IDF baseline



A TF-IDF plus Logistic Regression baseline is included as a second approach.



Reason:



It provides a comparison with a simple statistical machine-learning model.



The result is treated as a development comparison because the golden set is

small.



\---



\## 11. Keep the response generation deterministic



The response is generated from the predicted intent and handling decision.



Reason:



The same input should produce the same response, which makes debugging and

evaluation easier.



\---



\## 12. Validate generated output fields



The agent output is checked for:



\- Customer message

\- Predicted intent

\- Handling decision

\- Agent action

\- Agent response



Reason:



A classification result is not sufficient if the downstream agent output

is incomplete.



\---



\## 13. Do not overfit to individual golden-set examples



The classifier rules were not changed only to fix every individual golden-set

mismatch.



Reason:



Overfitting a small labeled set can reduce generalization to unseen

messages.



\---



\## 14. Treat multilingual cases as a known limitation



Messages in languages other than English may be misclassified by the current

keyword rules.



Reason:



The current baseline does not use a multilingual language model.



\---



\## 15. Keep raw and generated data out of Git



The raw dataset and generated intermediate files are excluded through

`.gitignore`.



Reason:



The raw dataset is large and generated files can be recreated by running

the pipeline.

