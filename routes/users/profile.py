import flask

import utils


def profile_get(user_id: str):
    """Get the profile of the current user."""

    user = utils.User.from_id(user_id)

    if user is None:
        return utils.Response(
            status_code=404,
            msg="User not found",
        )

    return utils.Response(
        status_code=200,
        msg="User profile retrieved successfully",
        data={
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "profile_picture": user.profile_picture,
            "created_at": user.created_at,
        },
    ).send()


def profile_put(user_id: str):
    data = flask.request.get_json()

    input_email = data.get("email")
    input_password = data.get("password")
    input_name = data.get("name")
    input_profile_picture = data.get("profile_picture")

    user = utils.User.from_id(user_id)
    if user is None:
        return utils.Response(
            status_code=404,
            msg="User not found",
        )

    updated = False

    if input_email is not None:
        user.email = input_email
        updated = True
    if input_password is not None:
        user.password = input_password
        updated = True
    if input_name is not None:
        user.name = input_name
        updated = True
    if input_profile_picture is not None:
        user.profile_picture = input_profile_picture
        updated = True

    if updated:
        user.save()

    return utils.Response(
        status_code=200,
        msg="Profile updated successfully" if updated else "No changes made",
        data={
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "profile_picture": user.profile_picture,
            "created_at": user.created_at,
        },
    ).send()
