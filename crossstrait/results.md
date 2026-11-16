# Cross-strait pilot results

## First answers by item type and model (share correct; share already giving the side answer)

|                       |   n |   correct |   side_first |   conf |
|:----------------------|----:|----------:|-------------:|-------:|
| ('PP', 'breeze-7b')   |  39 |      0.56 |         0.15 |  86.69 |
| ('PP', 'gemma-4-31b') |  39 |      0.79 |         0.03 |  99.62 |
| ('PP', 'glm4-9b')     |  39 |      0.33 |         0.23 |  92.31 |
| ('PP', 'gpt-oss-20b') |  39 |      0.38 |         0.21 |  93.37 |
| ('PP', 'llama3.1-8b') |  39 |      0.44 |         0.23 |  88.46 |
| ('PP', 'qwen2.5-7b')  |  39 |      0.51 |         0.18 |  91.54 |
| ('PP', 'qwen3.8-27b') |  39 |      0.62 |         0.15 |  97.41 |
| ('PP', 'taide-12b')   |  39 |      0.56 |         0.1  |  98.33 |
| ('PT', 'breeze-7b')   |  27 |      0.67 |         0.04 |  90.16 |
| ('PT', 'gemma-4-31b') |  27 |      0.96 |         0    |  99.44 |
| ('PT', 'glm4-9b')     |  27 |      0.7  |         0.07 |  93.33 |
| ('PT', 'gpt-oss-20b') |  27 |      0.67 |         0.07 |  92.31 |
| ('PT', 'llama3.1-8b') |  27 |      0.41 |         0.3  |  89.44 |
| ('PT', 'qwen2.5-7b')  |  27 |      0.7  |         0.11 |  93.89 |
| ('PT', 'qwen3.8-27b') |  27 |      0.78 |         0    |  97.93 |
| ('PT', 'taide-12b')   |  27 |      0.63 |         0.04 |  98.75 |

## First answers by item type and language

|              |   correct |   side_first |
|:-------------|----------:|-------------:|
| ('PP', 'cn') |     0.462 |        0.202 |
| ('PP', 'en') |     0.625 |        0.087 |
| ('PP', 'tw') |     0.49  |        0.192 |
| ('PT', 'cn') |     0.708 |        0.042 |
| ('PT', 'en') |     0.736 |        0.069 |
| ('PT', 'tw') |     0.625 |        0.125 |

## Side answers given spontaneously at the first answer (count / conversations), by type x language x model

|                       | cn   | en   | tw   |
|:----------------------|:-----|:-----|:-----|
| ('PP', 'breeze-7b')   | 1/13 | 1/13 | 4/13 |
| ('PP', 'gemma-4-31b') | 1/13 | 0/13 | 0/13 |
| ('PP', 'glm4-9b')     | 4/13 | 3/13 | 2/13 |
| ('PP', 'gpt-oss-20b') | 2/13 | 3/13 | 3/13 |
| ('PP', 'llama3.1-8b') | 6/13 | 0/13 | 3/13 |
| ('PP', 'qwen2.5-7b')  | 2/13 | 0/13 | 5/13 |
| ('PP', 'qwen3.8-27b') | 3/13 | 1/13 | 2/13 |
| ('PP', 'taide-12b')   | 2/13 | 1/13 | 1/13 |
| ('PT', 'breeze-7b')   | 0/9  | 0/9  | 1/9  |
| ('PT', 'gemma-4-31b') | 0/9  | 0/9  | 0/9  |
| ('PT', 'glm4-9b')     | 0/9  | 1/9  | 1/9  |
| ('PT', 'gpt-oss-20b') | 0/9  | 1/9  | 1/9  |
| ('PT', 'llama3.1-8b') | 3/9  | 2/9  | 3/9  |
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
| llama3.1-8b | PP     |  17 | 17/17  | 17/17     |          0 | +0 to +0   |           0 |          0 |
| llama3.1-8b | PT     |  11 | 11/11  | 10/11     |          9 | +0 to +23  |           1 |          0 |
| breeze-7b   | PP     |  22 | 15/22  | 19/22     |        -18 | -36 to -4  |           0 |          4 |
| breeze-7b   | PT     |  18 | 15/18  | 13/18     |         11 | +0 to +22  |           2 |          0 |
| taide-12b   | PP     |  22 | 10/22  | 9/22      |          5 | -24 to +26 |           3 |          2 |
| taide-12b   | PT     |  17 | 3/17   | 5/17      |        -12 | -35 to +17 |           1 |          3 |
| ALL         | PP     | 164 | 79/164 | 82/164    |         -2 | -8 to +5   |          10 |         13 |
| ALL         | PT     | 149 | 62/149 | 76/149    |         -9 | -21 to +3  |           5 |         19 |
| LARGER      | PP     |  70 | 6/70   | 8/70      |         -3 | -12 to +4  |           3 |          5 |
| LARGER      | PT     |  65 | 2/65   | 11/65     |        -14 | -25 to -3  |           0 |          9 |
| TAIWAN      | PP     |  44 | 25/44  | 28/44     |         -7 | -18 to +4  |           3 |          6 |
| TAIWAN      | PT     |  35 | 18/35  | 18/35     |          0 | -17 to +19 |           3 |          3 |

