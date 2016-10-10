-- add to activity notification queue:

insert into notify_queue
   (user_id, comment_id)

   -- get original message user, and all commenters:
   select
      distinct user_id, {comment_id}
   from
      messages
   where
      user_id != {user_id} and
      (id = {message_id} or reference_id = {message_id})

   UNION

   -- get all likers:
   select
      user_id, {comment_id}
   from
      likes
   where
      user_id != {user_id} and
      message_id = {message_id}
;
