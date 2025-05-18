import flask
import os

import utils


# MARK: GET /users/profile
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


# MARK: PUT /users/profile
def profile_put(user_id: str):
    data = flask.request.get_json()

    input_email = data.get("email")
    input_password = data.get("password")
    input_name = data.get("name")

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


# MARK: POST /users/profile/upload
def upload_profile_picture(user_id: str):
    """Upload a new profile picture for the user."""
    user = utils.User.from_id(user_id)
    if user is None:
        return utils.Response(
            status_code=404,
            msg="User not found",
        )

    # Assuming the file is sent as form-data with the key 'profile_picture'
    if "profile_picture" not in flask.request.files:
        return utils.Response(
            status_code=400,
            msg="No file part in the request",
        ).send()

    file = flask.request.files["profile_picture"]

    if file.filename == "":
        return utils.Response(
            status_code=400,
            msg="No selected file",
        ).send()

    # Check if the file is allowed
    allowed_extensions = {"png", "jpg", "jpeg"}
    if not (
        file.filename
        and any(file.filename.lower().endswith(f".{ext}") for ext in allowed_extensions)
    ):
        return utils.Response(
            status_code=400,
            msg="File type not allowed",
        ).send()

    # Save the file to a directory
    file_ext = file.filename.rsplit(".", 1)[-1].lower()
    upload_dir = f"uploads/{user.id}"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = f"{upload_dir}/profile_picture.{file_ext}"

    # Remove old profile pictures with different extensions
    for ext in allowed_extensions:
        old_file = f"{upload_dir}/profile_picture.{ext}"
        if os.path.exists(old_file) and old_file != file_path:
            os.remove(old_file)

    file.save(file_path)

    # Update the user's profile picture path
    user.profile_picture = "users/" + file_path
    user.save()

    return utils.Response(
        status_code=200,
        msg="Profile picture uploaded successfully",
        data={
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "profile_picture": user.profile_picture,
            "created_at": user.created_at,
        },
    ).send()


# MARK: GET /uploads/<user_id>/<filename>
def serve_profile_picture(user_id: str, filename: str):
    user = utils.User.from_id(user_id)
    if user is None:
        return utils.Response(
            status_code=404,
            msg="User not found",
        ).send()

    return flask.send_from_directory(
        f"uploads/{user_id}", filename, as_attachment=False
    )
