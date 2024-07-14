def parse_results(results):
    post = None
    comments = []

    for row in results:
        if post is None:
            post = {
                "content": row.post_content,
                "creator_id": row.post_creator_id,
                "reply_to": row.post_reply_to,
                "id": row.post_id,
                "created_at": row.post_created_at.isoformat(),
                "creator": {
                    "name": row.user_name,
                    "profile_pic": row.user_profile_pic,
                    "id": row.user_id,
                    "created_at": row.user_created_at.isoformat(),
                },
                "comments": []
            }
        comment = {
            "content": row.comment_content,
            "creator_id": row.comment_creator_id,
            "reply_to": row.comment_reply_to,
            "id": row.comment_id,
            "created_at": row.comment_created_at.isoformat(),
        }
        comments.append(comment)

    for comment in comments:
        comment["creator"] = {
            "name": row.comment_creator_name,
            "profile_pic": row.comment_creator_profile_pic,
            "id": row.comment_creator_id,
            "created_at": row.comment_creator_created_at.isoformat(),

        }
        comment["comments"] = row.reply_count

    if post:
        post["comments"] = comments

    return post


