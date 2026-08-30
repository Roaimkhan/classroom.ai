from gc_agent.Oauth.authentication_client import authenticate
from gc_agent.fetcher.fetcher import gc_fetcher
from googleapiclient.discovery import build

def build_fetcher()->gc_fetcher:
    creds = authenticate()
    clsrm_client = build("classroom", "v1", credentials=creds)
    dr_client = build("drive", "v3", credentials=creds)
    fetcher = gc_fetcher(clsrm_client,dr_client)
    return fetcher

fetcher = build_fetcher()
if __name__ == "__main__":
    file = fetcher.download_assignments("1QyrxFv6D8FT3ZqQS8Uh2EbwFLyhEfzI8")
    print(file)