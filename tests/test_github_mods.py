from ..vector_etl.source_mods.github_loader import GithubSource

def run():
    source = GithubSource({
        "repo_name": "https://github.com/terraform-aws-modules/terraform-aws-iam.git"
    })
    
    source.connect()
    
    files = source.list_files()
    
    print(files)
    
    
if __name__ == '__main__':
    run()