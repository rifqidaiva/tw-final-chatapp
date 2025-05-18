import flask

import utils


def friendship_remove(user_id: str):
    """Remove a friendship with another user."""
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
            msg="Cannot remove a friendship with yourself",
        ).send()

    # Check if the friendship exists
    friendship = utils.Friendship.from_user_ids(user_id, target_user_id)
    if friendship is None:
        return utils.Response(
            status_code=404,
            msg="Friendship not found",
        ).send()

    # Remove the friendship from the database
    friendship.delete()

    return utils.Response(
        status_code=200,
        msg="Friendship removed successfully",
    ).send()
