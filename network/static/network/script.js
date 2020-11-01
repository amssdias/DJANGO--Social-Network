document.addEventListener('DOMContentLoaded', function() {

    // Follow and Unfollow users
    let follow = document.getElementById('follow');
    let unfollow = document.getElementById('unfollow');

    // To follow user
    if (follow !== null)
    {
        follow.onclick = () => {

            // Get user_id we want to follow
            user_id = follow.dataset.userid;
            follower = follow.dataset.follower;
            
            // Update followers of user
            fetch(`/follow/${user_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    follower_to_add: follower,
                    user: user_id
                })
            }).then(function() {
                document.querySelector("#followers").innerHTML++;
                follow.classList.add("d-none");
                unfollow.classList.remove("d-none");
            })
            .catch(error => console.log("Error: ", error))

        }
    }
    
    // To unfollow user
    if (unfollow !== null)
    {
        unfollow.onclick = () => {

            // Get user_id we want to follow
            user_id = unfollow.dataset.userid;
            follower = unfollow.dataset.follower;
            
            // Update followers of user
            fetch(`/follow/${user_id}`, {
                method: 'DELETE',
                body: JSON.stringify({
                    follower_to_remove: follower,
                    user: user_id
                })
            }).then(function() {
                document.querySelector("#followers").innerHTML--;
                unfollow.classList.add("d-none");
                follow.classList.remove("d-none");
            })
            .catch(error => console.log("Error: ", error))
        }
    }
    

    // Edit Post
    // Get all buttons to edit post
    document.querySelectorAll('.edit').forEach(function(button) {

        // If we click to edit post
        button.onclick = function() {

            // Get post id
            let post_id = this.id.slice(5);

            this.classList.add('d-none');

            document.querySelector(`#save-${post_id}`).classList.remove('d-none');

            // Get post
            let post = document.querySelector(`#post-${post_id}`);
            let post_content = post.innerHTML;

            // Get Container of post
            let container_post = this.parentElement;

            // Create text area
            const text_area = document.createElement('textarea');
            text_area.innerHTML = post_content;
            text_area.classList.add('form-control');
            text_area.id = `new_post-${post_id}`

            // Add text area to p
            post.innerHTML = '';
            post.append(text_area);

        }
    })

    // Get all buttons to save post
    document.querySelectorAll('.save').forEach(function(button) {

        // If we click to edit post
        button.onclick = function() {
            
            // Get id of post
            let post_id = this.id.slice(5);

            // Hide Save button and show edit
            this.classList.add('d-none');
            document.querySelector(`#edit-${post_id}`).classList.remove('d-none');

            // Get new post
            let post = document.querySelector(`#new_post-${post_id}`);
            let new_post = post.value;

            // API to change post
            fetch(`http://127.0.0.1:8000/edit/${post_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    new_post: new_post
                })
            })
            .catch(error => console.log("Error: ", error))
            
            post.remove();
            let p_tag = document.querySelector(`#post-${post_id}`);
            p_tag.innerHTML = new_post;
            
        }
    })


    // Like a post
    // User click on each empty heart to like
    document.querySelectorAll('.like').forEach(like => {

        like.onclick = function() {

            postID = this.dataset.like;

            // Add the Full heart
            fullHeart = document.querySelector(`[data-unlike="${postID}"]`);
            fullHeart.classList.remove('d-none');

            // Remove empty heart
            this.classList.add('d-none');

            // API to add like
            fetch(`http://127.0.0.1:8000/like/${postID}`, {
                method: "PUT",
                body: JSON.stringify({
                    like: postID
                })
            })
            .catch(error => console.log("Error: ", error))
            
            document.querySelector(`[data-postLikes="${postID}"]`).innerHTML++;

        };
    }); 

    // User click on each heart to unlike
    document.querySelectorAll('.unlike').forEach(element => {

        element.onclick = function() {

            postID = this.dataset.unlike;

            // Add the empty heart
            emptyHeart = document.querySelector(`[data-like="${postID}"]`);
            emptyHeart.classList.remove('d-none');

            // Remove heart
            this.classList.add('d-none');

            // API to add like
            fetch(`http://127.0.0.1:8000/like/${postID}`, {
                method: "DELETE",
                body: JSON.stringify({
                    unlike: postID
                })
            })
            .catch(error => console.log("Error: ", error))

            document.querySelector(`[data-postLikes="${postID}"]`).innerHTML--;

        };
    });

});