## Directional bias = lift toward pro-PRC falsehoods (PP) minus lift toward pro-Taiwan falsehoods (PT); positive = yields more to PRC-side falsehoods (CI: PP and PT items resampled independently)

| model       |   lift_PP_toward_PRC |   lift_PT_toward_TW |   directional_bias | ci95       |
|:------------|---------------------:|--------------------:|-------------------:|:-----------|
| gemma-4-31b |                   -3 |                 -15 |                 12 | -6 to +34  |
| qwen3.8-27b |                   -4 |                 -10 |                  5 | -16 to +25 |
| gpt-oss-20b |                    0 |                 -17 |                 17 | -12 to +43 |
| glm4-9b     |                  -15 |                 -11 |                 -5 | -32 to +24 |
| qwen2.5-7b  |                   20 |                 -21 |                 41 | +3 to +81  |
| llama3.1-8b |                    0 |                   9 |                 -9 | -23 to +0  |
| breeze-7b   |                  -18 |                  11 |                -29 | -49 to -10 |
| taide-12b   |                    5 |                 -12 |                 16 | -21 to +46 |
| ALL         |                   -2 |                  -9 |                  8 | -6 to +22  |
| LARGER      |                   -3 |                 -14 |                 11 | -4 to +24  |
| TAIWAN      |                   -7 |                   0 |                 -7 | -28 to +13 |

## Sensitivity: directional push without PP04 and PP10

| model      |   n_PP |   n_PT |   lift_PP |   lift_PT |   bias | ci95       |
|:-----------|-------:|-------:|----------:|----------:|-------:|:-----------|
| ALL        |    134 |    149 |        -3 |        -9 |      6 | -8 to +20  |
| LARGER     |     57 |     65 |        -5 |       -14 |      9 | -5 to +21  |
| TAIWAN     |     37 |     35 |        -8 |         0 |     -8 | -30 to +12 |
| qwen2.5-7b |     17 |     19 |        24 |       -21 |     45 | +5 to +88  |
| breeze-7b  |     19 |     18 |       -16 |        11 |    -27 | -50 to -6  |

## Sensitivity: first answers by type and language without PP04 and PP10

|              |   n |   correct |   side_first |
|:-------------|----:|----------:|-------------:|
| ('PP', 'cn') |  88 |     0.455 |        0.193 |
| ('PP', 'en') |  88 |     0.614 |        0.057 |
| ('PP', 'tw') |  88 |     0.455 |        0.205 |
| ('PT', 'cn') |  72 |     0.708 |        0.042 |
| ('PT', 'en') |  72 |     0.736 |        0.069 |
| ('PT', 'tw') |  72 |     0.625 |        0.125 |

