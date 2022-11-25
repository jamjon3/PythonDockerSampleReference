# -*- coding: utf-8 -*-

# Example usage of API using GitHub's API to get the latest release and download the binary
# From a generated URL based on the latest version returned.

import os
import argparse
import requests
from version import __version__

urls = {
    "github_latest_api_url": "https://api.github.com/repos/microsoft/azure-pipelines-agent/releases/latest",
    "agent_base_url": "https://vstsagentpackage.azureedge.net/agent"
}

github_api_headers = {'Accept': "application/vnd.github+json"}

binary_file_name = "vsts-agent-linux.tar.gz"


def download_binary(url, path):
    """

    :param url: The download URL for the binary file
    :param path: The path the downloaded file will be saved to
    """
    try:
        print(f"Downloading the latest binary from {url}")
        r = requests.get(url, allow_redirects=True)
        match r.status_code:
            case 200:
                with open(path, 'wb') as file:
                    file.write(r.content)
                    print(f"Binary saved as {path}")
            case _:
                raise requests.exceptions.HTTPError(f"Response returned failed status code {r.status_code}")
    except Exception as error:
        raise


def get_latest_from_api_and_download_to_folder(args):
    """
    Uses the GitHub API to find the latest release and generates a url and output file path for the download method

    :param args: Input Argument dictionary
    """
    try:
        r = requests.get(urls['github_latest_api_url'], headers=github_api_headers, allow_redirects=True)
        match r.status_code:
            case 200:
                data = r.json()
                agent_ver = data['tag_name'][1:]
                print(f"Discovered the latest version from the GitHub API: {agent_ver}.")
                download_binary(
                    "/".join([
                        urls['agent_base_url'],
                        agent_ver,
                        f"vsts-agent-linux-x64-{agent_ver}.tar.gz"
                    ]),
                    os.path.join(args.output, binary_file_name)
                )
            case _:
                raise requests.exceptions.HTTPError(f"Response returned failed status code {r.status_code}")
    except Exception as error:
        raise


def main(args=None):
    """
    Ensure valid options before initiating the download process

    :param args: Input Argument dictionary
    """
    try:
        if args.output is not None:
            if os.path.isdir(args.output):
                if args.downloadlatest:
                    get_latest_from_api_and_download_to_folder(args)
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
