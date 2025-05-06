from models import Comment
import sqlite3

# Get all comments on a single post
def get_comments_on_post(post_id):
  with sqlite3.connect("./db.sqlite3") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
    
    db_cursor.execute("""
    SELECT 
      c.id,
      c.author_id,
      c.post_id,
      c.content
    FROM comment c
    WHERE c.post_id = ?
    """, (post_id, ))
    
    comments = []
    dataset = db_cursor.fetchall()
    
    for row in dataset:
      comment = Comment(
        row['id'],
        row['author_id'],
        row['post_id'],
        row['content'])
      
      comments.append(comment.__dict__)
  
  return comments

# Get all comments by a specific user
def get_comments_by_user(author_id):
  with sqlite3.connect("./db.sqlite3") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
    
    db_cursor.execute("""
    SELECT 
      c.id,
      c.author_id,
      c.post_id,
      c.content
    FROM comment c
    WHERE c.author_id = ?
    """, (author_id, ))
    
    comments = []
    dataset = db_cursor.fetchall()
    
    for row in dataset:
      comment = Comment(
        row['id'],
        row['author_id'],
        row['post_id'],
        row['content'])
      
      comments.append(comment.__dict__)
  
  return comments

# Get a single comment
def get_single_comment(id):
  with sqlite3.connect("./db.sqlite3") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
    
    db_cursor.execute("""
    SELECT
      c.id,
      c.author_id,
      c.post_id,
      c.content
    FROM comment c
    WHERE c.id = ?
    """, (id, ))
    
    data = db_cursor.fetchone()
    
    comment = Comment(
      data['id'],
      data['author_id'],
      data['post_id'],
      data['content']
    )
  
  return comment

# Get all comments ... not sure if this has any practical use, but it is an available function
def get_all_comments():
  with sqlite3.connect("./db.sqlite3") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
    
    db_cursor.execute("""
    SELECT 
      c.id,
      c.author_id,
      c.post_id,
      c.content
    FROM comment c
    """)
    
    comments = []
    dataset = db_cursor.fetchall()
    
    for row in dataset:
      comment = Comment(
        row['id'],
        row['author_id'],
        row['post_id'],
        row['content']
      )
      comments.append(comment.__dict__)
  
  return comments

# Create a comment on a post
def create_comment(new_comment):
  with sqlite3.connect("./db.sqlite3") as conn:
    db_cursor = conn.cursor()
    
    db_cursor.execute("""
    INSERT INTO Comments
      ( author_id, post_id, content )
    VALUES
      ( ?, ?, ?);
    """, (new_comment['author_id'], new_comment['post_id'], new_comment['content']))
    
    id = db_cursor.lastrowid
    
    new_comment['id'] = id
  
  return new_comment

# Edit a comment
def update_comment(id, new_comment):
  with sqlite3.connect("./db.sqlite3") as conn:
    db_cursor = conn.cursor()
    
    db_cursor.execute("""
    UPDATE Comments
      SET
        author_id = ?,
        post_id = ?,
        content = ?
    WHERE id = ?
    """, (new_comment['author_id'], new_comment['post_id'], new_comment['content'], id, ))
    
    rows_affected = db_cursor.rowcount
  
  if rows_affected == 0:
    return False #status code 404
  else:
    return True #status code 204

# Remove a comment
def delete_comment(id):
  with sqlite3.connect("./db.sqlite3") as conn:
    db_cursor = conn.cursor()
    
    db_cursor.execute("""
    DELETE FROM Comments
    WHERE id = ?
    """, (id, ))
