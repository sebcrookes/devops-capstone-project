"""
Account Service

This microservice handles the lifecycle of Accounts
"""
# pylint: disable=unused-import
from flask import jsonify, request, make_response, abort, url_for   # noqa; F401
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application


############################################################
# Health Endpoint
############################################################


@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################


@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
            # paths=url_for("list_accounts", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# CREATE A NEW ACCOUNT
######################################################################


@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based the data in the body that is posted
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    # Uncomment once get_accounts has been implemented
    # location_url = url_for("get_accounts", account_id=account.id, _external=True)
    location_url = "/"  # Remove once get_accounts has been implemented
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
# LIST ALL ACCOUNTS
######################################################################


@app.route("/accounts", methods=["GET"])
def list_all_accounts():
    """
    Lists all accounts
    This endpoint will return a JSON list of all of the accounts in the system
    """
    app.logger.info("Request to list accounts")

    accounts = Account.all()
    json_list = []

    for account in accounts:
        json_list.append(account.serialize())

    app.logger.info(f"When listing accounts, found {len(accounts)} accounts")

    return jsonify(json_list), 200


######################################################################
# READ AN ACCOUNT
######################################################################


@app.route("/accounts/<account_id>", methods=["GET"])
def read_account(account_id):
    """
    Read Account
    This endpoint will return a JSONified version of the account associated with the given ID
    """
    app.logger.info(f"Request for an account with id {account_id}")

    account = Account.find(account_id)

    if not account:
        abort(404, f"Account with given ID {account_id} not found")

    return account.serialize(), 200


######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################


@app.route("/accounts/<account_id>", methods=["PUT"])
def update_accounts(account_id):
    """
    Update an Account
    This endpoint will replace an account specified by the given ID with the data sent
    """
    app.logger.info(f"Request to update the account with ID {account_id}")

    account = Account.find(account_id)

    if not account:
        abort(404, f"Account with given ID {account_id} not found")

    account.deserialize(request.get_json())
    account.update()

    return account.serialize(), 200


######################################################################
# DELETE AN ACCOUNT
######################################################################


@app.route("/accounts/<account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """
    Delete an Account
    This endpoint will delete an account from the system given its ID
    """
    app.logger.info(f"Request to delete the account with ID {account_id}")

    account = Account.find(account_id)
    if account:
        account.delete()

    return "", 204


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
