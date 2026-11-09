import re
"""
regular expression
expr* : exp 0or many times
expr+ : exp 1 or more time
exp? : exp 0 or 1 times
expr {n} : expr n time
^expr : start with expr
exp$ : ends with expr
(expr1|expr2):expr1 or exper2
 [0-9] : interval 0 or 1 or 2,.. 9
 [a-zA-Z] :alphabetic char down or upper case
/d : digit
/w :alphabetic char
/s : space,/t, /n
/D : not a digit
/W : not alphabetic char
/S : not space
. : any char

"""

text="""
M123456,hanine,2006,l.hanine@gmail.com
MN789123,yassine,2004,a.yassine@esisa.ac.ma
"""

#match =re.search(r'(.*,)(.*,)(?P<date>\d{4})',text)
pattern = re.compile(r'(.*,),(.*,),(?P<date>\d{4})')

"""match: match[str] | None=re.search(pattern,text)
if match :
    print(match.groupdict(3),match.start(),match.end())"""
#results = re.findall(pattern,text)
#findall vs. finditer
"""for match in results:
    print(match[0],match[2])"""
matches = re.finditer(pattern,text)

for match in matches:
    print(match.group(1),match.group(2))