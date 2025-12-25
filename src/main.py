import argparse
from http import HTTPStatus
import os
from collections.abc import Callable
import sys
from pathlib import Path
from enum import StrEnum
import inspect
import requests

import jc
import jenkins

JENKINS_USER = os.environ["JENKINS_USERNAME"]
JENKINS_TOKEN = os.environ["JENKINS_TOKEN"]
parser = argparse.ArgumentParser("jenkins cli")


def get_connection() -> jenkins.Jenkins:
    return jenkins.Jenkins(
        "http://localhost:8000",
        username=JENKINS_USER,
        password=JENKINS_TOKEN,
    )


def cli_command() -> Callable:
    def decorate(func: Callable) -> Callable:
        func.is_visible = True
        return func

    return decorate


class Jenkins:
    """Contains methods for Jenkins class."""

    def __init__(self):
        self.connection = get_connection()

    @staticmethod
    def new_job(args) -> None:
        """Not impl."""
        print(jenkins.EMPTY_CONFIG_XML)

    @cli_command()
    def list_jobs(self) -> None:
        jobs = self.connection.get_jobs()
        print(jobs)

    @staticmethod
    def save_job(job_data: str, job_name: str) -> None:
        with Path("jobs/" + job_name + ".xml").open("w") as f:
            f.write(job_data)
        print(f"job name: {job_name} saved")

    @cli_command()
    def download_job(self, job_name: str) -> str:
        server = self.connection
        if (name := server.get_job_name(job_name)) is not None:
            job_info = server.get_job_config(name)
            print(job_info)
            Jenkins.save_job(job_info, job_name)
            return job_info
        msg = "Job not found"
        raise Exception(msg)

    def update_job(self, job_name: str) -> None:
        Jenkins.validate_job(job_name)

    @staticmethod
    @cli_command()
    def validate_job(fname: str):
        data = open("jobs/" + fname).read()
        if not data:
            raise Exception("Data is empty")
        form_data = {"Jenkinsfile": data}
        jenkins_host = (
            f"http://{os.environ['JENKINS_HOST']}/pipeline-model-converter/validate"
        )
        session = requests.Session()
        response = session.post(
            jenkins_host, auth=(JENKINS_USER, JENKINS_TOKEN), data=form_data
        )
        if response.status_code != HTTPStatus.OK:
            msg = f"Request to url: {os.environ['JENKINS_HOST']} was {response.status_code}.. {response.text if response.text else response.json()}"
            raise Exception(msg)
        print(f"Job: {fname} successfully validated")


def create_cli(cls):
    parser = argparse.ArgumentParser(description="Jenkins CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    used_shorthands = set()
    for name, func in inspect.getmembers(Jenkins, predicate=inspect.isfunction):
        if not hasattr(func, "is_visible"):
            continue

        shorthand = name[0]
        if shorthand in used_shorthands:
            shorthand = name[:2]

        used_shorthands.add(shorthand)
        sub = subparsers.add_parser(name, aliases=[shorthand], help=func.__doc__)
        sig = inspect.signature(func)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            kwargs = {}
            kwargs["required"] = True
            sub.add_argument(f"--{param_name.replace('_', '-')}", **kwargs)
        sub.set_defaults(func=func)
    return parser


def main() -> None:
    jk = Jenkins()
    parser = create_cli(Jenkins)
    args = parser.parse_args()

    func_args = vars(args).copy()

    command_name = func_args.pop("func").__name__
    func_args.pop("command")
    func_args.pop("func", None)

    method_to_call = getattr(jk, command_name)

    method_to_call(**func_args)


if __name__ == "__main__":
    main()
