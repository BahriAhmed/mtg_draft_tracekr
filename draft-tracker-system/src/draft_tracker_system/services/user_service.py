from draft_tracker_system.db.models import User, Role
from draft_tracker_system.utils.hash import hash_password, verify_password
from passlib.hash import bcrypt

def register_player(session, username, password):
    # check if username already exists
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        raise ValueError("Username already exists")

    # get the "player" role
    role = session.query(Role).filter_by(role_name="player").first()
    if not role:
        raise ValueError("Player role not found in DB")

    # create user
    new_user = User(
        username=username,
        password=hash_password(password),
        role_id=role.role_id
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

def login_user(session, username, password):
    user = session.query(User).filter_by(username=username).first()

    if not user:
        raise ValueError("User not found")

    if not verify_password(password, user.password):
        raise ValueError("Incorrect password")

    return user

def change_password(session, current_user, target_user_id, old_password, new_password):
    target_user = session.query(User).filter_by(user_id=target_user_id).first()

    if not target_user:
        raise ValueError("User not found")

    # ADMIN RULE: can change anyone
    if current_user.role.role_name == "admin":
        target_user.password = hash_password(new_password)
        session.commit()
        return target_user

    # PLAYER RULE: can only change self
    if current_user.user_id != target_user_id:
        raise PermissionError("Not allowed")

    # must verify old password
    if not verify_password(old_password, current_user.password):
        raise ValueError("Incorrect password")

    current_user.password = hash_password(new_password)
    session.commit()

    return current_user

def delete_user(session, current_user, target_user_id):

    target_user = session.query(User).filter_by(user_id=target_user_id).first()

    if not target_user:
        raise ValueError("User not found")


    # ADMIN CAN DELETE ANY USER
    if current_user.role.role_name == "admin":
        session.delete(target_user)
        session.commit()
        return {"deleted_user_id": target_user_id}

    # PLAYER CAN ONLY DELETE SELF
    if current_user.user_id != target_user_id:
        raise PermissionError("Not allowed to delete this user")

    session.delete(current_user)
    session.commit()

    return {"deleted_user_id": target_user_id}


def update_username(session, current_user, target_user_id, new_username):

    target_user = session.query(User).filter_by(user_id=target_user_id).first()

    if not target_user:
        raise ValueError("User not found")

    # ADMIN CAN UPDATE ANY USER
    if current_user.role.role_name == "admin":
        existing = session.query(User).filter_by(username=new_username).first()
        if existing:
            raise ValueError("Username already taken")

        target_user.username = new_username
        session.commit()

        return target_user

    # PLAYER CAN ONLY UPDATE SELF
    if current_user.user_id != target_user_id:
        raise PermissionError("Not allowed to update this user")

    existing = session.query(User).filter_by(username=new_username).first()
    if existing:
        raise ValueError("Username already taken")

    target_user.username = new_username
    session.commit()

    return target_user

def get_all_users(session, current_user):

    # ONLY ADMIN CAN ACCESS
    if current_user.role.role_name != "admin":
        raise PermissionError("Not allowed")

    users = session.query(User).all()

    return users