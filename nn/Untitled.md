### Sorting

* Heap Sort

* Quick Sort

  * psuedocode

  ```pseudocode
  Quicksort(A,l,h):
      if l < h :
         p <- Partition(A,l,h)
         Quicksort(A,l,p)
         Quicksort(A,p+1,h)
  
  Partition(A,l,h):
  	// p <- Random(l, h)
      // pivot <- A[p]
      pivot <- A[l]
      i <- l-1
      for j=l; j <= h-1; j++:
      	if A[j] < pivot:
      		i++
      		swap A[i] and A[j]
      swap A[i+1] and A[h]
      return i+1
  }
  ```

  * Randomization

### Data Structure(Skip)

* [Linked](http://www.koreascience.or.kr/article/JAKO201616853106304.pub) List
* Stack and Queue
* Graph and Tree

### Tree

* Binary Search Tree
* Red Black Tree
  * Lemma
  * Insertion
    * Reconstructing
    * Recoloring
  * Deletion
    if the node `z` 
    * has two children(left, right), replace it as `SUCCESSOR(z)`
    * is red node, remove it and replace its child `x`
    * is black node 
      * the color of child `x`  is red
        remove the node `z` and replace it as child `x`. 
        And then change the child `x`'s color to black
      * the child color is black
        remove the node `z` and replace it as child `x`.
        there are another nodes as sibling `s`, `l` is left child of `s` , `r` is right child of `s`
        * if the parent color of `x` is red, `<l, r>`(Same numbering is same method to solve)
          * Case 1-1: <black, black> *- 1*
            exchange color `p`, `s`
            ![image-20201210171758981](/home/dohan/project/studying/nn/img/image-20201210171758981.png)
          * Case 1-2: <*, Red> *- 2*
            reconstructing `p, s, r`
            exchange color of `p, s` and color `r` as red
            ![image-20201210171751450](/home/dohan/project/studying/nn/img/image-20201210171751450.png)
          * Case 1-3: <Red, Black> *- 3*
            ![image-20201210171635948](/home/dohan/project/studying/nn/img/image-20201210171635948.png)
        * if the parent color of `x` is black, <s, l, r>
          * Case 2-1: <black, black, black> *- 4*
            change `s` as red, and solve it recursively
            ![image-20201210171834425](/home/dohan/project/studying/nn/img/image-20201210171834425.png)
          * Case 2-2: <black, *, red> *- 2*
          * Case 2-3: <black, red, black> *- 3*
          * Case 2-4: <red, black, black> *- 5*
            ![image-20201210171853623](/home/dohan/project/studying/nn/img/image-20201210171853623.png)
  * Height
    The height is over than $$h \over 2$$, so tree has internal nodes more than $$2^{h \over 2} - 1$$at least. So $$n > 2^{h \over 2} - 1$$ is $$log_{2}{n + 1} > {h \over 2}$$, it is same as $$h < 2log_2{n+1}$$.

### Hash Table

* Direct Message
  * Concept
  * Limitation
* Hash Functions
  * Division Method
  * Multiplication Method
  * Universal Hashing
* Open Addressing

### Graph

* BFS

* DFS

* Topological Sort

  * Concept

  * Condition

  * psuedocode

    ```pseudocode
    int N
    bool visit[N]
    dfs(x):
    	visit[x] = true
    	for child in x:
    		if visit[child] is false:
    			dfs(child)
    	insert last of topological_sort array
    
    topological_sort(){	
    	for i=0; i<n; ++i:
    		if visit[i] is false:
    			dfs(visit)
    }
    ```

    

sudo apt-get install cabextract

WINEARCH=win32 WINEPREFIX=~/.wine wine wineboot

wget https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks

chmod 777 winetricks

./winetricks

출처: https://yurmu.tistory.com/5 [유르무차의 자기개발서]

Error in POL_Wine
Wine seems to have crashed

If your program is running, just ignore this message