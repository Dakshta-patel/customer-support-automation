\## Baseline evaluation



We evaluated the keyword-based intent classifier on a 180-example golden set covering 9 customer-support intents.



| Baseline | Accuracy | Macro F1 |

|---|---:|---:|

| Keyword classifier | 95.56% | 95.54% |

| Majority-class baseline | 12.78% | 2.52% |



The keyword classifier substantially outperformed the majority-class baseline. The main observed weaknesses were delivery-date confusion and overlap between general delivery issues and delivery-date questions.



These results are preliminary because the golden-set labels were initially assisted by heuristic rules and require human verification before being treated as final ground truth.

