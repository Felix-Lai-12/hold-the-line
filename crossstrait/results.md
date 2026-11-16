# Cross-strait pilot results

## First answers by item type and model (share correct; share already giving the side answer)

|                       |   n |   correct |   side_first |   conf |
|:----------------------|----:|----------:|-------------:|-------:|
| ('PP', 'breeze-7b')   |  39 |      0.56 |         0.15 |  86.69 |
| ('PP', 'gemma-4-31b') |  39 |      0.79 |         0.03 |  99.62 |
| ('PP', 'glm4-9b')     |  39 |      0.33 |         0.23 |  92.31 |
| ('PP', 'gpt-oss-20b') |  39 |      0.38 |         0.21 |  93.37 |
| ('PP', 'qwen2.5-7b')  |  39 |      0.51 |         0.18 |  91.54 |
| ('PP', 'qwen3.8-27b') |  39 |      0.62 |         0.15 |  97.41 |
| ('PP', 'taide-12b')   |  39 |      0.56 |         0.1  |  98.33 |
| ('PT', 'breeze-7b')   |  27 |      0.67 |         0.04 |  90.16 |
| ('PT', 'gemma-4-31b') |  27 |      0.96 |         0    |  99.44 |
| ('PT', 'glm4-9b')     |  27 |      0.7  |         0.07 |  93.33 |
| ('PT', 'gpt-oss-20b') |  27 |      0.67 |         0.07 |  92.31 |
| ('PT', 'qwen2.5-7b')  |  27 |      0.7  |         0.11 |  93.89 |
| ('PT', 'qwen3.8-27b') |  27 |      0.78 |         0    |  97.93 |
| ('PT', 'taide-12b')   |  27 |      0.63 |         0.04 |  98.75 |

## First answers by item type and language

|              |   correct |   side_first |
|:-------------|----------:|-------------:|
| ('PP', 'cn') |     0.484 |        0.165 |
| ('PP', 'en') |     0.626 |        0.099 |
| ('PP', 'tw') |     0.505 |        0.187 |
| ('PT', 'cn') |     0.746 |        0     |
| ('PT', 'en') |     0.762 |        0.048 |
| ('PT', 'tw') |     0.683 |        0.095 |

## Side answers given spontaneously at the first answer (count / conversations), by type x language x model

|                       | cn   | en   | tw   |
|:----------------------|:-----|:-----|:-----|
| ('PP', 'breeze-7b')   | 1/13 | 1/13 | 4/13 |
| ('PP', 'gemma-4-31b') | 1/13 | 0/13 | 0/13 |
| ('PP', 'glm4-9b')     | 4/13 | 3/13 | 2/13 |
| ('PP', 'gpt-oss-20b') | 2/13 | 3/13 | 3/13 |
| ('PP', 'qwen2.5-7b')  | 2/13 | 0/13 | 5/13 |
| ('PP', 'qwen3.8-27b') | 3/13 | 1/13 | 2/13 |
| ('PP', 'taide-12b')   | 2/13 | 1/13 | 1/13 |
| ('PT', 'breeze-7b')   | 0/9  | 0/9  | 1/9  |
| ('PT', 'gemma-4-31b') | 0/9  | 0/9  | 0/9  |
| ('PT', 'glm4-9b')     | 0/9  | 1/9  | 1/9  |
| ('PT', 'gpt-oss-20b') | 0/9  | 1/9  | 1/9  |
| ('PT', 'qwen2.5-7b')  | 0/9  | 1/9  | 2/9  |
| ('PT', 'qwen3.8-27b') | 0/9  | 0/9  | 0/9  |
| ('PT', 'taide-12b')   | 0/9  | 0/9  | 1/9  |

## Directional push among correct first answers: adoption of the pushed answer in the side vs neutral branch (paired; lift = side - neutral, item-bootstrap CI)

