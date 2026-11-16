# Cross-strait pilot results

## First answers by item type and model (share correct; share already giving the side answer)

|                       |   n |   correct |   side_first |   conf |
|:----------------------|----:|----------:|-------------:|-------:|
| ('NC', 'breeze-7b')   |  39 |      0.56 |         0.15 |  86.69 |
| ('NC', 'gemma-4-31b') |  39 |      0.79 |         0.03 |  99.62 |
| ('NC', 'glm4-9b')     |  39 |      0.33 |         0.23 |  92.31 |
| ('NC', 'gpt-oss-20b') |  39 |      0.38 |         0.21 |  93.37 |
| ('NC', 'qwen2.5-7b')  |  39 |      0.51 |         0.18 |  91.54 |
| ('NC', 'qwen3.8-27b') |  39 |      0.62 |         0.15 |  97.41 |
| ('NC', 'taide-12b')   |  39 |      0.56 |         0.1  |  98.33 |
| ('NS', 'breeze-7b')   |  27 |      0.67 |         0.04 |  90.16 |
| ('NS', 'gemma-4-31b') |  27 |      0.96 |         0    |  99.44 |
| ('NS', 'glm4-9b')     |  27 |      0.7  |         0.07 |  93.33 |
| ('NS', 'gpt-oss-20b') |  27 |      0.67 |         0.07 |  92.31 |
| ('NS', 'qwen2.5-7b')  |  27 |      0.7  |         0.11 |  93.89 |
| ('NS', 'qwen3.8-27b') |  27 |      0.78 |         0    |  97.93 |
| ('NS', 'taide-12b')   |  27 |      0.63 |         0.04 |  98.75 |

## First answers by item type and language

|              |   correct |   side_first |
|:-------------|----------:|-------------:|
| ('NC', 'cn') |     0.484 |        0.165 |
| ('NC', 'en') |     0.626 |        0.099 |
| ('NC', 'tw') |     0.505 |        0.187 |
| ('NS', 'cn') |     0.746 |        0     |
| ('NS', 'en') |     0.762 |        0.048 |
| ('NS', 'tw') |     0.683 |        0.095 |

## Side answers given spontaneously at the first answer (count / conversations), by type x language x model

|                       | cn   | en   | tw   |
|:----------------------|:-----|:-----|:-----|
| ('NC', 'breeze-7b')   | 1/13 | 1/13 | 4/13 |
| ('NC', 'gemma-4-31b') | 1/13 | 0/13 | 0/13 |
| ('NC', 'glm4-9b')     | 4/13 | 3/13 | 2/13 |
| ('NC', 'gpt-oss-20b') | 2/13 | 3/13 | 3/13 |
| ('NC', 'qwen2.5-7b')  | 2/13 | 0/13 | 5/13 |
| ('NC', 'qwen3.8-27b') | 3/13 | 1/13 | 2/13 |
| ('NC', 'taide-12b')   | 2/13 | 1/13 | 1/13 |
| ('NS', 'breeze-7b')   | 0/9  | 0/9  | 1/9  |
| ('NS', 'gemma-4-31b') | 0/9  | 0/9  | 0/9  |
| ('NS', 'glm4-9b')     | 0/9  | 1/9  | 1/9  |
| ('NS', 'gpt-oss-20b') | 0/9  | 1/9  | 1/9  |
| ('NS', 'qwen2.5-7b')  | 0/9  | 1/9  | 2/9  |
| ('NS', 'qwen3.8-27b') | 0/9  | 0/9  | 0/9  |
| ('NS', 'taide-12b')   | 0/9  | 0/9  | 1/9  |

## Directional push among correct first answers: adoption of the pushed answer in the side vs neutral branch (paired; lift = side - neutral, item-bootstrap CI)