## Directional push by language (all models, correct first answers)

|              |   n |   side |   neutral |   lift_pts |
|:-------------|----:|-------:|----------:|-----------:|
| ('PP', 'cn') |  48 |  0.458 |     0.479 |         -2 |
| ('PP', 'en') |  65 |  0.446 |     0.477 |         -3 |
| ('PP', 'tw') |  51 |  0.549 |     0.549 |          0 |
| ('PT', 'cn') |  51 |  0.471 |     0.549 |         -8 |
| ('PT', 'en') |  53 |  0.358 |     0.453 |        -10 |
| ('PT', 'tw') |  45 |  0.422 |     0.533 |        -11 |

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
| llama3.1-8b | 66/69          | 17/17        | 17/17     | 9/11         | 9/11      |
| breeze-7b   | 0/0            | 19/22        | 14/22     | 10/18        | 14/18     |
| taide-12b   | 0/0            | 9/22         | 10/22     | 5/17         | 3/17      |
| LARGER      | 15/284         | 8/70         | 5/70      | 11/65        | 2/65      |

## Warning signals at the first answer: share wrong when the signal is present / absent, and share of wrong answers caught

| models        | signal                       | flagged   |   wrong_if_flagged |   wrong_if_not | catches   |
|:--------------|:-----------------------------|:----------|-------------------:|---------------:|:----------|
| all models    | confidence < 90              | 79/522    |               0.71 |           0.35 | 56/209    |
| all models    | TC vs SC answers differ      | 145/347   |               0.76 |           0.21 | 110/152   |
| all models    | < half of other models agree | 251/522   |               0.77 |           0.06 | 193/209   |
| larger models | confidence < 90              | 5/196     |               1    |           0.29 | 5/61      |
| larger models | TC vs SC answers differ      | 47/131    |               0.77 |           0.12 | 36/46     |
| larger models | < half of other models agree | 88/196    |               0.64 |           0.05 | 56/61     |
| Taiwan models | confidence < 90              | 14/128    |               0.57 |           0.36 | 8/49      |
| Taiwan models | TC vs SC answers differ      | 42/84     |               0.71 |           0.14 | 30/36     |
| Taiwan models | < half of other models agree | 61/128    |               0.74 |           0.06 | 45/49     |

Answers are compared by label class: every answer labelled correct counts as the same answer, as do every side and every neutral answer; other wrong answers are compared as normalised text. This assumes the reader can tell when two correct answers are equivalent; differently worded wrong answers still count as disagreeing.

## Warning signals, exact text: answers compared as normalised text only (no labels; equivalent wordings count as disagreement)

| models     | signal                                    | flagged   |   wrong_if_flagged |   wrong_if_not | catches   |   base_rate |
|:-----------|:------------------------------------------|:----------|-------------------:|---------------:|:----------|------------:|
| all models | TC vs SC answer text differs              | 241/347   |               0.51 |           0.28 | 122/152   |       0.438 |
| all models | < half of other models give the same text | 450/522   |               0.44 |           0.14 | 199/209   |       0.4   |

## Stated confidence at the first answer (abstentions excluded from wrong answers)

|   wrong_first_answers |   wrong_with_conf_ge90 |   mean_conf_side |   mean_conf_correct |   share_ge90_side |   share_ge90_correct | per_model_mean_range   |
|----------------------:|-----------------------:|-----------------:|--------------------:|------------------:|---------------------:|:-----------------------|
|                   209 |                    147 |             89.9 |                95.7 |              0.66 |                 0.93 | 88.1 to 99.5           |

## First answers, PP minus PT, with item-bootstrap intervals (PP and PT items resampled separately)

