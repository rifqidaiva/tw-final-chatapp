import flask

import utils


def friendship_accept(user_id: str):
    """Accept a friendship request from another user."""
    data = flask.request.get_json()
    target_user_id = data.get("target_user_id")

    if target_user_id is None:
        return utils.Response(
            status_code=400,
            msg="target_user_id is required",
        ).send()

    if target_user_id == user_id:
        return utils.Response(
            status_code=400,
            msg="Cannot accept a friendship request from yourself",
        ).send()

    # Check if the friendship exists
    friendship = utils.Friendship.from_user_ids(user_id, target_user_id)
    if friendship is None:
        return utils.Response(
            status_code=404,
            msg="Friendship not found",
        ).send()

    # Check if the friendship is pending
    if friendship.status != "pending":
        return utils.Response(
            status_code=400,
            msg="Friendship is not in a pending state",
        ).send()

    # Update the friendship status to "accepted"
    friendship.status = "accepted"
    friendship.save()

    return utils.Response(
        status_code=200,
        msg="Friendship request accepted successfully",
    ).send()