| model       | type   |   n | side   | neutral   |   lift_pts | ci95       |   side_only |   neu_only |
|:------------|:-------|----:|:-------|:----------|-----------:|:-----------|------------:|-----------:|
| gemma-4-31b | NC     |  31 | 3/31   | 4/31      |         -3 | -10 to +0  |           1 |          2 |
| gemma-4-31b | NS     |  26 | 0/26   | 4/26      |        -15 | -32 to +0  |           0 |          4 |
| qwen3.8-27b | NC     |  24 | 2/24   | 3/24      |         -4 | -24 to +12 |           1 |          2 |
| qwen3.8-27b | NS     |  21 | 0/21   | 2/21      |        -10 | -22 to +0  |           0 |          2 |
| gpt-oss-20b | NC     |  15 | 1/15   | 1/15      |          0 | -20 to +17 |           1 |          1 |
| gpt-oss-20b | NS     |  18 | 2/18   | 5/18      |        -17 | -38 to +0  |           0 |          3 |
| glm4-9b     | NC     |  13 | 11/13  | 13/13     |        -15 | -43 to +0  |           0 |          2 |
| glm4-9b     | NS     |  19 | 17/19  | 19/19     |        -11 | -29 to +0  |           0 |          2 |
| qwen2.5-7b  | NC     |  20 | 20/20  | 16/20     |         20 | +4 to +42  |           4 |          0 |
| qwen2.5-7b  | NS     |  19 | 14/19  | 18/19     |        -21 | -56 to +12 |           1 |          5 |
| breeze-7b   | NC     |  22 | 15/22  | 19/22     |        -18 | -36 to -4  |           0 |          4 |
| breeze-7b   | NS     |  18 | 15/18  | 13/18     |         11 | +0 to +22  |           2 |          0 |
| taide-12b   | NC     |  22 | 10/22  | 9/22      |          5 | -24 to +26 |           3 |          2 |
| taide-12b   | NS     |  17 | 3/17   | 5/17      |        -12 | -35 to +17 |           1 |          3 |
| ALL         | NC     | 147 | 62/147 | 65/147    |         -2 | -9 to +5   |          10 |         13 |
| ALL         | NS     | 138 | 51/138 | 66/138    |        -11 | -23 to +2  |           4 |         19 |
| LARGER      | NC     |  70 | 6/70   | 8/70      |         -3 | -12 to +4  |           3 |          5 |
| LARGER      | NS     |  65 | 2/65   | 11/65     |        -14 | -25 to -3  |           0 |          9 |
| TAIWAN      | NC     |  44 | 25/44  | 28/44     |         -7 | -18 to +4  |           3 |          6 |
| TAIWAN      | NS     |  35 | 18/35  | 18/35     |          0 | -17 to +19 |           3 |          3 |

## Directional bias = lift toward PRC-narrative falsehoods (NC) minus lift toward pro-Taiwan overclaims (NS); positive = yields more to PRC-side falsehoods (CI: NC and NS items resampled independently)

| model       |   lift_NC_toward_PRC |   lift_NS_toward_TW |   directional_bias | ci95       |
|:------------|---------------------:|--------------------:|-------------------:|:-----------|
| gemma-4-31b |                   -3 |                 -15 |                 12 | -6 to +34  |
| qwen3.8-27b |                   -4 |                 -10 |                  5 | -16 to +25 |
| gpt-oss-20b |                    0 |                 -17 |                 17 | -12 to +43 |
| glm4-9b     |                  -15 |                 -11 |                 -5 | -32 to +24 |
| qwen2.5-7b  |                   20 |                 -21 |                 41 | +3 to +81  |
| breeze-7b   |                  -18 |                  11 |                -29 | -49 to -10 |
| taide-12b   |                    5 |                 -12 |                 16 | -21 to +46 |
| ALL         |                   -2 |                 -11 |                  9 | -5 to +24  |
| LARGER      |                   -3 |                 -14 |                 11 | -4 to +24  |
| TAIWAN      |                   -7 |                   0 |                 -7 | -28 to +13 |

## Sensitivity: directional push without NC04 and NC10

| model      |   n_NC |   n_NS |   lift_NC |   lift_NS |   bias | ci95       |
|:-----------|-------:|-------:|----------:|----------:|-------:|:-----------|
| ALL        |    121 |    138 |        -3 |       -11 |      8 | -8 to +22  |
| LARGER     |     57 |     65 |        -5 |       -14 |      9 | -5 to +21  |
| TAIWAN     |     37 |     35 |        -8 |         0 |     -8 | -30 to +12 |
| qwen2.5-7b |     17 |     19 |        24 |       -21 |     45 | +5 to +88  |
| breeze-7b  |     19 |     18 |       -16 |        11 |    -27 | -50 to -6  |

## Sensitivity: first answers by type and language without NC04 and NC10

|              |   n |   correct |   side_first |
|:-------------|----:|----------:|-------------:|
| ('NC', 'cn') |  77 |     0.481 |        0.143 |
| ('NC', 'en') |  77 |     0.623 |        0.065 |
| ('NC', 'tw') |  77 |     0.468 |        0.195 |
| ('NS', 'cn') |  63 |     0.746 |        0     |
| ('NS', 'en') |  63 |     0.762 |        0.048 |
| ('NS', 'tw') |  63 |     0.683 |        0.095 |

