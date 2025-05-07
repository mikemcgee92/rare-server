CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" TEXT,
  "last_name" TEXT,
  "email" TEXT,
  "bio" TEXT,
  "username" TEXT,
  "password" TEXT,
  "profile_image_url" TEXT,
  "created_on" DATE,
  "active" INTEGER
);

CREATE TABLE "DemotionQueue" (
  "action" TEXT,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY("admin_id") REFERENCES "Users"("id"),
  FOREIGN KEY("approver_one_id") REFERENCES "Users"("id"),
  PRIMARY KEY ("action", "admin_id", "approver_one_id")
);

CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" DATE,
  FOREIGN KEY("follower_id") REFERENCES "Users"("id"),
  FOREIGN KEY("author_id") REFERENCES "Users"("id")
);

CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" TEXT,
  "publication_date" DATE,
  "image_url" TEXT,
  "content" TEXT,
  "approved" INTEGER,
  FOREIGN KEY("user_id") REFERENCES "Users"("id")
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" TEXT,
  FOREIGN KEY("post_id") REFERENCES "Posts"("id"),
  FOREIGN KEY("author_id") REFERENCES "Users"("id")
);

CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" TEXT,
  "image_url" TEXT
);

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY("user_id") REFERENCES "Users"("id"),
  FOREIGN KEY("reaction_id") REFERENCES "Reactions"("id"),
  FOREIGN KEY("post_id") REFERENCES "Posts"("id")
);

CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" TEXT
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY("post_id") REFERENCES "Posts"("id"),
  FOREIGN KEY("tag_id") REFERENCES "Tags"("id")
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" TEXT
);


INSERT INTO Categories ("label") VALUES ('News');
INSERT INTO Tags ("label") VALUES ('JavaScript');
INSERT INTO Reactions ("label", "image_url") VALUES ('happy', 'https://pngtree.com/so/happy');
INSERT INTO Categories ('label') VALUES ('News');
INSERT INTO Tags ('label') VALUES ('JavaScript');
INSERT INTO Reactions ('label', 'image_url') VALUES ('happy', 'https://pngtree.com/so/happy');
INSERT INTO Comments ('id', 'author_id', 'post_id', 'content') VALUES (1, 1, 1, 'sample text');

