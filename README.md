# Artificial Intelligence Contamporary Approach

## Online Course Projects from edx.org
https://courses.edx.org/courses/course-v1:ColumbiaX+CSMM.101x+1T2020/course/

**Activate the virtual environment**
```
source ai-env/bin/activate
```

**Install all packages**
```
pip3 install -r requirements.txt
```


**Run Weeks 2-3 Project**

Make sure to activate the virtual environment

```
python3 -m projects.week2.driver bfs 8,6,4,2,1,3,5,7,0
python3 -m projects.week2.driver dfs 8,6,4,2,1,3,5,7,0
python3 -m projects.week2.driver ast 8,6,4,2,1,3,5,7,0
```

**Run Week 2-3 Project tests**

Make sure to activate the virtual environment

```
python3 -m pytest projects/week2/tests
```