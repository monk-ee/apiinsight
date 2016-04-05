import subprocess


def lambda_handler(event, context):
    args = ("venv/bin/python3.4 ", "api_insight.py")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    print(output)