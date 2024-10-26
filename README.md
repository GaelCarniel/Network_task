This content is meant to run on a PsychoPy installed in a venv containt several libraries that are not dependencies of psychopy.

You will need python 3.10
To create this environment: 
- C:\path\to\your\python.exe (3.10) -m venv c:Path\to\file
- if you are on windows using cmd *\Scripts\activate.bat  (inside your venv path)  *folder of your venv
- pip install -r requirements.py
- or directly pip install psychopy then pip install networkx 
- python "*\Lib\site-packages\psychopy\app\_psychopyApp.py" Network_task.py     *folder of your venv