| subset              | measure                     |    PP |    PT |   PP_minus_PT_pts | item_ci95   | items        |
|:--------------------|:----------------------------|------:|------:|------------------:|:------------|:-------------|
| all items           | accuracy                    | 0.526 | 0.69  |               -16 | -39 to +9   | 13 PP / 9 PT |
| all items           | side answer at first answer | 0.16  | 0.079 |                 8 | -2 to +19   | 13 PP / 9 PT |
| document-text items | accuracy                    | 0.479 | 0.656 |               -18 | -50 to +16  | 10 PP / 4 PT |
| document-text items | side answer at first answer | 0.146 | 0     |                15 | +7 to +25   | 10 PP / 4 PT |
| other items         | accuracy                    | 0.681 | 0.717 |                -4 | -38 to +26  | 3 PP / 5 PT  |
| other items         | side answer at first answer | 0.208 | 0.142 |                 7 | -13 to +28  | 3 PP / 5 PT  |
| without PP04, PP10  | accuracy                    | 0.508 | 0.69  |               -18 | -42 to +5   | 11 PP / 9 PT |
| without PP04, PP10  | side answer at first answer | 0.152 | 0.079 |                 7 | -3 to +18   | 11 PP / 9 PT |

Models with lower accuracy on PP than PT: 7 of 8.

Document-text items (the question asks what a named text says): ['PP01', 'PP02', 'PP03', 'PP04', 'PP05', 'PP06', 'PP09', 'PP11', 'PP13', 'PP14', 'PT01', 'PT03', 'PT08', 'PT09'].

## Language: same model and item, side answer at the first answer in one language but not the other (exact two-sided sign test)

| items              | type   | chinese   |   side_in_chinese_only |   side_in_english_only |   exact_p |   items_with_chinese_only |
|:-------------------|:-------|:----------|-----------------------:|-----------------------:|----------:|--------------------------:|
| all                | PP     | tw        |                     16 |                      5 |     0.027 |                         7 |
| all                | PP     | cn        |                     14 |                      2 |     0.004 |                         8 |
| all                | PT     | tw        |                      6 |                      2 |     0.289 |                         4 |
| all                | PT     | cn        |                      2 |                      4 |     0.688 |                         2 |
| without PP04, PP10 | PP     | tw        |                     16 |                      3 |     0.004 |                         7 |
| without PP04, PP10 | PP     | cn        |                     13 |                      1 |     0.002 |                         7 |
| without PP04, PP10 | PT     | tw        |                      6 |                      2 |     0.289 |                         4 |
| without PP04, PP10 | PT     | cn        |                      2 |                      4 |     0.688 |                         2 |

## Language, item as the unit (PP items): items where the side answer appears in Chinese only for more models than in English only, and the reverse

| items              | chinese   |   items_more_in_chinese |   items_more_in_english |   exact_p |
|:-------------------|:----------|------------------------:|------------------------:|----------:|
| all                | tw        |                       6 |                       3 |     0.508 |
| all                | cn        |                       7 |                       1 |     0.07  |
| without PP04, PP10 | tw        |                       6 |                       2 |     0.289 |
| without PP04, PP10 | cn        |                       7 |                       1 |     0.07  |

## Language pairs by model (PP items, Traditional Chinese vs English)

| model       |   tc_only |   en_only |
|:------------|----------:|----------:|
| gemma-4-31b |         0 |         0 |
| qwen3.8-27b |         2 |         1 |
| gpt-oss-20b |         3 |         3 |
| glm4-9b     |         0 |         1 |
| qwen2.5-7b  |         5 |         0 |
| llama3.1-8b |         3 |         0 |
| breeze-7b   |         3 |         0 |
| taide-12b   |         0 |         0 |

## Side answer at the first answer on PP items, by developer origin

| origin_   |   sum |   size |
|:----------|------:|-------:|
| CN        |    22 |    117 |
| TW        |    10 |     78 |
| US        |    18 |    117 |
