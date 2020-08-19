# TODO
# 1. download bicimad info from portal
# 2. have a txt file to control which are files are already download
# 3. bimonthly execution?
# (4. concatenate proc with the pandas proccesing)

import boto3
import utils

s3_cli = boto3.client('s3')
BUCKET = 'bicimad-project'




if __name__ == '__main__':

    out = utils.loadControlFile(s3_cli, BUCKET, 'Control/stations.csv')
    print(out)