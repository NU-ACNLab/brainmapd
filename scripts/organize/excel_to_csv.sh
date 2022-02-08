### This script converts excel files to csv
###
### Brooke Feinstein
### February 8, 2022

#https://linux.die.net/man/1/unoconv

xlsx_files=`find /path/to/brainmapd/acnl/ -name "*.xlsx"`

for xlsx_file in ${xlsx_files}; do
	unoconv -f csv ${xlsx_file}
done

# Notes
# 1) Check where you are writing out files to before
# running for loop
