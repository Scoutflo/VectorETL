from github import Github
import boto3
import logging
from io import BytesIO
import os
from .file_loader import FileBaseSource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GithubSource(FileBaseSource):
    def __init__(self, config):
        super().__init__(config)
        self.client = None
        self.repo_url = config['repo_name']
        self.pat = config.get('pat', None)  
        self.repo = None
        self.branch_name = config.get('branch_name', 'main')  
        self.file_ext = config.get('file_ext', '.md')
        
    
    def connect(self):
        logger.info("Connecting to Github client...")
        ACCESS_USERNAME = os.getenv('GITHUB_ACCESS_USERNAME')
        ACCESS_PWD = os.getenv('GITHUB_ACCESS_PWD')
        self.client = Github(ACCESS_USERNAME, ACCESS_PWD, per_page=100)
        self.repo = self.client.get_repo(self.repo_url)
        if self.repo != None: 
            logger.info("Connected to Github client.")
        else: 
            logger.error("Failed to connect Github client.")
            
    def list_files(self):
        if not self.client:
            self.connect()

        
        branch = self.repo.get_branch(self.branch_name)
        commit_sha = branch.commit.sha

        tree = self.repo.get_git_tree(commit_sha, recursive=True).tree
        filtered_files = [file.path for file in tree if file.path.endswith(self.file_ext)]
        
        return filtered_files
    
    def read_file(self, file_path):
        downloaded_files = []

        local_file_path = os.path.join(os.getcwd(), file_path.split('/')[-1])
        content = self.repo.get_contents(file_path, ref=self.branch_name)
        
        file_data = content.decoded_content          
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        
        # Save file
        with open(local_file_path, "wb") as f:
            f.write(file_data)
        
       
        downloaded_files.append(local_file_path)
        logger.info(f"Downloaded {file_path} to {os.getcwd()}")

        return downloaded_files
    
    def delete_directory(self, path):

        for root, dirs, files in os.walk(path, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(path)
        
    def download_file(self, file_path):

        downloaded_files = []

        local_file_path = os.path.join("tempfile_downloads", file_path.split('/')[-1])
        
        if not self.client:
            self.connect()
            
        content = self.repo.get_contents(file_path, ref=self.branch_name)
        file_data = content.decoded_content
        
    
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        
        
        with open(local_file_path, "wb") as f:
            f.write(file_data)
        
        downloaded_files.append(local_file_path)
        logger.info(f"Downloaded {file_path} to {local_file_path}")

        return downloaded_files

