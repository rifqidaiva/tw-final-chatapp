import utils


def messages_get(user_id: str):
    messages = utils.Message.get_by_user(user_id)
    if not messages:
        return utils.Response(
            status_code=404,
            msg="No messages found for the user.",
        ).send()

    return utils.Response(
        status_code=200,
        msg="Messages retrieved successfully.",
        data={"messages": [message.to_dict() for message in messages]},
    ).send()
