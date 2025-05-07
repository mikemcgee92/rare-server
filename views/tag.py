import json
import sqlite3

from models import Tag


def get_all_tags():
    """Get all tags from the database"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            id,
            label
        FROM Tags
        ORDER BY label
        """
        )

        tags = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row["id"], row["label"])
            tags.append(tag.__dict__)

    return tags


def get_single_tag(id):
    """Get a single tag by id"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            id,
            label
        FROM Tags
        WHERE id = ?
        """,
            (id,),
        )

        data = db_cursor.fetchone()

        if data is None:
            return {"error": "Tag not found", "status": 404}

        tag = Tag(data["id"], data["label"])

    return tag.__dict__


def create_tag(new_tag):
    """Create a new tag"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        # Validate tag data
        if "label" not in new_tag or not new_tag["label"].strip():
            return {"error": "Label is required"}

        # Check if tag with same label already exists
        db_cursor.execute(
            """
        SELECT id FROM Tags WHERE label = ?
        """,
            (new_tag["label"],),
        )

        existing_tag = db_cursor.fetchone()
        if existing_tag:
            return {"error": "A tag with this label already exists"}

        db_cursor.execute(
            """
        INSERT INTO Tags
            (label)
        VALUES
            (?)
        """,
            (new_tag["label"],),
        )

        id = db_cursor.lastrowid

        new_tag["id"] = id

    return new_tag


def update_tag(id, tag_data):
    """Update an existing tag"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        # Validate tag data
        if "label" in tag_data and not tag_data["label"].strip():
            return {"error": "Label cannot be empty"}

        # Check if tag exists
        db_cursor.execute(
            """
        SELECT id FROM Tags WHERE id = ?
        """,
            (id,),
        )

        tag = db_cursor.fetchone()
        if not tag:
            return {"error": "Tag not found", "status": 404}

        # Check if new label is already in use by another tag
        if "label" in tag_data:
            db_cursor.execute(
                """
            SELECT id FROM Tags WHERE label = ? AND id != ?
            """,
                (tag_data["label"], id),
            )

            existing_tag = db_cursor.fetchone()
            if existing_tag:
                return {"error": "A tag with this label already exists"}

            # Update the tag
            db_cursor.execute(
                """
            UPDATE Tags
            SET label = ?
            WHERE id = ?
            """,
                (tag_data["label"], id),
            )

            rows_affected = db_cursor.rowcount

            if rows_affected == 0:
                return {"message": "No changes were made", "status": 200}
            else:
                return {"message": "Tag updated successfully", "status": 204}
        else:
            return {"message": "No valid fields to update", "status": 400}


def delete_tag(id):
    """Delete a tag"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        # Check if there are posts using this tag
        db_cursor.execute(
            """
        SELECT COUNT(*) as post_count FROM PostTags WHERE tag_id = ?
        """,
            (id,),
        )

        result = db_cursor.fetchone()
        if result[0] > 0:
            # Remove the tag from all posts first
            db_cursor.execute(
                """
            DELETE FROM PostTags
            WHERE tag_id = ?
            """,
                (id,),
            )

        # Delete the tag
        db_cursor.execute(
            """
        DELETE FROM Tags
        WHERE id = ?
        """,
            (id,),
        )

        return {"message": "Tag deleted", "status": 204}
