# -*- coding: utf-8 -*-

# Example usage of API using GitHub's API to get the latest release and download the binary
# From a generated URL based on the latest version returned.

import os
import argparse
import requests
from version import __version__


class LatestReleaseFromGithubAPI:
    """
    Gets the latest release from a specified GitHub Repository
    """

    github_api_headers = {'Accept': "application/vnd.github+json"}
    github_api_base_url = "https://api.github.com/repos"

    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo

    def get_latest_release(self):
        """
        Uses the GitHub API to find the latest release and generates url and output file path for the download method

        return string
        """
        try:
            r = requests.get("/".join([
                self.github_api_base_url,
                self.owner,
                self.repo,
                "releases/latest"
            ]), headers=self.github_api_headers, allow_redirects=True)
            match r.status_code:
                case 200:
                    data = r.json()
                    agent_ver = data['tag_name']
                    print(f"Discovered the latest version from the GitHub API: {agent_ver}.")
                    return agent_ver
                case _:
                    raise requests.exceptions.HTTPError(f"Response returned failed status code {r.status_code}")
        except Exception as error:
            raise

    def __enter__(self):
        """
        __enter__ Just returns an instance of self

        :return: Instance of LatestReleaseFromGithubAPI
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        __exit__ Just returns an instance of self

        :param exc_type: Execution Type
        :param exc_val: Execution Value
        :param exc_tb: Execution
        :return: Instance of LatestReleaseFromGithubAPI
        """
        return self


class DownloadVSTSAgent:
    agent_base_url = "https://vstsagentpackage.azureedge.net/agent"
    binary_file_name = "vsts-agent-linux.tar.gz"

    def __init__(self, agent_ver):
        self.agent_ver = agent_ver

    def download_agent(self, path):
        """

        :param path: The path the downloaded file will be saved to
        """
        try:
            url = "/".join([
                self.agent_base_url,
                self.agent_ver,
                f"vsts-agent-linux-x64-{self.agent_ver}.tar.gz"
            ])
            print(f"Downloading the latest binary from {url}")
            r = requests.get(url, allow_redirects=True)
            match r.status_code:
                case 200:
                    fullpath = os.path.join(path, self.binary_file_name)
                    with open(fullpath, 'wb') as file:
                        file.write(r.content)
                        print(f"Binary saved as {fullpath}")
                case _:
                    raise requests.exceptions.HTTPError(f"Response returned failed status code {r.status_code}")
        except Exception as error:
            raise
        return None

    def __enter__(self):
        """
        __enter__ Creates the database connection and sets it to the class as 'db'

        :return: Instance of DownloadVSTSAgent
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        __exit__ Sets Exits the class and closes the database connection

        :param exc_type: Execution Type
        :param exc_val: Execution Value
        :param exc_tb: Execution
        :return: Instance of DownloadVSTSAgent
        """
        return self


def main(args=None):
    """
    Ensure valid options before initiating the download process

    :param args: Input Argument dictionary
    """
    try:
        if args.output is not None:
            if os.path.isdir(args.output):
                if args.downloadlatest:
                    with LatestReleaseFromGithubAPI(
                            "microsoft",
                            "azure-pipelines-agent") as APILatest:
                        with DownloadVSTSAgent(APILatest.get_latest_release()[1:]) as agentDownloader:
                            agentDownloader.download_agent(args.output)
                else:
                    raise ValueError(f"Usage: -d or --downloadlatest must be provided")
            else:
                raise FileExistsError(f"{args.output} directory does not exist. Directory must exist!")
        else:
            raise ValueError(f"Usage: Option -o , --output <directory> is required.")
    except Exception as error:
        raise


if __name__ == '__main__':
    """
    __name__ Initializes the application and parses the parameters

    :return: None
    """
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--downloadlatest", action="store_true",
                            help="Download the latest Azure DevOps agent binary using the GitHub API")
        parser.add_argument('-o', '--output', help="Output directory of the Agent binary")
        parser.add_argument('-v', '--version', action='version', version=__version__)
        main(parser.parse_args())
    except Exception as e:
        print('Caught this error: ' + repr(e))
        raise
