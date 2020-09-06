SIMPLE COMMANDS:
================
echo hello
grep "123" TestFolder/testing2.txt
ls
cd
pwd

INVALID COMMANDS:
=================
rm -r invalidFileName


COMPLEX COMMANDS 
===================
--> PIPE OPERATOR
cat TestFolder/testing1.txt | tail -n 11

--> REDIRECTION FUNCTION
head -n 10 < TestFolder/testing1.txt

--> SEQUENCE OF COMMANDS
echo hi; echo ho ; echo he

--> BACKTICKS OPERATOR
wc -l `find -name 'testing1.txt'`
 
--> REGULAR EXPRESSIONS 
cat TestFolder/testing*.txt