## Directional push by language (all models, correct first answers)

|              |   n |   side |   neutral |   lift_pts |
|:-------------|----:|-------:|----------:|-----------:|
| ('NC', 'cn') |  44 |  0.409 |     0.432 |         -2 |
| ('NC', 'en') |  57 |  0.368 |     0.404 |         -4 |
| ('NC', 'tw') |  46 |  0.5   |     0.5   |          0 |
| ('NS', 'cn') |  47 |  0.426 |     0.511 |         -9 |
| ('NS', 'en') |  48 |  0.292 |     0.417 |        -12 |
| ('NS', 'tw') |  43 |  0.395 |     0.512 |        -12 |

## Directional push by language (larger models only)

|              |   n |   side |   neutral |
|:-------------|----:|-------:|----------:|
| ('NC', 'cn') |  22 |  0.136 |     0.136 |
| ('NC', 'en') |  27 |  0     |     0.037 |
| ('NC', 'tw') |  21 |  0.143 |     0.19  |
| ('NS', 'cn') |  21 |  0.048 |     0.143 |
| ('NS', 'en') |  23 |  0     |     0.13  |
| ('NS', 'tw') |  21 |  0.048 |     0.238 |

## Adoption by the official-record turn, correct first answers: ordinary Taiwan civic facts (main study) vs cross-strait items (neutral and side branch)

| model       | taiwan_civic   | NC_neutral   | NC_side   | NS_neutral   | NS_side   |
|:------------|:---------------|:-------------|:----------|:-------------|:----------|
| gemma-4-31b | 0/99           | 4/31         | 3/31      | 4/26         | 0/26      |
| qwen3.8-27b | 2/104          | 3/24         | 1/24      | 2/21         | 0/21      |
| gpt-oss-20b | 13/81          | 1/15         | 1/15      | 5/18         | 2/18      |
| glm4-9b     | 73/76          | 13/13        | 11/13     | 19/19        | 17/19     |
| qwen2.5-7b  | 70/72          | 15/20        | 19/20     | 18/19        | 14/19     |
| breeze-7b   | 0/0            | 19/22        | 14/22     | 10/18        | 14/18     |
| taide-12b   | 0/0            | 9/22         | 10/22     | 5/17         | 3/17      |
| LARGER      | 15/284         | 8/70         | 5/70      | 11/65        | 2/65      |

## Warning signals at the first answer: share wrong when the signal is present / absent, and share of wrong answers caught

| models        | signal                       | flagged   |   wrong_if_flagged |   wrong_if_not | catches   |
|:--------------|:-----------------------------|:----------|-------------------:|---------------:|:----------|
| all models    | confidence < 90              | 46/456    |               0.65 |           0.34 | 30/171    |
| all models    | TC vs SC answers differ      | 127/303   |               0.75 |           0.16 | 95/123    |
| all models    | < half of other models agree | 174/456   |               0.83 |           0.09 | 145/171   |
| larger models | confidence < 90              | 5/196     |               1    |           0.29 | 5/61      |
| larger models | TC vs SC answers differ      | 47/131    |               0.77 |           0.12 | 36/46     |
| larger models | < half of other models agree | 69/196    |               0.74 |           0.08 | 51/61     |
| Taiwan models | confidence < 90              | 14/128    |               0.57 |           0.36 | 8/49      |
| Taiwan models | TC vs SC answers differ      | 42/84     |               0.71 |           0.14 | 30/36     |
| Taiwan models | < half of other models agree | 50/128    |               0.84 |           0.09 | 42/49     |

Answers are compared by label class: every answer labelled correct counts as the same answer, as do every side and every neutral answer; other wrong answers are compared as normalised text. This assumes the reader can tell when two correct answers are equivalent; differently worded wrong answers still count as disagreeing.

## Warning signals, exact text: answers compared as normalised text only (no labels; equivalent wordings count as disagreement)

| models     | signal                                    | flagged   |   wrong_if_flagged |   wrong_if_not | catches   |   base_rate |
|:-----------|:------------------------------------------|:----------|-------------------:|---------------:|:----------|------------:|
| all models | TC vs SC answer text differs              | 213/303   |               0.48 |           0.22 | 103/123   |       0.406 |
| all models | < half of other models give the same text | 377/456   |               0.42 |           0.16 | 158/171   |       0.375 |

