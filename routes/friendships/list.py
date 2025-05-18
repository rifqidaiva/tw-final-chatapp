import utils


def friendship_list(user_id: str):
    """List all friendships for a user."""
    friendships = utils.Friendship.get(user_id)

    if not friendships:
        return utils.Response(
            status_code=404,
            msg="No friendships found",
        ).send()

    friendships_list = [
        {
            "id": friendship.id,
            "user1_id": friendship.user1_id,
            "user2_id": friendship.user2_id,
            "status": friendship.status,
            "created_at": friendship.created_at,
        }
        for friendship in friendships
    ]

    return utils.Response(
        status_code=200,
        msg="Friendships retrieved successfully",
        data=friendships_list,
    ).send()
