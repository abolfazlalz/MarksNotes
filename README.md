# Notes Markdown

Write text and note with md file format and save it into sqlite database.

## Clone the project

Clone the project using the following command.

```bash
git clone https://github.com/techanodev/MarksNotes
```

Go to project directory

```bash
cd MarksNotes
```

### Run using Docker
at first install docker on your system.

```bash
docker-compose up -d
```

we use `-d` tag for run container in background.

for stopping the program run below command:

```bash
docker-compose down
```

### Run as development

At first make a enviroment

```bash
python3 -m venv .env
source .env/bin/activate # This command is different in Windows systems.
```

Install the required libraries for the project.

```bash
pip install -r requirements.txt
```

Set the environment variables Flask needs 

```bash 
export FLASK_APP=app
export FLASK_ENV=development
```
