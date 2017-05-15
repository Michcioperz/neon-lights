#!/bin/bash
source params.sh
if [ ! -f my_display_name ]; then
  echo "my_display_name file not existing"
  exit 1
fi
rm -f .new_status-swp .new_status-content
vim .new_status-content
touch .new_status-swp
echo "Author-Id: $(ipfs id -f='<id>')" >> .new_status-swp
echo "Author-Display-Name: $(cat my_display_name)" >> .new_status-swp
if [ -f .previous_status ]; then
  echo "Previous: $(cat .previous_status)" >> .new_status-swp
fi
echo "Date-Time: $(date -Iseconds)" >> .new_status-swp
echo >> .new_status-swp
cat .new_status-content >> .new_status-swp
./ipfs add --quieter --pin .new_status-swp > .previous_status
./ipfs name publish $(cat .previous_status)
