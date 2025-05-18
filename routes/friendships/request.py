import flask

import utils


def friendship_request(user_id: str):
    """Send a friendship request to another user."""
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
            msg="Cannot send a friendship request to yourself",
        ).send()

    # Check if the target user exists
    target_user = utils.User.from_id(target_user_id)
    if target_user is None:
        return utils.Response(
            status_code=404,
            msg="Target user not found",
        ).send()

    # Check if the friendship already exists
    friendship = utils.Friendship.from_user_ids(user_id, target_user_id)
    if friendship is not None:
        return utils.Response(
            status_code=400,
            msg="Friendship already exists",
        ).send()

    # Create a new friendship request
    friendship = utils.Friendship(
        user1_id=user_id,
        user2_id=target_user_id,
        status="pending",
    )

    # Save the friendship request to the database
    friendship.save()

    return utils.Response(
        status_code=200,
        msg="Friendship request sent successfully",
    ).send()