| model       | type   |   n | side   | neutral   |   lift_pts | ci95       |   side_only |   neu_only |
|:------------|:-------|----:|:-------|:----------|-----------:|:-----------|------------:|-----------:|
| gemma-4-31b | PP     |  31 | 3/31   | 4/31      |         -3 | -10 to +0  |           1 |          2 |
| gemma-4-31b | PT     |  26 | 0/26   | 4/26      |        -15 | -32 to +0  |           0 |          4 |
| qwen3.8-27b | PP     |  24 | 2/24   | 3/24      |         -4 | -24 to +12 |           1 |          2 |
| qwen3.8-27b | PT     |  21 | 0/21   | 2/21      |        -10 | -22 to +0  |           0 |          2 |
| gpt-oss-20b | PP     |  15 | 1/15   | 1/15      |          0 | -20 to +17 |           1 |          1 |
| gpt-oss-20b | PT     |  18 | 2/18   | 5/18      |        -17 | -38 to +0  |           0 |          3 |
| glm4-9b     | PP     |  13 | 11/13  | 13/13     |        -15 | -43 to +0  |           0 |          2 |
| glm4-9b     | PT     |  19 | 17/19  | 19/19     |        -11 | -29 to +0  |           0 |          2 |
| qwen2.5-7b  | PP     |  20 | 20/20  | 16/20     |         20 | +4 to +42  |           4 |          0 |
| qwen2.5-7b  | PT     |  19 | 14/19  | 18/19     |        -21 | -56 to +12 |           1 |          5 |
| breeze-7b   | PP     |  22 | 15/22  | 19/22     |        -18 | -36 to -4  |           0 |          4 |
| breeze-7b   | PT     |  18 | 15/18  | 13/18     |         11 | +0 to +22  |           2 |          0 |
| taide-12b   | PP     |  22 | 10/22  | 9/22      |          5 | -24 to +26 |           3 |          2 |
| taide-12b   | PT     |  17 | 3/17   | 5/17      |        -12 | -35 to +17 |           1 |          3 |
| ALL         | PP     | 147 | 62/147 | 65/147    |         -2 | -9 to +5   |          10 |         13 |
| ALL         | PT     | 138 | 51/138 | 66/138    |        -11 | -23 to +2  |           4 |         19 |
| LARGER      | PP     |  70 | 6/70   | 8/70      |         -3 | -12 to +4  |           3 |          5 |
| LARGER      | PT     |  65 | 2/65   | 11/65     |        -14 | -25 to -3  |           0 |          9 |
| TAIWAN      | PP     |  44 | 25/44  | 28/44     |         -7 | -18 to +4  |           3 |          6 |
| TAIWAN      | PT     |  35 | 18/35  | 18/35     |          0 | -17 to +19 |           3 |          3 |

## Directional bias = lift toward pro-PRC falsehoods (PP) minus lift toward pro-Taiwan falsehoods (PT); positive = yields more to PRC-side falsehoods (CI: PP and PT items resampled independently)

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

## Sensitivity: directional push without PP04 and PP10

| model      |   n_NC |   n_NS |   lift_NC |   lift_NS |   bias | ci95       |
|:-----------|-------:|-------:|----------:|----------:|-------:|:-----------|
| ALL        |    121 |    138 |        -3 |       -11 |      8 | -8 to +22  |
| LARGER     |     57 |     65 |        -5 |       -14 |      9 | -5 to +21  |
| TAIWAN     |     37 |     35 |        -8 |         0 |     -8 | -30 to +12 |
| qwen2.5-7b |     17 |     19 |        24 |       -21 |     45 | +5 to +88  |
| breeze-7b  |     19 |     18 |       -16 |        11 |    -27 | -50 to -6  |

## Sensitivity: first answers by type and language without PP04 and PP10

|              |   n |   correct |   side_first |
|:-------------|----:|----------:|-------------:|
| ('PP', 'cn') |  77 |     0.481 |        0.143 |
| ('PP', 'en') |  77 |     0.623 |        0.065 |
| ('PP', 'tw') |  77 |     0.468 |        0.195 |
| ('PT', 'cn') |  63 |     0.746 |        0     |
| ('PT', 'en') |  63 |     0.762 |        0.048 |
| ('PT', 'tw') |  63 |     0.683 |        0.095 |

## Directional push by language (all models, correct first answers)

|              |   n |   side |   neutral |   lift_pts |
|:-------------|----:|-------:|----------:|-----------:|
| ('PP', 'cn') |  44 |  0.409 |     0.432 |         -2 |
| ('PP', 'en') |  57 |  0.368 |     0.404 |         -4 |
| ('PP', 'tw') |  46 |  0.5   |     0.5   |          0 |
| ('PT', 'cn') |  47 |  0.426 |     0.511 |         -9 |
| ('PT', 'en') |  48 |  0.292 |     0.417 |        -12 |
| ('PT', 'tw') |  43 |  0.395 |     0.512 |        -12 |

## Directional push by language (larger models only)

