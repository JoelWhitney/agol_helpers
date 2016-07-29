__author__='joelwhitney'
"""
   This sample shows how to move file in agol using arcrest library with just a folder name and item name
"""
import datetime
from time import sleep
import arcrest
from arcresthelper import securityhandlerhelper
import argparse
import json


def main(args):
    """
    This
    :param args: arguments from argparse
    :return:
    """
    securityinfo = {}
    securityinfo['security_type'] = args.security_type
    securityinfo['username'] = args.username
    securityinfo['password'] = args.password
    securityinfo['org_url'] = args.org_url
    securityinfo['proxy_url'] = args.proxy_url
    securityinfo['proxy_port'] = args.proxy_port
    securityinfo['referer_url'] = args.referer_url
    securityinfo['token_url'] = args.token_url
    securityinfo['certificatefile'] = args.certificate_file
    securityinfo['keyfile'] = args.keyfile
    securityinfo['client_id'] = args.client_id
    securityinfo['secret_id'] = args.secret_id
    try:
        # Authenticate
        shh = securityhandlerhelper.securityhandlerhelper(securityinfo)
        if not shh.valid:
            print(shh.message)
        else:
            # Get portal instance
            portal_admin = arcrest.manageorg.Administration(securityHandler=shh.securityhandler)
            # Get item_id by title
            destination_folder = args.destination_folder
            item_title = args.item_title
            # Initialize objects for validation purposes
            item_object = ""
            destination_folder_id = ""
            try:
                user = portal_admin.content.users.user(args.username)
                # Retrieve item object from AGOL
                for item in user.items:
                    if item.title == item_title:
                        move_item = item
                        # Get item
                        item_object = portal_admin.content.getItem(itemId=move_item.id).userItem
                        # Retrieve folder id
                        try:
                            for folder in user.folders:
                                if folder['title'] == destination_folder:
                                    dest_folder = folder
                                    destination_folder_id = dest_folder['id']
                        except Exception as e:
                            print(e)
                            print("Cannont find folder...")
                        # Move the item to the destination_folder_id
                        try:
                            print("Moving {} to folder {}...".format(move_item.title, dest_folder['title']))
                            item_object.moveItem(folder=destination_folder_id)
                            datetimenow = datetime.datetime.now()
                            print("Successfully Moved Map Item Id: {}\nModified at: {}".format(move_item.title, datetimenow))
                        except Exception as e:
                            print(e)
                            print("Cannot move item to folder...")
                    else:
                        raise Exception("Cannont find item...")
            except Exception as e:
                print("Error Moving item '{}' to '{}' folder".format(item_title, destination_folder))
                print(e)
    except Exception as e:
        print(e)



# cd "C:\Users\joel8641\Dropbox\Esri Material\Other helper scripts\agol_helpers"
# python move_file_in_agol.py -it "EsriPortland_Office_300mapscale" -df "a"
if __name__ == "__main__":
    # Get all of the commandline arguments
    parser = argparse.ArgumentParser("Sign in information")
    parser.add_argument('-st', dest="security_type",
                        help="The security of the portal/org (Portal, LDAP, NTLM, OAuth, PKI)", default="Portal")
    parser.add_argument('-u', dest='username', help="The username to authenticate with", default="ar_navtest")
    parser.add_argument('-p', dest='password', help="The password to authenticate with", default="navtest1")
    parser.add_argument('-url', dest='org_url', help="The url of the org/portal to use", default="http://appsregression.maps.arcgis.com")
    parser.add_argument('-purl', dest='proxy_url', help="The proxy url to use", default=None)
    parser.add_argument('-pport', dest='proxy_port', help="The proxy port to use", default=None)
    parser.add_argument('-rurl', dest='referer_url', help="The referer url to use", default=None)
    parser.add_argument('-turl', dest='token_url', help="The token url to use", default=None)
    parser.add_argument('-cert', dest='certificate_file', help="The certificate to use", default=None)
    parser.add_argument('-kf', dest='keyfile', help="The key file to use", default=None)
    parser.add_argument('-cid', dest='client_id', help="The client id", default=None)
    parser.add_argument('-sid', dest='secret_id', help="The secret id", default=None)
    # Arguments for portal item and folder
    parser.add_argument('-it', dest='item_title', help="The title of the item you want to move", required=True)
    parser.add_argument('-df', dest='destination_folder', help="The name of the destination folder", required=True)

    args = parser.parse_args()
    main(args)





