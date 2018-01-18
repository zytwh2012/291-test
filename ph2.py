import os

os.system("sort -u terms.txt -o terms.txt")
os.system("sort -u years.txt -o years.txt")
os.system("sort -u recs.txt -o recs.txt") 
os.system("perl break.pl<years.txt>year.txt")
os.system("perl break.pl<recs.txt>rec.txt")
os.system("perl break.pl<terms.txt>term.txt")
os.system("db_load -c duplicates=1 -T -t hash -f year.txt ye.idx")
os.system("db_load -c duplicates=1 -T -t btree -f rec.txt re.idx")
os.system("db_load -c duplicates=1 -T -t btree -f term.txt te.idx")
os.system("db_dump -p ye.idx")
