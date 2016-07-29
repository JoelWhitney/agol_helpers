__author__='joelwhitney'
"""
   This sample shows how to share a package to agol using arcpy
"""
import datetime
import argparse
import arcpy
import os

def main(args):
    """
    This
    :param args: arguments from argparse
    :return:
    """
    in_package = args.in_package
    username = args.username
    password = args.password
    summary = args.summary
    tags = args.tags
    datetimenow = datetime.datetime.now()
    # Update each map by the provided id
    try:
        if not verify_file_path(args.in_package): raise Exception('Package does not exist')
        # Get item
        arcpy.SharePackage_management(in_package=in_package, username=username, password=password, summary=summary,
                                      tags=tags, organization="EVERYBODY")
        print("Successfully shared package\nShared at: {}".format(datetimenow))
    except Exception as e:
        print(e)

def verify_file_path(filePath):
    """
    verify file exists
    :param filePath: the joined directory and file name
    :return: Boolean: True if file exists
    """
    ospath = os.path.abspath(filePath)
    ospath = ospath.replace("\\", "\\\\")
    if not os.path.isfile(str(ospath)):
        return False
    else:
        return True

# cd "C:\Users\joel8641\Dropbox\Esri Material\Other helper scripts\agol_helpers"
# python share_package_to_agol.py -fp "C:\Users\joel8641\Downloads\corrupt_Canada_Prairies.mmpk" -u "nitrouser" -p "nitrouser" -s "Package uploaded from helper script" -t "ArcPy; Locator; Transportation Network; MMPK"
if __name__ == "__main__":
    # Get all of the commandline arguments
    parser = argparse.ArgumentParser("Sharing details")
    parser.add_argument('-fp', dest='in_package', help="File path to package ", required=True)
    parser.add_argument('-u', dest='username', help="AGOL username", required=True)
    parser.add_argument('-p', dest='password', help="AGOL password", required=True)
    parser.add_argument('-s', dest='summary', help="Summary for package", required=True)
    parser.add_argument('-t', dest='tags', help="Tags for package", default=None)
    args = parser.parse_args()
    try:
        main(args)
    except Exception as e:
        print(e)