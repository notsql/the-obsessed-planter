# The Obsessed Planter

## Setup

1. Run the following command:
```bash
nano ~/.bashrc
```

2. Paste the following:

```text
export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/Desktop/the-obsessed-planter/pi/serviceAccountKey.json"
```

3. Create Python Virtual Environment and Install Dependencies:

```bash
cd pi
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```
