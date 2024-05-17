# Zenaura 

<img title="a title" alt="Alt text" src="./assets/logo.png" width="300" height="300" />

Zenaura, is expermenital library built on top of pyscript that allows python developers to build stateful component based SAP applications.
The library uses virtual dom implmentation to optimize performance and reactivity, responsiveness and interactivity of web apps.

## Quick Example : 

```Python
	    
```

# testing 
- install requirements 
```
pip install -r requirements.txt 
```
- run tests with coverage : 
```
python -m coverage run -m unittest
```

- run test coverage report :
```
python -m coverage report -m
```

- report 
```
-----------------------------------------------------------
zenaura\client\compiler.py       46      5    89%   38-39, 66, 88, 119
zenaura\client\component.py      22      2    91%   24, 34
zenaura\client\dom.py            50      2    96%   68, 71
zenaura\client\tags.py          144      3    98%   9-11
-----------------------------------------------------------
```

- important note : test coverage must be kept at 95%

# run example :

cd to examples folder
cd into example folder 
run 
```
flask --app hello run
```