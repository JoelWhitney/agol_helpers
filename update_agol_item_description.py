__author__='joelwhitney'
"""
   This sample shows how to edit a item description on agol using arcrest library by item id
   In order to get id with just an item name you can do something like:

    user = portal_admin.content.users.user("ar_navtest")
    for item in user.items:
        if item.title == someTitle:
            moveItem = item.id
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
            while True:
                # Get portal instance
                portal_admin = arcrest.manageorg.Administration(securityHandler=shh.securityhandler)
                # Update each map by the provided id
                for item_id in args.item_ids:
                    try:
                        # Get item
                        item = portal_admin.content.getItem(itemId=item_id).userItem
                        itemParams = arcrest.manageorg.ItemParameter()
                        datetimenow = datetime.datetime.now()
                        itemParams.description = "Modified: {}".format(datetimenow)
                        item.updateItem(itemParams)
                        print("Successfully Modified Map Item Id: {}\nModified at: {}".format(item.title, datetimenow))
                    except Exception as e:
                        print("Error Configuring id: {}".format(item_id))
                        print(e)
                sleep(30)
    except Exception as e:
        print(e)



# cd "C:\Users\joel8641\Dropbox\Esri Material\Other helper scripts\agol_helpers"
# python update_agol_item_description.py -ids "9c55baf37d46409d9f738dc37fc109b9"
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
    parser.add_argument('-ids', dest='item_ids', help="The ids of the items to configure", nargs="+", required=True)

    args = parser.parse_args()
    main(args)