import os
import sys
import jenkins
import argparse
from pprint import pprint

JENKINS_USER = os.environ["JENKINS_USERNAME"]
JENKINS_TOKEN = os.environ["JENKINS_TOKEN"]
parser = argparse.ArgumentParser(
    "jenkins cli"
)
parser.add_argument("-hw", action="store_true", help="Hello world", dest="hello_world")
parser.add_argument("-ls", action="store_true", help="list jobs", dest="list_jobs")
parser.add_argument("-c", action="store_true", help="New Job", dest="new_job")
parser.add_argument("-d", help="Download Job", dest="download_job")

args = parser.parse_args()

def get_connection():
    return jenkins.Jenkins(
        'http://localhost:8000',
        username=JENKINS_USER,
        password=JENKINS_TOKEN
    )

def hello_world(server: jenkins.Jenkins):
    user = server.get_whoami()
    version = server.get_version()
    print('Hello %s from Jenkins %s' % (user['fullName'], version))

def new_job(server: jenkins.Jenkins):
    print(jenkins.EMPTY_CONFIG_XML)

def list_jobs(server: jenkins.Jenkins):
    jobs = server.get_jobs()
    print(jobs)

def save_job(job_data:str, job_name: str):
    with open('jobs/' + job_name + ".xml", 'w') as f:
        f.write(job_data)
    print(f"job name: {job_name} saved")

def download_job(server: jenkins.Jenkins, job_name: str):
    if (name := server.get_job_name(job_name)) is not None:
        job_info = server.get_job_config(name)
        print(job_info)
        save_job(job_info, job_name)
        return
    raise Exception("Job not found")

def main():
    if len(sys.argv) == 1:
        args.print_help()
    conn = get_connection()
    if args.hello_world:
        hello_world(conn)
    elif args.list_jobs:
        list_jobs(conn)
    elif args.new_job:
        new_job(conn)
    elif args.download_job:
        download_job(conn, args.download_job)
    else:
        parser.print_help()
