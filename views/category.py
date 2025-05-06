import json
import sqlite3

from models import Category


def get_all_categories():
    """Get all categories from the database"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            id,
            label
        FROM Categories
        ORDER BY label
        """
        )

        categories = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            category = Category(row["id"], row["label"])
            categories.append(category.__dict__)

    return categories


def get_single_category(id):
    """Get a single category by id"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            id,
            label
        FROM Categories
        WHERE id = ?
        """,
            (id,),
        )

        data = db_cursor.fetchone()

        if data is None:
            return {"error": "Category not found", "status": 404}

        category = Category(data["id"], data["label"])

    return category.__dict__


def create_category(new_category):
    """Create a new category"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        # Validate category data
        if "label" not in new_category or not new_category["label"].strip():
            return {"error": "Label is required"}

        # Check if category with same label already exists
        db_cursor.execute(
            """
        SELECT id FROM Categories WHERE label = ?
        """,
            (new_category["label"],),
        )

        existing_category = db_cursor.fetchone()
        if existing_category:
            return {"error": "A category with this label already exists"}

        db_cursor.execute(
            """
        INSERT INTO Categories
            (label)
        VALUES
            (?)
        """,
            (new_category["label"],),
        )

        id = db_cursor.lastrowid

        new_category["id"] = id

    return new_category


def update_category(id, category_data):
    """Update an existing category"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        # Validate category data
        if "label" in category_data and not category_data["label"].strip():
            return {"error": "Label cannot be empty"}

        # Check if category exists
        db_cursor.execute(
            """
        SELECT id FROM Categories WHERE id = ?
        """,
            (id,),
        )

        category = db_cursor.fetchone()
        if not category:
            return {"error": "Category not found", "status": 404}

        # Check if new label is already in use by another category
        if "label" in category_data:
            db_cursor.execute(
                """
            SELECT id FROM Categories WHERE label = ? AND id != ?
            """,
                (category_data["label"], id),
            )

            existing_category = db_cursor.fetchone()
            if existing_category:
                return {"error": "A category with this label already exists"}

            # Update the category
            db_cursor.execute(
                """
            UPDATE Categories
            SET label = ?
            WHERE id = ?
            """,
                (category_data["label"], id),
            )

            rows_affected = db_cursor.rowcount

            if rows_affected == 0:
                return {"message": "No changes were made", "status": 200}
            else:
                return {"message": "Category updated successfully", "status": 204}
        else:
            return {"message": "No valid fields to update", "status": 400}


def delete_category(id):
    """Delete a category"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        # Check if there are posts using this category
        db_cursor.execute(
            """
        SELECT COUNT(*) as post_count FROM Posts WHERE category_id = ?
        """,
            (id,),
        )

        result = db_cursor.fetchone()
        if result[0] > 0:
            return {
                "error": "Cannot delete category that is in use by posts",
                "status": 400,
            }

        # Delete the category
        db_cursor.execute(
            """
        DELETE FROM Categories
        WHERE id = ?
        """,
            (id,),
        )

        return {"message": "Category deleted", "status": 204}