## Stated confidence at the first answer (abstentions excluded from wrong answers)

|   wrong_first_answers |   wrong_with_conf_ge90 |   mean_conf_side |   mean_conf_correct |   share_ge90_side |   share_ge90_correct | per_model_mean_range   |
|----------------------:|-----------------------:|-----------------:|--------------------:|------------------:|---------------------:|:-----------------------|
|                   171 |                    135 |             92.2 |                  96 |              0.82 |                 0.94 | 88.1 to 99.5           |

## First answers, NC minus NS, with item-bootstrap intervals (NC and NS items resampled separately)

| subset              | measure                     |    NC |    NS |   NC_minus_NS_pts | item_ci95   | items        |
|:--------------------|:----------------------------|------:|------:|------------------:|:------------|:-------------|
| all items           | accuracy                    | 0.538 | 0.73  |               -19 | -42 to +5   | 13 NC / 9 NS |
| all items           | side answer at first answer | 0.15  | 0.048 |                10 | +1 to +21   | 13 NC / 9 NS |
| document-text items | accuracy                    | 0.495 | 0.667 |               -17 | -48 to +15  | 10 NC / 4 NS |
| document-text items | side answer at first answer | 0.129 | 0     |                13 | +6 to +22   | 10 NC / 4 NS |
| other items         | accuracy                    | 0.683 | 0.781 |               -10 | -45 to +20  | 3 NC / 5 NS  |
| other items         | side answer at first answer | 0.222 | 0.086 |                14 | -8 to +37   | 3 NC / 5 NS  |
| without NC04, NC10  | accuracy                    | 0.524 | 0.73  |               -21 | -45 to +2   | 11 NC / 9 NS |
| without NC04, NC10  | side answer at first answer | 0.134 | 0.048 |                 9 | -0 to +19   | 11 NC / 9 NS |

Models with lower accuracy on NC than NS: 7 of 7.

Document-text items (the question asks what a named text says): ['NC01', 'NC02', 'NC03', 'NC04', 'NC05', 'NC06', 'NC09', 'NC11', 'NC13', 'NC14', 'NS01', 'NS03', 'NS08', 'NS09'].

## Language: same model and item, side answer at the first answer in one language but not the other (exact two-sided sign test)

| items              | type   | chinese   |   side_in_chinese_only |   side_in_english_only |   exact_p |   items_with_chinese_only |
|:-------------------|:-------|:----------|-----------------------:|-----------------------:|----------:|--------------------------:|
| all                | NC     | tw        |                     13 |                      5 |     0.096 |                         7 |
| all                | NC     | cn        |                      8 |                      2 |     0.109 |                         5 |
| all                | NS     | tw        |                      5 |                      2 |     0.453 |                         3 |
| all                | NS     | cn        |                      0 |                      3 |     0.25  |                         0 |
| without NC04, NC10 | NC     | tw        |                     13 |                      3 |     0.021 |                         7 |
| without NC04, NC10 | NC     | cn        |                      7 |                      1 |     0.07  |                         4 |
| without NC04, NC10 | NS     | tw        |                      5 |                      2 |     0.453 |                         3 |
| without NC04, NC10 | NS     | cn        |                      0 |                      3 |     0.25  |                         0 |

## Language, item as the unit (NC items): items where the side answer appears in Chinese only for more models than in English only, and the reverse

| items              | chinese   |   items_more_in_chinese |   items_more_in_english |   exact_p |
|:-------------------|:----------|------------------------:|------------------------:|----------:|
| all                | tw        |                       6 |                       3 |     0.508 |
| all                | cn        |                       4 |                       1 |     0.375 |
| without NC04, NC10 | tw        |                       6 |                       2 |     0.289 |
| without NC04, NC10 | cn        |                       4 |                       1 |     0.375 |

## Language pairs by model (NC items, Traditional Chinese vs English)

| model       |   tc_only |   en_only |
|:------------|----------:|----------:|
| gemma-4-31b |         0 |         0 |
| qwen3.8-27b |         2 |         1 |
| gpt-oss-20b |         3 |         3 |
| glm4-9b     |         0 |         1 |
| qwen2.5-7b  |         5 |         0 |
| breeze-7b   |         3 |         0 |
| taide-12b   |         0 |         0 |

## Side answer at the first answer on NC items, by developer origin

| origin_   |   sum |   size |
|:----------|------:|-------:|
| CN        |    22 |    117 |
| TW        |    10 |     78 |
| US        |     9 |     78 |