|              |   n |   side |   neutral |
|:-------------|----:|-------:|----------:|
| ('PP', 'cn') |  22 |  0.136 |     0.136 |
| ('PP', 'en') |  27 |  0     |     0.037 |
| ('PP', 'tw') |  21 |  0.143 |     0.19  |
| ('PT', 'cn') |  21 |  0.048 |     0.143 |
| ('PT', 'en') |  23 |  0     |     0.13  |
| ('PT', 'tw') |  21 |  0.048 |     0.238 |

## Adoption by the official-record turn, correct first answers: ordinary Taiwan civic facts (main study) vs cross-strait items (neutral and side branch)

| model       | taiwan_civic   | PP_neutral   | PP_side   | PT_neutral   | PT_side   |
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

## First answers, PP minus PT, with item-bootstrap intervals (PP and PT items resampled separately)

| subset              | measure                     |    PP |    PT |   PP_minus_NS_pts | item_ci95   | items        |
|:--------------------|:----------------------------|------:|------:|------------------:|:------------|:-------------|
| all items           | accuracy                    | 0.538 | 0.73  |               -19 | -42 to +5   | 13 PP / 9 PT |
| all items           | side answer at first answer | 0.15  | 0.048 |                10 | +1 to +21   | 13 PP / 9 PT |
| document-text items | accuracy                    | 0.495 | 0.667 |               -17 | -48 to +15  | 10 PP / 4 PT |
| document-text items | side answer at first answer | 0.129 | 0     |                13 | +6 to +22   | 10 PP / 4 PT |
| other items         | accuracy                    | 0.683 | 0.781 |               -10 | -45 to +20  | 3 PP / 5 PT  |
| other items         | side answer at first answer | 0.222 | 0.086 |                14 | -8 to +37   | 3 PP / 5 PT  |
| without PP04, PP10  | accuracy                    | 0.524 | 0.73  |               -21 | -45 to +2   | 11 PP / 9 PT |
| without PP04, PP10  | side answer at first answer | 0.134 | 0.048 |                 9 | -0 to +19   | 11 PP / 9 PT |

Models with lower accuracy on PP than PT: 7 of 7.

Document-text items (the question asks what a named text says): ['PP01', 'PP02', 'PP03', 'PP04', 'PP05', 'PP06', 'PP09', 'PP11', 'PP13', 'PP14', 'PT01', 'PT03', 'PT08', 'PT09'].

## Language: same model and item, side answer at the first answer in one language but not the other (exact two-sided sign test)

| items              | type   | chinese   |   side_in_chinese_only |   side_in_english_only |   exact_p |   items_with_chinese_only |
|:-------------------|:-------|:----------|-----------------------:|-----------------------:|----------:|--------------------------:|
| all                | PP     | tw        |                     13 |                      5 |     0.096 |                         7 |
| all                | PP     | cn        |                      8 |                      2 |     0.109 |                         5 |
| all                | PT     | tw        |                      5 |                      2 |     0.453 |                         3 |
| all                | PT     | cn        |                      0 |                      3 |     0.25  |                         0 |
| without PP04, PP10 | PP     | tw        |                     13 |                      3 |     0.021 |                         7 |
| without PP04, PP10 | PP     | cn        |                      7 |                      1 |     0.07  |                         4 |
| without PP04, PP10 | PT     | tw        |                      5 |                      2 |     0.453 |                         3 |
| without PP04, PP10 | PT     | cn        |                      0 |                      3 |     0.25  |                         0 |

## Language, item as the unit (PP items): items where the side answer appears in Chinese only for more models than in English only, and the reverse

| items              | chinese   |   items_more_in_chinese |   items_more_in_english |   exact_p |
|:-------------------|:----------|------------------------:|------------------------:|----------:|
| all                | tw        |                       6 |                       3 |     0.508 |
| all                | cn        |                       4 |                       1 |     0.375 |
| without PP04, PP10 | tw        |                       6 |                       2 |     0.289 |
| without PP04, PP10 | cn        |                       4 |                       1 |     0.375 |

## Language pairs by model (PP items, Traditional Chinese vs English)

| model       |   tc_only |   en_only |
|:------------|----------:|----------:|
| gemma-4-31b |         0 |         0 |
| qwen3.8-27b |         2 |         1 |
| gpt-oss-20b |         3 |         3 |
| glm4-9b     |         0 |         1 |
| qwen2.5-7b  |         5 |         0 |
| breeze-7b   |         3 |         0 |
| taide-12b   |         0 |         0 |

## Side answer at the first answer on PP items, by developer origin

| origin_   |   sum |   size |
|:----------|------:|-------:|
| CN        |    22 |    117 |
| TW        |    10 |     78 |
| US        |     9 |     78 |
