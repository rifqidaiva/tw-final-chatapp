import utils


def get_all_users(user_id: str):
    """
    Get all users except the current user.
    """
    users = utils.User.get_all_except(user_id)
    if not users:
        return utils.Response(
            status_code=404,
            msg="No users found.",
        ).send()

    return utils.Response(
        status_code=200,
        msg="Users retrieved successfully.",
        data={"users": [user.to_dict() for user in users]},
    ).send()
