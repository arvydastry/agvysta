#!/bin/sh
# iCloud Drive (Optimize Mac Storage) gali iškelti failus į debesį ("dataless"), tada serveris juos grąžina tuščius.
# Šis skriptas parsiunčia visus projekto failus atgal į diską. Naudojimas: sh tools/hydrate.sh
cd "$(dirname "$0")/.." || exit 1
for i in 1 2 3 4 5 6 7 8 9 10; do
  left=$(find assets content templates tools *.html *.py -type f -flags +dataless 2>/dev/null)
  [ -z "$left" ] && { echo "visi failai diske"; exit 0; }
  echo "$left" | while read -r f; do brctl download "$f" >/dev/null 2>&1; done
  sleep 4
done
echo "dar liko: $(find assets content templates tools *.html *.py -type f -flags +dataless 2>/dev/null | wc -l)"
