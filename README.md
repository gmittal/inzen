# Inzen
A simple search engine that uses Latent Semantic Analysis and Singular Value Matrix Decomposition and to produce better results.

Demo code for **Building Better Search Engines**, a 2016-17 Gunn High School Analysis Honors Project by [Daniel Zhu](@TheBigDanny) and [Gautam Mittal](@gmittal) that focuses on information retrieval applications using concepts such as vectors, matrices, and eigenspaces (learned throughout the year in the Analysis H course at Gunn). For our presentation demo, we created a simple search engine that uses Wikipedia documents and applies the topics discussed in the presentation, such as the use of vector space models, dense term-document matrices using singular value decomposition, and latent semantic analysis.

Requires Python 2.x+ and ```numpy```.

### Usage
``` $ python main.py```

Running the ```main.py``` script will either generate the necessary matrices needed (can take a while for large document sets), or will load previously generated matrices into memory if they exist locally.

You can then proceed to type in a search query once the cursor prompt becomes available. For example, here are some results when searching for "Elon".

```none
$ python main.py
Loading...
> Elon
-------------------------
Search Results for 'Elon' (0.11 seconds)
#1: data/www/Elon Musk.txt (0.984872421995)
#2: data/www/Flight_attendant.txt (0.536892581191)
#3: data/www/Royal_Air_Force.txt (0.425419054035)
#4: data/www/Forbes.txt (0.40558151638)
#5: data/www/Honeywell.txt (0.335476099555)
#6: data/www/The_World's_Billionaires.txt (0.328166039837)
#7: data/www/Forbes_list_of_The_World's_Most_Powerful_People.txt (0.323584583725)
#8: data/www/Boeing B-50 Superfortress.txt (0.254107931551)
#9: data/www/Air_pollution.txt (0.231107897563)
#10: data/www/Paul_Allen.txt (0.23078901262)
```

If you want to exit the program, simply type ```/exit```.

### Saved Results
Term-document and singular value decomposition matrices are saved after the initial execution of the program to avoid being regenerated every single time (saving compute resources and search time). This is useful if the desired reduced rank or the number of documents within the term-document matrix does not change. If you want to reset the program, simply run ``` $ rm -rf data/save/*``` to remove all of the saved files. The new term-document and SVD matrices will be automatically generated using your new documents or parameters the next time you run the program.


### License
[The MIT License (MIT)](https://tldrlegal.com/license/mit-license)

Copyright (c) 2017 Gautam Mittal and Daniel Zhu

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
