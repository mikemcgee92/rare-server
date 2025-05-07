from models import Comment
import sqlite3

def get_comments_on_post(post_id):
  """ Gets all comments on a specific post """
  
  with sqlite3.connect("./db.sqlite3") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
    
    db_cursor.execute("""
    SELECT 
      c.id,
      c.author_id,
      c.post_id,
      c.content
    FROM Comments c
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

def get_comments_by_user(author_id):
  """ Gets all comments by a specific user """
  
  with sqlite3.connect("./db.sqlite3") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
    
    db_cursor.execute("""
    SELECT 
      c.id,
      c.author_id,
      c.post_id,
      c.content
    FROM Comments c
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

def get_single_comment(id):
  """ Gets a single comment """
  
  with sqlite3.connect("./db.sqlite3") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
    
    db_cursor.execute("""
    SELECT
      c.id,
      c.author_id,
      c.post_id,
      c.content
    FROM Comments c
    WHERE c.id = ?
    """, (id, ))
    
    data = db_cursor.fetchone()
    
    comment = Comment(
      data['id'],
      data['author_id'],
      data['post_id'],
      data['content']
    )
  
  return comment.__dict__

# not sure if this has any practical use, but it is an available function
def get_all_comments():
  """ Gets all comments in the database """
  with sqlite3.connect("./db.sqlite3") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
    
    db_cursor.execute("""
    SELECT 
      c.id,
      c.author_id,
      c.post_id,
      c.content
    FROM Comments c
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

def create_comment(new_comment):
  """ Creates a comment on a post """
  
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

def update_comment(id, new_comment):
  """ Updates a comment """
  
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

def delete_comment(id):
  """ Removes a comment """
  
  with sqlite3.connect("./db.sqlite3") as conn:
    db_cursor = conn.cursor()
    
    db_cursor.execute("""
    DELETE FROM Comments
    WHERE id = ?
    """, (id, ))
