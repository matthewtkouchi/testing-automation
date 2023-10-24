# testing-automation
<h3>Note currently script must be run using "run python file" in terminal when using the venv. If you installed your own dependencies, then you can use code runner fine in vs code </h3>
<p>Also make sure you are in the venv before running code. You should have a (.venv) in front of your directory path in the terminal. If it doesn't show, then close the terminal and reopen it. This will automatically run the activate.bat file stored in the .venv/Scripts for Windows and .venv/bin for Unix</p>
<br />
## Filename: requirements.txt

- Contains the dependencies needed for this project.
- If any changes to the package dependencies are made, run `pip freeze > requirements.txt` to update the requirements file.
- Running `pip install -r requirements.txt` will install all the dependencies on your local machine.



### v1.1 10/23/23:
- improvement 1: folders to store csv is created automatically using relative paths now
- improvement 2: Select the instrument resource connection through an automatic GUI instead of manually
- improvement 3: Can rename files at the end of every test
- improvement 4: creates a compiled file of all .csv's in measurement-files. This file will be all the dBm values of each test converted to linear Watts.

### Going to add in next iteration: 
- Automatically get the com port for serial
- gui for setting field fox to NA or SA mode
- gui for settings of either of those choices
- automatic plotting
- make renaming csv files a callable function, rather than running it after every test