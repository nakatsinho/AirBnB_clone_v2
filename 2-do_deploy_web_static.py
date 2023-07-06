#!/usr/bin/python3
from fabric.api import env, run, put
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = '<your-username>'
env.key_filename = '<path-to-your-ssh-key>'

def do_deploy(archive_path):
    """
    Distributes an archive to web servers.
    """
    if not exists(archive_path):
        return False

    try:
        archive_filename = archive_path.split('/')[-1]
        archive_folder = "/data/web_static/releases/{}".format(archive_filename.split('.')[0])

        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Uncompress the archive to /data/web_static/releases/
        run('mkdir -p {}'.format(archive_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, archive_folder))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move contents to proper location
        run('mv {}/web_static/* {}/'.format(archive_folder, archive_folder))
        run('rm -rf {}/web_static'.format(archive_folder))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current
        run('ln -s {} /data/web_static/current'.format(archive_folder))

        return True
    except Exception as e:
        print(e)
        return False
