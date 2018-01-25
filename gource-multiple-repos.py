#!/usr/bin/python

#==============================================================================
#title           :gource-multiple-repos.py
#description     :This will clone all repos of given github user/organization and render a commit visualization
#author          :nlsltz
#date            :24.01.2018
#version         :0.1
#usage           :python gource-multiple-repos.py <USER/ORGANIZATION> <API_TOKEN>
#notes           :To work properly python module requests and gitpython is needed. Also gource and ffmpeg has to be installed.
#python_version  :2.7
#==============================================================================

import os
import glob
import requests
from git import Repo
from optparse import OptionParser

usage = "usage: %prog GITHUB_ACCOUNT GITHUB_API_TOKEN"
parser = OptionParser(usage)
(options, args) = parser.parse_args()
if len(args) != 2:
    parser.error("Incorrect number of arguments. Please provide github account and api token!")

github_account = args[0]
api_token      = args[1]

print 'Creating folders...'
#os.mkdir('repos')
os.mkdir('logs')
files = glob.glob('./logs/*')
for f in files:
    os.remove(f)
os.mkdir('output')
files = glob.glob('./output/*')
for f in files:
    os.remove(f)
print 'Done...'

print 'Requesting list of repos...'
endpoint = 'https://api.github.com/orgs/' + github_account + '/repos?per_page=100'
headers  = {'Authorization':'Bearer ' + api_token}
response = requests.get(endpoint,headers=headers).json()
print 'Done...'

print 'Cloning repos and creating gource logs...'
for item in response:
    clone_url           = item['ssh_url']
    repo_dir            = "./repos/" + item['name']
    #Repo.clone_from(clone_url, repo_dir)
    log_dir             = './logs'
    repo_name           = item['name']
    gource_log_command  = 'gource --output-custom-log ' + log_dir + '/' + repo_name + '.log ' + repo_dir
    gource_log_command2 = '''awk -F\| -v repo="''' + repo_name + '''" '{print $1 "|" $2 "|" $3 "|" repo $4}' "''' + log_dir + '/' + repo_name + '.log" > "' + log_dir + '/' + repo_name + '.gourced.log"'''
    os.system(gource_log_command)
    os.system(gource_log_command2)
print 'Done...'

print 'Combining single gource logs...'
combine_log_command = '''cat ./logs/*.gourced.log | sort -n > ./logs/combined.gourced.log'''
os.system(combine_log_command)
print 'Done...'

print 'Creating gource file...'
output_dir         = './output'
gource_output_file = 'gource-multi-repos.ppm'
gource_command     = 'gource ./logs/combined.gourced.log --title "ZEIT Repositories" --background 555555 --key --bloom-multiplier 1.0 --bloom-intensity 1.0 -e 1.0 --seconds-per-day 1 --auto-skip-seconds 0.7 --file-idle-time 0 --max-file-lag 3 -highlight-dirs --file-extensions --highlight-users --multi-sampling --stop-at-end -1280x720 -s 0.25 -o ' + output_dir + '/' +  gource_output_file
os.system(gource_command)
print 'Done...'

print 'Creating rendered video...'
ffmepg_output_file = 'gource-multi-repos.mp4'
ffmpeg_command     = 'ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i ' + output_dir + '/' + gource_output_file + ' -vcodec libx264 -preset ultrafast -pix_fmt yuv420p -crf 1 -threads 0 -bf 0 ' + output_dir + '/' +  ffmepg_output_file
#os.system(ffmpeg_command)
print 'Done...'

print 'Cleaning log directory...'
files = glob.glob('./logs/*')
for f in files:
    os.remove(f)
print 'Done...'