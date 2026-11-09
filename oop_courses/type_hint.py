"""
since python 3.5
-lisibilite du code
-type check in TDK vscode
"""

b:bool=True
i:int=10
pi:float=22/7
adn:str='AAAADDDDBBBBCCCC'

l:list[str]=['a','b']
t:tuple[int,...]=(3,4,)
d:dict[str,float]={'fes':20.5,'1':3}

#create new type
Vector=list[float]
v:Vector=[3,4,5.1]
from typin import(
    Any,
    Final,
    Optional,
    Union
)
var:Any=[]
MAX:Final[int]=100
opt:Optional[str]=''
val:Union[list[int],str]=[]

