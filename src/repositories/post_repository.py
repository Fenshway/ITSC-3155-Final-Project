from src.models import Post, Post_Vote
from app import db
from sqlalchemy import exists, inspect

class PostRepository:
    def get_all_posts(self):
        posts = Post.query.all()
        return posts
    def get_all_posts_ordered(self):
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return posts

    def get_post_by_id(self, post_id):
        return Post.query.get(post_id)

    def get_all_posts_by_user(self, posted_by_id):
        posts = Post.query.filter_by(posted_by_id=posted_by_id).all()
        return posts

    def create_post_embedded_video(self, title, embedded_video_link, posted_by_id):
        new_post = Post(title, 'embedded_video', embedded_video_link, None, None, None, posted_by_id)
        db.session.add(new_post)
        db.session.commit()
        return new_post
        
    def create_post_stored_video(self, title, video_path, posted_by_id):
        new_post = Post(title, 'stored_video', None, video_path, None, None, posted_by_id)
        db.session.add(new_post)
        db.session.commit()
        return new_post

    def create_post_stored_image(self, title, image_path, posted_by_id):
        new_post = Post(title, 'stored_image', None, None, image_path, None, posted_by_id)
        db.session.add(new_post)
        db.session.commit()
        return new_post
    
    def create_post_text(self, title, post_text, posted_by_id):
        new_post = Post(title, 'text', None, None, None, post_text, posted_by_id)
        db.session.add(new_post)
        db.session.commit()
        return new_post

    def search_post(self, post_title):
        searched_post = Post.query.filter(Post.title.ilike("%"+post_title+"%"))
        return searched_post
    

    def vote_post(self, user_id, post_id, vote):
        vote_update = Post_Vote.query.get((user_id,post_id))
        if vote_update != None:
            if vote_update.upvote:
                if vote == "1":
                    db.session.delete(vote_update) 
                elif vote == "2":
                    vote_update.upvote = False
            else:
                if vote == "1":
                    vote_update.upvote = True
                elif vote == "2":
                    db.session.delete(vote_update) 
        else:
            if vote == "1":
                new_vote = Post_Vote(user_id,post_id, True)
                post = post_repository_singleton.get_post_by_id(post_id)
                db.session.add(new_vote)
                post.votes.append(new_vote)
            elif vote == "2":
                new_vote = Post_Vote(user_id,post_id, False)
                post = post_repository_singleton.get_post_by_id(post_id)
                db.session.add(new_vote)
                post.votes.append(new_vote)

        db.session.commit() 
        

         
        

        
        
       



    

post_repository_singleton = PostRepository()