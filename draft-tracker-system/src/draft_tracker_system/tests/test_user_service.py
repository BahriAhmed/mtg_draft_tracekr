import pytest

from draft_tracker_system.services.user_service import (
    register_player,
    login_user,
    change_password,
    delete_user,
    update_username,
    get_all_users
)

from draft_tracker_system.db.models import User, Role

def create_admin(db_session):
    admin_role = db_session.query(Role).filter_by(role_name="admin").first()

    admin = User(
        username="admin",
        password="hashed",
        role_id=admin_role.role_id
    )

    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)

    return admin

def test_register_user(db_session):
    user = register_player(db_session, "john", "1234")

    assert user.username == "john"
    assert user.user_id is not None

def test_login_user(db_session):
    register_player(db_session, "john", "1234")

    user = login_user(db_session, "john", "1234")

    assert user.username == "john"

def test_login_wrong_password(db_session):
    register_player(db_session, "john", "1234")

    with pytest.raises(ValueError):
        login_user(db_session, "john", "wrong")

def test_delete_self(db_session):
    user = register_player(db_session, "john", "1234")

    result = delete_user(db_session, user, user.user_id)

    assert result["deleted_user_id"] == user.user_id

def test_change_password(db_session):
    user = register_player(db_session, "john", "1234")

    updated = change_password(
        db_session,
        user,
        user.user_id,
        "1234",
        "newpass"
    )

    assert updated.user_id == user.user_id

def test_player_cannot_change_other_password(db_session):
    player1 = register_player(db_session, "john", "1234")
    player2 = register_player(db_session, "mike", "1234")

    with pytest.raises(PermissionError):
        change_password(
            db_session,
            player1,
            player2.user_id,
            "1234",
            "newpass"
        )

def test_player_cannot_delete_other_user(db_session):
    player1 = register_player(db_session, "john", "1234")
    player2 = register_player(db_session, "mike", "1234")

    with pytest.raises(PermissionError):
        delete_user(db_session, player1, player2.user_id)

def test_admin_can_change_any_password(db_session):
    player = register_player(db_session, "john", "1234")
    admin = create_admin(db_session)

    updated = change_password(
        db_session,
        admin,
        player.user_id,
        None,
        "newpass"
    )

    assert updated.user_id == player.user_id

def test_admin_can_delete_any_user(db_session):
    player = register_player(db_session, "john", "1234")
    admin = create_admin(db_session)

    result = delete_user(db_session, admin, player.user_id)

    assert result["deleted_user_id"] == player.user_id

def test_player_can_update_own_username(db_session):
    user = register_player(db_session, "john", "1234")

    updated = update_username(
        db_session,
        user,
        user.user_id,
        "john_new"
    )

    assert updated.username == "john_new"

def test_player_cannot_update_other_user(db_session):
    user1 = register_player(db_session, "john", "1234")
    user2 = register_player(db_session, "mike", "1234")

    with pytest.raises(PermissionError):
        update_username(
            db_session,
            user1,
            user2.user_id,
            "hacked_name"
        )

def test_admin_can_update_any_user(db_session):
    user = register_player(db_session, "john", "1234")
    admin = create_admin(db_session)

    updated = update_username(
        db_session,
        admin,
        user.user_id,
        "admin_changed"
    )

    assert updated.username == "admin_changed"

def test_username_already_taken(db_session):
    user1 = register_player(db_session, "john", "1234")
    user2 = register_player(db_session, "mike", "1234")

    with pytest.raises(ValueError):
        update_username(
            db_session,
            user2,
            user2.user_id,
            "john"
        )

def test_admin_can_read_all_users(db_session):
    # create users
    user1 = register_player(db_session, "john", "1234")
    user2 = register_player(db_session, "mike", "1234")

    admin = create_admin(db_session)

    users = get_all_users(db_session, admin)

    usernames = [u.username for u in users]

    assert "john" in usernames
    assert "mike" in usernames
    assert "admin" in usernames

import pytest

def test_player_cannot_read_all_users(db_session):
    user1 = register_player(db_session, "john", "1234")
    user2 = register_player(db_session, "mike", "1234")

    with pytest.raises(PermissionError):
        get_all_users(db_session, user1)