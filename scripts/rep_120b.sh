#!/bin/sh
# Repeat run of gpt-oss-120b for run-to-run variance (Groq quota is 200k tokens/day, rolling).
# Waits until 08:00 Taipei on 2026-11-16, then runs Taiwan + matched-local items in Traditional and
# Simplified Chinese; reruns every 30 min (run.py resumes and retries errored conversations) until
# no errors remain or 15:00.
cd "$(dirname "$0")/.." || exit 1
start=$(date -j -f "%Y-%m-%d %H:%M" "2026-11-16 08:00" +%s); stop=$(date -j -f "%Y-%m-%d %H:%M" "2026-11-16 15:00" +%s)
while [ "$(date +%s)" -lt "$start" ]; do sleep 300; done
IDS=$(python3 -c "import json;print(' '.join([i['id'] for i in json.load(open('data/items.json')) if i['id'].startswith('T')]+[i['id'] for i in json.load(open('data/items_local.json'))]))")
while [ "$(date +%s)" -lt "$stop" ]; do
  .venv/bin/python src/run.py --models gpt-oss-120b --outdir runs/rep2 --ids $IDS --langs tw cn --workers 2
  left=$(python3 -c "
import json
r=[json.loads(l) for l in open('runs/rep2/gpt-oss-120b.jsonl')]
ok={(x['item'],x['lang']) for x in r if not any(t['raw'].startswith('__ERROR__') for t in x['turns'])}
print(118-len(ok))")
  echo "$(date '+%F %T') remaining: $left"
  [ "$left" -le 0 ] && break
  sleep 1800
done
sed -i '' -E 's/org_[0-9a-z]{20,}/org_REDACTED/g' runs/rep2/*.jsonl
echo finished
