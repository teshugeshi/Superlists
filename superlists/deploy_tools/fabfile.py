from fabric.contrib.files import append,exists,sed
from fabric.api import env,local,run
import random

REPO_URL='git@github.com:teshugeshi/Superlists.git'

def deploy():
    self_folder=f'/home/superlists/Superlists'
    _create_directory_structure_if_necessary(self_folder)
    _get_latest_source(self_folder)
    _update_static_files(self_folder)
    _update_database(self_folder)
def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database','static'):
        run(f'mkdir -p {site_folder}/{subfolder}')
def _get_latest_source(site_folder):
    if exists(site_folder + '/.git'):
        run(f'cd {site_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {site_folder}')
    current_commit=local("git log -n 1 --format=%H",capture=True)
    run(f'cd {site_folder} && git reset --hard {current_commit}')
def _update_static_files(site_folder):
    run(
        f'cd {site_folder}'
        ' && python3 manage.py collectstatic --noinput'
    )
def _update_database(site_folder):
    run(
        f'cd {site_folder}'
        ' && python3 manage.py migrate --noinput'
    )
