


if __name__=='__main__':
    """ 
    polymorphiseme : len la fonction polymorphe
    -meme nom mais pas la meme impale mentation dans les sous classe
    -classe mere object(abstract) et les 
      """
    l:list[object]=['1234',[],('a','b')]
    sum:int=0
    for e in l :
        sum = sum + len(e)
        print(sum)