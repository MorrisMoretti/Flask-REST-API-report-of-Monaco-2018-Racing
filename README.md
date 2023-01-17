### TASK 8 - REST API report of Monaco 2018 Racing

####  Folder road_data must be placed in project root directory.


### Install
```sh
 python -m pip install --upgrade pip
 python -m pip install -r requirements.txt
```
#####

#### Install pre-commit
```sh
pre-commit install
```
#####
#### Check migrate from .pre-commit-config.yaml
```sh
pre-commit migrate-config
```
#####

##### Check isort flake8 hooks
```sh
pre-commit run --all-files
```
####
### Start flask app
````
python app.py
````
#####

## Examples:

#### http://127.0.0.1:5000/apidocs/
<img src="read_me_png/13.png" alt="Alt text" title="Optional title">

#### http://127.0.0.1:5000/api/v1/report/?format=json
<img src="read_me_png/5.png" alt="Alt text" title="Optional title">

#### http://127.0.0.1:5000/api/v1/report/?format=xml
<img src="read_me_png/6.png" alt="Alt text" title="Optional title">

#### http://127.0.0.1:5000/api/v1/drivers/?format=xml&order=desc
<img src="read_me_png/7.png" alt="Alt text" title="Optional title">

#### http://127.0.0.1:5000/api/v1/drivers/?format=xml&order=asc
<img src="read_me_png/8.png" alt="Alt text" title="Optional title">

#### http://127.0.0.1:5000/api/v1/drivers/?format=json&order=asc
<img src="read_me_png/9.png" alt="Alt text" title="Optional title">

#### http://127.0.0.1:5000/api/v1/drivers/?format=json&order=desc
<img src="read_me_png/10.png" alt="Alt text" title="Optional title">

#### http://127.0.0.1:5000/api/v1/drivers/driver_id=SVF?format=xml
<img src="read_me_png/11.png" alt="Alt text" title="Optional title">

#### http://127.0.0.1:5000/api/v1/drivers/driver_id=SVF?format=json
<img src="read_me_png/12.png" alt="Alt text" title="Optional title">

#### http://127.0.0.1:5000/report
<img src="read_me_png/1.png" alt="Alt text" title="Optional title">

#### http://127.0.0.1:5000/drivers/
<img src="read_me_png/2.png" alt="Alt text" title="Optional title">

#### http://127.0.0.1:5000/drivers/?order=desc
<img src="read_me_png/4.png" alt="Alt text" title="Optional title">

#### http://127.0.0.1:5000/drivers/driver_id=SVF
<img src="read_me_png/3.png" alt="Alt text" title="Optional title">
